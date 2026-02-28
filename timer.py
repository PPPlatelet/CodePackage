import logging
import time
import threading
from queue import Queue
from functools import wraps
from typing import Any, Callable

logger = logging.getLogger('Timer')
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s │ %(message)s')

class FunctionTimeoutError(Exception):
    pass

def fib(n: int) -> int:
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def get_func_path(func: Callable[..., Any]) -> str:
    """
    Get a function's relative path.

    Args:
        func (Callable[..., Any]):

    Examples:
        >>> get_func_path(report)
        'module.device.platform.winapi.functions_windows.report'
        >>> get_func_path(FILETIME.__init_subclass__)
        'module.device.platform.winapi.structures_windows.Structure::__init_subclass__'

    Returns:
        str:
    """
    if not callable(func):
        raise TypeError(f"Expected a callable, but got {type(func).__name__}")

    module = getattr(func, '__module__', '')
    qualname = getattr(func, '__qualname__', getattr(func, '__name__', '')).replace('.', '::')

    return '.'.join(filter(lambda x: x != '', [module, qualname]))

class Timer:
    def __init__(self, limit, count=0):
        """
        Args:
            limit (int, float): Timer limit
            count (int): Timer reach confirm count. Default to 0.
                When using a structure like this, must set a count.
                Otherwise it goes wrong, if screenshot time cost greater than limit.

                if self.appear(MAIN_CHECK):
                    if confirm_timer.reached():
                        pass
                else:
                    confirm_timer.reset()

                Also, It's a good idea to set `count`, to make alas run more stable on slow computers.
                Expected speed is 0.35 second / screenshot.
        """
        self.limit = limit
        self.count = count
        self._current = 0
        self._reach_count = count

    def start(self):
        if not self.started():
            self._current = time.time()
            self._reach_count = 0

        return self

    def started(self):
        return bool(self._current)

    def current(self):
        """
        Returns:
            float
        """
        if self.started():
            return time.time() - self._current
        else:
            return 0.

    def reached(self):
        """
        Returns:
            bool
        """
        self._reach_count += 1
        return time.time() - self._current > self.limit and self._reach_count > self.count

    def reset(self):
        self._current = time.time()
        self._reach_count = 0
        return self

    def clear(self):
        self._current = 0
        self._reach_count = self.count
        return self

    def reached_and_reset(self):
        """
        Returns:
            bool:
        """
        if self.reached():
            self.reset()
            return True
        else:
            return False

    def wait(self):
        """
        Wait until timer reached.
        """
        diff = self._current + self.limit - time.time()
        if diff > 0:
            time.sleep(diff)

    def show(self):
        logger.info(str(self))

    def __str__(self):
        return f'Timer(limit={round(self.current(), 3)}/{self.limit}, count={self._reach_count}/{self.count})'

    __repr__ = __str__

class TimerLogger:
    def __init__(self, func: Callable[..., Any], level: int):
        self.path = get_func_path(func)
        self.original_level = level
        logger.setLevel(logging.DEBUG)

    def __enter__(self):
        logger.debug(f"{self.path} | Enter")
        self.start_time = time.perf_counter()
        return self.path

    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb: Any):
        self.execution_time = (time.perf_counter() - self.start_time) * 1e3
        logger.debug(f"{self.path} | Leave, {self.execution_time:.2f} ms")
        logger.setLevel(self.original_level)
        """
        if exc_type is None:
            logger.debug(f"{self.path} | Leave, {self.execution_time:.2f} ms")
        else:
            logger.error(f"{self.path} | Exception occurred: {exc_type.__name__}: {exc_val}")
            if exc_tb:
                tb_str = ''.join(traceback.format_tb(exc_tb))
                logger.error(f"{self.path} | Traceback:\n{tb_str}")
        """

F = Callable[..., Any]
def timer(timeout: int | float = 1):
    """
    A decorator to measure the execution time of a function with timeout control.

    Args:
        timeout (int): The maximum allowed execution time (in seconds) for the function.

    Notes:
        - There's no way to kill a RUNNING thread! Please ensure that the decorated function doesn't get stuck in an infinite loop.
        - threading.RLock is strongly recommended to ensure thread safety.
        - This decorator is not intended for use in user environments. Please modify it if needed.

    Examples:
        >>> @timer(timeout=2)
        >>> def fun():
        >>>     for i in range(5):
        >>>         logger.info("Function 'fun' running...")
        >>>         time.sleep(1)
        >>>
        >>> try:
        >>>     fun()
        >>> except TimeoutError as e:
        >>>     logger.error(e)
        DEBUG │ __main__.fun | Enter
        INFO  │ Function 'fun' running...
        INFO  │ Function 'fun' running...
        INFO  │ Function 'fun' running...
        DEBUG │ __main__.fun | Leave, 2015.5029000000013 ms
        ERROR │ TimeoutError: Function __main__.fun timedout after 2 seconds
        INFO  │ Function 'fun' running...
        INFO  │ Function 'fun' running...

    Raises:
        TypeError: If the function is not callable.
        FunctionTimeoutError: If the function execution time exceeds the specified timeout.
        Exception: Any exceptions that may be thrown by the decorated function.
    """
    def decorator(func: F) -> F:
        if not callable(func):
            raise TypeError(f"Expected a callable, but got {type(func).__name__}")
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result, exc = None, None
            stop_event, _lock = threading.Event(), threading.RLock()

            def target():
                nonlocal result, exc
                with _lock:
                    try:
                        result = func(*args, **kwargs)
                    except Exception as e:
                        exc = e
                    finally:
                        stop_event.set()

            with TimerLogger(func, logger.level) as path:
                target_thread = threading.Thread(target=target, name=f"Thread-{path}")
                target_thread.start()

                if not stop_event.wait(timeout=timeout):
                    raise FunctionTimeoutError(f"Function {path} timed out after {timeout} seconds")

                if exc is not None:
                    raise exc
                return result
        return wrapper
    return decorator

@timer(timeout=2)
def fun(t: int):
    logger.info(f"Function 'fun' running. Sleep for {t} seconds...")
    time.sleep(t)

def test():
    threads: list[threading.Thread] = []
    for t in range(5):
        threads.append(threading.Thread(target=fun, args=(t,)))
    
    for thread in threads:
        try:
            thread.start()
        except FunctionTimeoutError as e:
            logger.error(e)

@timer(timeout=2)
def test2():
    _lock = threading.Lock()

    def worker(t: int, q: Queue[tuple[int, int]]) -> None:
        result = fib(t)
        with _lock:
            q.put((t, result))

    threads: list[threading.Thread] = []
    results: Queue[tuple[int, int]] = Queue()
    for t in range(20, 40, 2):
        threads.append(threading.Thread(target=worker, args=(t, results)))

    for thread in threads:
        try:
            thread.start()
        except FunctionTimeoutError as e:
            logger.error(e)
    
    for thread in threads:
        thread.join()

    while not results.empty():
        t, result = results.get()
        print(f"fib({t}) = {result}")

if __name__ == '__main__':
    try:
        test2()
    except FunctionTimeoutError as e:
        logger.error(e)

import logging
import time
import threading
from functools import wraps
from typing import Any, Callable

logger = logging.getLogger('Timer')
class FunctionTimeoutError(Exception):
    pass

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

class TimerLogger:
    def __init__(self, func, level):
        self.path = get_func_path(func)
        self.original_level = level
        logger.setLevel(logging.DEBUG)

    def __enter__(self):
        logger.debug(f"{self.path} | Enter")
        self.start_time = time.perf_counter()
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.execution_time = (time.perf_counter() - self.start_time) * 1e3
        logger.debug(f"{self.path} | Leave, {self.execution_time} ms")
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

def timer(timeout: int = 1):
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
        TimeoutError: If the function execution time exceeds the specified timeout.
        Exception: Any exceptions that may be thrown by the decorated function.
    """
    def decorator(func):
        if not callable(func):
            raise TypeError(f"Expected a callable, but got {type(func).__name__}")

        @wraps(func)
        def wrapper(*args, **kwargs):
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

import threading

class SingletonMeta(type):
    _instances = {}
    _lock = threading.RLock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class MultitonMeta(SingletonMeta):
    _instances = {}
    _lock = threading.RLock()

    def __call__(cls, *args, **kwargs):
        key = (cls, args, frozenset(kwargs.items()))
        with cls._lock:
            if key not in cls._instances:
                cls._instances[key] = type.__call__(*args, **kwargs)
        return cls._instances[key]
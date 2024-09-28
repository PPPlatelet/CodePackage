from functools import wraps
import inspect

class OverloadError(Exception):
    pass

def get_function_types(*params):
    types = []

    for param in params:
        if callable(param):
            types.append(param.__name__)
        elif isinstance(param, tuple):
            types.extend(type(arg).__name__ for arg in param)
        elif isinstance(param, dict):
            types.extend(type(value).__name__ for value in param.values())
        else:
            raise TypeError(f"Invalid parameter type: {type(param).__name__}. Expected callable, tuple or dict.")
    
    return tuple(types)

def get_param_types(params):
    types = []

    for param in params:
        if isinstance(param, type):
            types.append(param.__name__)
        elif isinstance(param, str):
            types.append(param)
        else:
            types.append(param.__name__)

    return tuple(types)

_instances = {}

def overload(name, *params):
    def decorator(func):
        if not callable(func):
            raise TypeError(f"Expected a callable, but got {type(func).__name__}")
        
        _types = get_param_types(params)

        _hashtypes = hash((name, ) + _types)

        if _hashtypes in _instances:
            raise OverloadError(f"Function {_instances[_hashtypes]} is already defined")
        
        _instances[_hashtypes] = func
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            types = get_function_types(func, args, kwargs)
            hashtypes = hash(types)

            if hashtypes not in _instances:
                raise TypeError(f"No matching overloaded function for types: {hashtypes}")

            return _instances[hashtypes](*args, **kwargs)
        return wrapper
    return decorator

class Overload2:
    _instances = {}
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Overload2, cls).__new__(cls)
        return cls._instance

    def __call__(self, name, *params: type | str):
        def decorator(func):
            if not callable(func):
                raise TypeError(f"Expected a callable, but got {type(func).__name__}")
            
            _types = get_param_types(params)
            
            _hashtypes = hash((name, ) + _types)

            if _hashtypes in self._instances:
                raise OverloadError(f"Function {self._instances[_hashtypes]} is already defined")
            
            self._instances[_hashtypes] = func
            
            @wraps(func)
            def wrapper(*args, **kwargs):

                types = get_function_types(func, args, kwargs)
                hashtypes = hash(types)

                if hashtypes not in self._instances:
                    raise TypeError(f"No matching overloaded function for types: {hashtypes}")

                return self._instances[hashtypes](*args, **kwargs)
            return wrapper
        return decorator

class Overload3:
    _instances = {}
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Overload3, cls).__new__(cls)
        return cls._instance

    def __call__(self, func):
        sig = inspect.signature(func)
        name = func.__name__
        _types = tuple(param.annotation.__name__ for param in sig.parameters.values())

        if any(t == inspect.Parameter.empty for t in _types):
            raise TypeError("All parameters must be annotated with types for overloading")
        
        _hashtypes = hash((name, ) + _types)

        if _hashtypes in self._instances:
            raise OverloadError(f"Function {self._instances[_hashtypes]} is already defined")
        
        self._instances[_hashtypes] = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            types = get_function_types(func, args, kwargs)

            hashtypes = hash(types)

            if hashtypes not in self._instances:
                raise TypeError(f"No matching overloaded function for types: {hashtypes}")

            return self._instances[hashtypes](*args, **kwargs)
        return wrapper

# overload = Overload()
overload2 = Overload2()
overload3 = Overload3()

@overload2('foo', int)
def foo(a: int):
    return f"Integer: {a}"

@overload2('foo', str)
def foo(a: str):
    return f"String: {a}"

@overload2('foo', 'dict')
def foo(a: dict):
    return f"Dict: {a}"

print(foo(10))
print(foo("hello"))
print(foo({'b': 1, 'c': '2'}))

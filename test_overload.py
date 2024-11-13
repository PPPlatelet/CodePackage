from functools import wraps
import inspect
from typing import Any, Callable

class OverloadError(Exception):
    pass

def get_function_types(*params: Callable[..., Any] | tuple | dict):
    """
    Get the types of the parameters of a function.

    Args:
        params (tuple): A tuple of parameters.
    
    Returns:
        tuple: A tuple of types.
    
    Raises:
        TypeError: If the parameter type is not callable, tuple or dict.
    """
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

def get_param_types(params: tuple):
    """
    Get the types of the parameters of a function.

    Args:
        params (tuple): A tuple of parameters.

    Returns:
        tuple: A tuple of types.
    """
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
        
        # get parameter types and hash them
        _types = get_param_types(params)
        _hashtypes = hash((name, ) + _types)

        # check if function is already defined
        if _hashtypes in _instances:
            raise OverloadError(f"Function {_instances[_hashtypes]} is already defined")
        
        # register function
        _instances[_hashtypes] = func
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # get function types and hash them
            types = get_function_types(func, args, kwargs)
            hashtypes = hash(types)

            # check if function is not in the registry
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

            # get parameter types and hash them
            _types = get_param_types(params)
            _hashtypes = hash((name, ) + _types)

            # check if function is already defined
            if _hashtypes in self._instances:
                raise OverloadError(f"Function {self._instances[_hashtypes]} is already defined")
            
            # register function
            self._instances[_hashtypes] = func
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                # get function types and hash them
                types = get_function_types(func, args, kwargs)
                hashtypes = hash(types)

                # check if function is not in the registry
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
        if not callable(func):
            raise TypeError(f"Expected a callable, but got {type(func).__name__}")
        
        # get function signature
        sig = inspect.signature(func)
        name = func.__name__
        
        # get parameter information
        param_info = [(param.name, param.annotation) for param in sig.parameters.values()]
        
        # check if all parameters are annotated
        if any(annotation == inspect.Parameter.empty for _, annotation in param_info):
            raise TypeError("All parameters must be annotated with types for overloading")
        
        # get parameter types and hash them
        _types = tuple(annotation.__name__ for _, annotation in param_info)
        _hashtypes = hash((name, ) + _types)

        # check if function is already defined
        if _hashtypes in self._instances:
            raise OverloadError(f"Function {self._instances[_hashtypes]} is already defined")
        
        # register function
        self._instances[_hashtypes] = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            # get function types and hash them
            arg_types = tuple(type(arg).__name__ for arg in args)
            kwarg_types = tuple(type(value).__name__ for value in kwargs.values())
            types = (name, ) + arg_types + kwarg_types
            hashtypes = hash(types)

            # check if function is not in the registry
            if hashtypes not in self._instances:
                raise TypeError(f"No matching overloaded function for types: {types}")

            return self._instances[hashtypes](*args, **kwargs)
        return wrapper

# 创建 Overload 实例
overload2 = Overload2()
overload3 = Overload3()

@overload2("foo", int)
def foo(a: int):
    return f"Integer: {a}"

@overload2("foo", str)
def foo(a: str):
    return f"String: {a}"

@overload2("foo", dict)
def foo(a: dict):
    return f"Dict: {a}"

@overload2("foo", tuple)
def foo(a: tuple):
    return f"Tuple: {a}"

@overload2("foo", int, str)
def foo(a: int, b: str):
    return str(a) + b

def test():
    print(foo(10))
    print(foo("hello"))
    print(foo({'b': 1, 'c': '2'}))
    print(foo((1, 2, 3, 'a', 'b', 'c')))
    print(foo(a = 12345, b = "hello"))

if __name__ == "__main__":
    test()

import threading
from typing import Any, Dict, Tuple, Type, TypeVar, Self

T = TypeVar('T', bound='ConditionalMultiton')

class SingletonMeta(type):
    _instances: Dict[Type['SingletonMeta'], Any] = {}
    _lock = threading.RLock()

    def __call__(cls, *args: Any, **kwargs: Any):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class MultitonMeta(type):
    _instances: Dict[Tuple[Type['MultitonMeta'], Tuple[Any, ...], frozenset[Any]], Any] = {}
    _lock = threading.RLock()

    def __call__(cls, *args: Any, **kwargs: Any):
        key = (cls, args, frozenset(kwargs.items()))
        with cls._lock:
            if key not in cls._instances:
                cls._instances[key] = super().__call__(*args, **kwargs)
        return cls._instances[key]

class ConditionalMultitonMeta(type):
    _instances: dict[Tuple[Type['ConditionalMultitonMeta'], Any], Any] = {}
    _lock = threading.RLock()

    def __call__(cls, *args: Any, **kwargs: Any):
        condition = kwargs.get('condition', None)

        if condition is None:
            raise ValueError("Condition must be provided")
        
        with cls._lock:
            for key, instance in cls._instances.items():
                if issubclass(key[0], cls) and cls.condition_match(key[1], condition):
                    cls._instances[(cls, condition)] = instance
                    return instance
            
            instance = super().__call__(*args, **kwargs)
            cls._instances[(cls, condition)] = instance
            return instance

    @staticmethod
    def condition_match(existing_condition: Any, new_condition: Any) -> bool:
        return existing_condition == new_condition

class ConditionalMultiton(metaclass=ConditionalMultitonMeta):
    def __init__(self, value: Any, condition: Any):
        self.value = value
        self.condition = condition

    @staticmethod
    def condition_match(existing_condition: Any, new_condition: Any) -> bool:
        return existing_condition == new_condition

class MyClass(ConditionalMultiton):
    @staticmethod
    def condition_match(existing_condition: int, new_condition: int) -> bool:
        return abs(existing_condition - new_condition) <= 5

if __name__ == "__main__":
    instance1 = MyClass(10, condition=0)
    instance2 = MyClass(20, condition=2)
    instance3 = MyClass(30, condition=-5)

    print(instance1 is instance2)  # 输出: True
    print(instance1 is instance3)  # 输出: True
    print(instance2 is instance3)  # 输出: True

    instance4 = MyClass(40, condition=10)
    print(instance4 is instance1)  # 输出: False
    print(instance4 is instance2)  # 输出: False
    print(instance4 is instance3)  # 输出: False

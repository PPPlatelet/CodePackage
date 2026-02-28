import threading

from typing import NoReturn, Any

def Next(ptr, size, step = 1):
    return (ptr + step) % size

def Prev(ptr, size, step = 1):
    return (ptr - step + size) % size

class OperationRecorder:
    def __init__(self, buffer_size = 5):
        self._lock = threading.RLock()
        self.buffer_size = buffer_size
        self.buffer: list[Any] = []
        self.tail = 0
        self.count = 0
        self.undocount = 0
        self.total = 0

    def record(self, data):
        with self._lock:
            if self.undocount > 0:
                self.count -= self.undocount
                self.undocount = 0

            if self.tail == self.total:
                self.buffer.append(data)
                self.total += 1
            else:
                self.buffer[self.tail] = data

            self.tail = Next(self.tail, self.buffer_size)
            if self.count < self.buffer_size:
                self.count += 1

    def undo(self) -> Any:
        with self._lock:
            if self.undocount >= self.count:
                return
            self.tail = Prev(self.tail, self.buffer_size)
            self.undocount += 1
            result = self.buffer[self.tail]
        return result
    
    def redo(self) -> Any:
        with self._lock:
            if self.undocount == 0:
                return
            self.undocount -= 1
            result = self.buffer[self.tail]
            self.tail = Next(self.tail, self.buffer_size)
        return result
    
    def clear(self):
        with self._lock:
            self.tail = 0
            self.count = 0
            self.undocount = 0

class OperationRecorderLite():
    def __init__(self, buffer_size = 5):
        self._lock = threading.RLock()
        self.buffer_size = buffer_size
        self.can_undo = False
        self.__buffer: list[Any] = [None] * buffer_size
        self.__head = 0
        self.__count = 0

    def record(self, data):
        with self._lock:
            self.can_undo = True
            self.__buffer[self.__head] = data
            self.__head = Next(self.__head, self.buffer_size)
            if self.__count < self.buffer_size:
                self.__count += 1
    
    def undo(self) -> Any:
        with self._lock:
            match self.__count:
                case 0:
                    return
                case 1:
                    self.can_undo = False
            self.__head = Prev(self.__head, self.buffer_size)
            self.__count -= 1
            result = self.__buffer[self.__head]
        return result

    def redo(self) -> NoReturn:
        raise NotImplementedError("No way.")
    
    def clear(self):
        with self._lock:
            self.__head = 0
            self.__count = 0
            self.can_undo = False

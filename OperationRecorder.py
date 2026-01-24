def Next(ptr, size, step = 1):
    return (ptr + step) % size

def Prev(ptr, size, step = 1):
    return (ptr - step + size) % size

class OperationRecorder:
    def __init__(self, buffer_size = 5):
        self.buffer_size = buffer_size
        self.buffer = []
        self.tail = 0
        self.count = 0
        self.undocount = 0
        self.total = 0

    def record(self, data):
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

    def undo(self):
        if self.undocount >= self.count:
            return
        self.tail = Prev(self.tail, self.buffer_size)
        self.undocount += 1
        return self.buffer[self.tail]
    
    def redo(self):
        if self.undocount == 0:
            return
        self.undocount -= 1
        tmp = self.buffer[self.tail]
        self.tail = Next(self.tail, self.buffer_size)
        return tmp
    
    def clear(self):
        self.tail = 0
        self.count = 0
        self.undocount = 0

class OperationRecorderLite():
    def __init__(self, buffer_size = 5):
        self.buffer_size = buffer_size
        self.can_undo = False
        self.__buffer = [None] * buffer_size
        self.__head = 0
        self.__count = 0

    def record(self, data):
        self.can_undo = True
        self.__buffer[self.__head] = data
        self.__head = Next(self.__head, self.buffer_size)
        if self.__count < self.buffer_size:
            self.__count += 1
    
    def undo(self):
        match self.__count:
            case 0:
                return
            case 1:
                self.can_undo = False
        self.__head = Prev(self.__head, self.buffer_size)
        self.__count -= 1
        return self.__buffer[self.__head]

    def redo(self):
        return None
    
    def clear(self):
        self.__head = 0
        self.__count = 0
        self.can_undo = False

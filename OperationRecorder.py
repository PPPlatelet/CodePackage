class OperationRecorder:
    def __init__(self, buffer_size = 5):
        self.buffer_size = buffer_size
        self.buffer = []
        self.tail = 0
        self.count = 0
        self.undocount = 0
        self.total = 0

    @classmethod
    def Next(cls, ptr, size, step = 1):
        return (ptr + step) % size
    
    @classmethod
    def Prev(cls, ptr, size, step = 1):
        return (ptr - step + size) % size

    def record(self, data):
        if self.undocount > 0:
            self.count -= self.undocount
            self.undocount = 0

        if self.tail == self.total:
            self.buffer.append(data)
            self.total += 1
        else:
            self.buffer[self.tail] = data

        self.tail = self.Next(self.tail, self.buffer_size)
        if self.count < self.buffer_size:
            self.count += 1

    def undo(self):
        if self.undocount >= self.count:
            return
        self.tail = self.Prev(self.tail, self.buffer_size)
        self.undocount += 1
        return self.buffer[self.tail]
    
    def redo(self):
        if self.undocount == 0:
            return
        self.undocount -= 1
        tmp = self.buffer[self.tail]
        self.tail = self.Next(self.tail, self.buffer_size)
        return tmp
    
    def clear(self):
        self.tail = 0
        self.count = 0
        self.undocount = 0

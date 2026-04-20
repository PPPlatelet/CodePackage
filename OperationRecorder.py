# import threading
import random
import time

from typing import Any
from dataclasses import dataclass

from timer import Timer

def Next(ptr, size, step = 1):
    return (ptr + step) % size

def Prev(ptr, size, step = 1):
    return (ptr - step + size) % size

class OperationRecorder:
    def __init__(self, size = 10000):
        self.size = size
        self.buffer = [None] * size
        self.tail = 0
        self.count = 0
        self.undocount = 0
    
    def record(self, data: Any):
        if self.undocount > 0:
            self.count -= self.undocount
            self.undocount = 0
        
        self.buffer[self.tail] = data
        
        self.tail = Next(self.tail, self.size)
        self.count = min(self.count + 1, self.size)
    
    def undo(self) -> Any:
        if self.undocount < self.count:
            self.tail = Prev(self.tail, self.size)
            self.undocount += 1
            return self.buffer[self.tail]
    
    def redo(self) -> Any:
        if self.undocount > 0:
            self.undocount -= 1
            res = self.buffer[self.tail]
            self.tail = Next(self.tail, self.size)
            return res
    
    def clear(self):
        self.tail = 0
        self.count = 0
        self.undocount = 0

@dataclass
class Frame:
    float3: tuple[float, float, float]
    velocity: tuple[float, float, float]

class Client():
    def __init__(self):
        self.buffer: list[list[Frame]] = [None] * 10000
        self.tail = 0
        self.count = 0
        self.undocount = 0
        self.buffer_idx = 0

        self.segment: list[Frame] = [None] * 16
        self.segment_idx = 0
        self.segment_idx_snapshot = 0

        self.rewind_active = False
        self.direction = 0
    
    def skill(self, frame: Frame):
        print(f"Skill executed: {frame.float3} with velocity {frame.velocity}")

    def record(self, data: Frame):
        if self.segment_idx < 16:
            self.segment[self.segment_idx] = data
            self.segment_idx += 1
            if self.segment_idx == 16:
                self.buffer[self.tail] = self.segment.copy()
                self.tail = Next(self.tail, 10000)
                self.count = min(self.count + 1, 10000)
                self.segment_idx = 0

    def replay(self):
        if not self.rewind_active:
            self.segment_idx_snapshot = self.segment_idx
            self.buffer_idx = 16

            self.rewind_active = True
            self.direction = -1
        else:
            if self.undocount > 0: # self.segment_idx = 0
                if 0 < self.buffer_idx < 16:
                    self.segment = self.buffer[self.tail].copy()
                    self.segment_idx = self.buffer_idx

                self.count -= self.undocount
                self.undocount = 0
            self.rewind_active = False
            self.direction = 0

    def rewind(self):
        match self.direction:
            case 0: # do nothing
                return
            case -1: # undo
                if self.segment_idx > 0:
                    self.segment_idx -= 1
                    self.skill(self.segment[self.segment_idx])
                    return
                
                if self.buffer_idx == 16:
                    if self.undocount < self.count:
                        self.tail = Prev(self.tail, 10000)
                        self.undocount += 1

                        self.buffer_idx = 15
                        self.skill(self.buffer[self.tail][self.buffer_idx])
                    return

                if 0 < self.buffer_idx < 16:
                    self.buffer_idx -= 1
                    self.skill(self.buffer[self.tail][self.buffer_idx])
                    if self.buffer_idx == 0 and self.undocount < self.count:
                        self.buffer_idx = 16

            case 1: # redo
                if self.undocount > 0:
                    if self.buffer_idx < 16:
                        self.skill(self.buffer[self.tail][self.buffer_idx])
                        self.buffer_idx += 1
                        if self.buffer_idx == 16:
                            self.undocount -= 1
                            self.tail = Next(self.tail, 10000)
                            self.buffer_idx = 0
                    return
                if self.segment_idx < self.segment_idx_snapshot:
                    self.skill(self.segment[self.segment_idx])
                    self.segment_idx += 1
                    return

    def sub(self):
        if self.direction in [0, 1]:
            self.direction -= 1
    
    def add(self):
        if self.direction in [-1, 0]:
            self.direction += 1

    def loop(self):
        t = Timer(0.1)
        while True:
            t.start()
            if self.rewind_active:
                self.rewind()
            else:
                self.record(Frame(float3 = (random.random(), random.random(), random.random()), velocity = (random.random(), random.random(), 0)))
            t.wait()

    def clear(self):
        self.tail = 0
        self.count = 0
        self.undocount = 0
        self.buffer_idx = 0
        self.segment_idx = 0

        self.rewind_active = False
        self.direction = 0

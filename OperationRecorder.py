# import threading
import random
# import time

from typing import Any
from dataclasses import dataclass

# from timer import Timer

def Next(ptr, size, step = 1):
    return (ptr + step) % size

def Prev(ptr, size, step = 1):
    return (ptr - step + size) % size

class OperationRecorder:
    def __init__(self, size = 10000):
        self.size = size
        self.buffer = [None] * size
        self.head = 0
        self.tail = 0
        self.count = 0
        self.undocount = 0
    
    def record(self, data: Any):
        if self.undocount > 0:
            self.count -= self.undocount
            self.undocount = 0
        
        self.buffer[self.tail] = data
        
        if self.count < self.size:
            self.count += 1
        else:
            self.head = Next(self.head, self.size)

        self.tail = Next(self.tail, self.size)

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
        self.head = 0
        self.tail = 0
        self.count = 0
        self.undocount = 0

@dataclass
class Frame:
    pose: tuple[float, float, float] # X, Y, Angle
    velocity: tuple[float, float, float] # Vx, Vy, 0

    def __str__(self):
        x, y, a = self.pose
        vx, vy, _ = self.velocity
        return f"pose=({x:.2f},{y:.2f},{a:.2f}) vel=({vx:.2f},{vy:.2f})"
    
    __repr__ = __str__

def generate_random_frame() -> Frame:
    frame = Frame(pose = (random.random(), random.random(), random.random()), velocity = (random.random(), random.random(), 0))
    print(f"Generated frame: {frame}")
    return frame

class Client():
    def __init__(self, capacity = 10000, size = 16):
        self.capacity = capacity
        self.size = size

        self.segments: list[list[Frame]] = [None] * capacity
        self.head = 0
        self.tail = 0
        self.count = 0

        self.seg: list[Frame] = [None] * self.size
        self.seg_idx = 0
        self.seg_snap = 0

        self.timeline_end = 0
        self.timeline_cursor = 0

        self.replay_mode = False
        self.direction = 0

        self.paused = False

    def execute(self, frame: Frame):
        print(f"Execute frame: {frame}")
        self.signal_resume()

    def record(self, data: Frame):
        self.seg[self.seg_idx] = data
        self.seg_idx += 1
        if self.seg_idx == self.size:
            self.segments[self.tail] = self.seg.copy()
            self.tail = Next(self.tail, self.capacity)
            if self.count < self.capacity:
                self.count += 1
            else:
                self.head = Next(self.head, self.capacity)
            self.seg_idx = 0

    def replay(self):
        if not self.replay_mode:
            self.seg_snap = self.seg_idx

            self.timeline_end = self.timeline_cursor = self.count * self.size

            self.replay_mode = True
            self.direction = -1
        else:
            seg_pos, frame_pos = divmod(self.timeline_cursor, self.size)
            if seg_pos < self.count: # seg_idx = 0
                self.count = seg_pos
                self.tail = Next(self.head, self.capacity, self.count)
                if frame_pos > 0:
                    self.seg = self.segments[Next(self.head, self.capacity, seg_pos)].copy()
                    self.seg_idx = frame_pos

            self.replay_mode = False
            self.direction = 0

    def rewind(self):
        match self.direction:
            case 0: # do nothing
                pass
            case -1: # undo
                if self.seg_idx > 0:
                    self.seg_idx -= 1
                    self.execute(self.seg[self.seg_idx])
                    return

                if self.timeline_cursor > 0:
                    self.timeline_cursor -= 1
                    seg_pos, frame_pos = divmod(self.timeline_cursor, self.size)
                    self.execute(self.segments[Next(self.head, self.capacity, seg_pos)][frame_pos])
                    return

            case 1: # redo
                if self.timeline_cursor < self.timeline_end:
                    seg_pos, frame_pos = divmod(self.timeline_cursor, self.size)
                    self.timeline_cursor += 1
                    self.execute(self.segments[Next(self.head, self.capacity, seg_pos)][frame_pos])
                    return

                if self.seg_idx < self.seg_snap:
                    self.seg_idx += 1
                    self.execute(self.seg[self.seg_idx - 1])
                    return

        self.signal_stop()

    def sub(self):
        match self.direction:
            case 0:
                self.direction = -1
                self.signal_resume()
            case 1:
                self.direction = 0
                self.signal_stop()

    def add(self):
        match self.direction:
            case -1:
                self.direction = 0
                self.signal_stop()
            case 0:
                self.direction = 1
                self.signal_resume()

    def clear(self):
        self.head = 0
        self.tail = 0
        self.count = 0

        self.seg_idx = 0

        self.replay_mode = False
        self.direction = 0

    def signal_stop(self):
        if not self.paused:
            print("Signal stop")
            self.paused = True

    def signal_resume(self):
        if self.paused:
            print("Signal resume")
            self.paused = False

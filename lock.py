import threading

_lock = threading.Lock()
released = False

def release_resource():
    global released
    lst = []
    with _lock:
        if released:
            return
        released = True
        for i in range(1000):
            lst.append((i, ))

class A:
    def __init__(self):
        self.self = self
    
    def __del__(self):
        release_resource()

def f():
    A()

f()
release_resource()
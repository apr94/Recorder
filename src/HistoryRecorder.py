import pymouse 
from pymouse import PyMouseEvent
import threading
from threading import Thread
import time


ack = 0
lock1 = threading.Lock()

def changeAck(change):
    global ack
    with lock1:
        ack = change
        time.sleep(0.02)
        
class MouseListener(PyMouseEvent):

    def __init__(self):
        PyMouseEvent.__init__(self)
        self.history = []
            
    def click(self, x, y, button, press):
        if press:
            if (ack == 1):
                print(x, y, button)

ml = MouseListener()

class ThreadedRecorder(Thread):
    
    def __init__(self):
        self.m = pymouse.PyMouse      
        
    def run(self, history):
        Thread(target=ml.run).start()
        while(1):
            if (ack == 1):
                history.append((self.m.position(pymouse.PyMouse()), 0))
                time.sleep(1)
            elif (ack == 2):
                ml.stop()
                break
        
    
        

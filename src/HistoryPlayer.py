import pymouse 
import pykeyboard 
from threading import Thread
import time

class ThreadedPlayer(Thread):
    
    def __init__(self):
        self.m = pymouse.PyMouse
        self.k = pykeyboard.PyKeyboard
        
    def run(self, history):
        for (((x,y),button)) in history:
            self.m.move(pymouse.PyMouse(),x,y)
            if (button > 0):
                self.m.click(pymouse.PyMouse(),x,y,button,1)
            time.sleep(1)
            
    def replicate(self,((x,y),button)):
        curr_x = self.m.position(pymouse.PyMouse())[0]
        curr_y = self.m.position(pymouse.PyMouse())[1]
        while(1):
            curr_x = self.m.position(pymouse.PyMouse())[0]
            curr_y = self.m.position(pymouse.PyMouse())[1]
            dif_x = x - curr_x
            dif_y = y - curr_y
            self.factor = abs(dif_x if abs(dif_x) > abs(dif_y) else dif_y)
            if self.factor is not 0:
                self.rate_y = 5*(dif_y/self.factor)
                self.rate_x = 5*(dif_x/self.factor)
            if (abs(curr_x - x) < 5 and abs(curr_y - y) < 5):
                break
            self.m.move(pymouse.PyMouse(),curr_x+self.rate_x,curr_y+self.rate_y)
        if (button > 0):
            self.m.click(pymouse.PyMouse(),x,y,button,1)
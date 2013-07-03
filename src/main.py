import pymouse 
from pymouse import PyMouseEvent
import pykeyboard 
from pykeyboard import PyKeyboardEvent
import threading
from threading import Thread
import time
import HistoryPlayer

m = pymouse.PyMouse()
k = pykeyboard.PyKeyboard()

ack = 0
lock1 = threading.Lock()

history = []
lock2 = threading.Lock()


def changeAck(change):
    global ack
    with lock1:
        ack = change
        time.sleep(0.02) 

def buildHistory(story):
    global history
    with lock2:
        history.append(story)
        time.sleep(0.02) 


class MouseListener(PyMouseEvent):

    def __init__(self):
        PyMouseEvent.__init__(self)
        self.history = []
            
    def click(self, x, y, button, press):
        if ack == 1:
            if press:
                print(x, y, button)
                buildHistory((x,y,button))

m = MouseListener()
         
class KeyBoardListener(PyKeyboardEvent):
    
    def startRecording(self):
        if ack != 1:
            changeAck(1)
            print("Recording")
    
    def endRecording(self):
        if ack == 1:
            changeAck(2)
            print("Stopping Recording")
    
    def quitProgram(self):
        print("Quitting")
        self.stop()
        m.stop()
        
    
    def printHistory(self):
        print(history)
        
    def playHistory(self):
        Thread(target=self.player.run(history)).start()
        

    def __init__(self):
        PyKeyboardEvent.__init__(self)
        self.player = HistoryPlayer.ThreadedPlayer()
        self.commands = {'24': self.quitProgram,
                         '26': self.endRecording,
                         '33': self.playHistory,
                         '39': self.startRecording, 
                         '43': self.printHistory
                         }

    def _key_press(self, keycode):
        print(keycode)
        if str(keycode) in self.commands:
            self.commands[str(keycode)]()
            

c = KeyBoardListener()

if __name__ == '__main__':
    try:
        Thread(target=c.run).start()
        Thread(target=m.run).start()  
    except Exception as err:
        print (err) 
import pykeyboard 
from pykeyboard import PyKeyboardEvent
from threading import Thread
import HistoryPlayer
import HistoryRecorder

k = pykeyboard.PyKeyboard()

history = []

class KeyBoardListener(PyKeyboardEvent):
    
    def startRecording(self):
        if self.ack != 1:
            print("Recording")
            HistoryRecorder.changeAck(1)
            self.ack = 1
            
    
    def endRecording(self):
        if self.ack == 1:
            print("Stopping Recording")
            HistoryRecorder.changeAck(3)
            self.ack = 3
            
    
    def quitProgram(self):
        print("Quitting")
        HistoryRecorder.changeAck(2)
        self.ack = 2
        self.stop()
        
    
    def printHistory(self):
        print(history)
        
    def playHistory(self):
        Thread(target=self.player.run(history)).start()
        

    def __init__(self):
        PyKeyboardEvent.__init__(self)
        self.ack = 0
        self.player = HistoryPlayer.ThreadedPlayer()
        self.recorder = HistoryRecorder.ThreadedRecorder()
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
        Thread(target=c.recorder.run(history)).start()
    except Exception as err:
        print (err) 
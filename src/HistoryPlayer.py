import pymouse 
from pymouse import PyMouseEvent
import pykeyboard 
from pykeyboard import PyKeyboardEvent
import threading
from threading import Thread
import time


class ThreadedPlayer(Thread):
    def run(self, history):
        for x in history:
            print x
            time.sleep(1)
            
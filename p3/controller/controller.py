from model import Board
import threading
import time

class GolController:
    def __init__(self, model: Board, refreshFun, updateSpeed):
        self._model = model
        self._refreshFun = refreshFun
        self._updateSpeed = updateSpeed
        self._killThread = False
        self._updateThread = threading.Thread(target=self.updateFun, args=(self._updateSpeed,))
        self.updaing = False

    def swapField(self, field):
        self._model.swap_field(field)
        self._refreshFun()

    def nextGen(self):
        self._model.next_gen()
        self._refreshFun()

    def resetBoard(self):
        self._model.reset_board()
        self._refreshFun()

    def startUpdating(self):
        if self.updaing:
            self._killThread = True
            self._updateThread.join()
            self._killThread = False
        interval = 3.0 / self._updateSpeed
        self._updateThread = threading.Thread(target=self.updateFun, args=(interval,))
        self._updateThread.start()
        self.updaing = True

    def stopUpdating(self):
        if self._updateSpeed is not None and self._updateThread.is_alive():
            self._killThread = True
            self._updateThread.join()
            self._killThread = False
        self.updaing = False

    def updateFun(self, interval):
        while(not self._killThread):
            self.controlledSleep(interval)
            self._model.next_gen()
            self._refreshFun()

    def controlledSleep(self, interval):
        sum = 0.0
        while(sum < interval):
            time.sleep(0.1)
            if(self._killThread):
                return
            sum += 0.1

    def speedChanged(self, newSpeed):
        self._updateSpeed = newSpeed
        if self.updaing:
            self.stopUpdating()
            self.startUpdating()
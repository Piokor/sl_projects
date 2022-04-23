from model import Board
from pyqt import GofWindow
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    board = Board((35, 35))
    win = GofWindow(board)
    win.show()
    sys.exit(app.exec_())
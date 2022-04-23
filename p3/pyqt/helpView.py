from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QWidget, QPushButton, QVBoxLayout, QSlider, QLabel, QMenu, QAction
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QBrush, QColor, QMouseEvent


class HelpWindow(QMainWindow):

    def __init__(self, parent=None):
        super(HelpWindow, self).__init__(parent)
        self.setGeometry(220, 70, 100, 80)
        self.setWindowTitle('Gra w życie - pomoc')
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._generalLayout = QVBoxLayout()
        self._centralWidget.setLayout(self._generalLayout)
        self._generalLayout.addWidget(QLabel('Wciśnij na komórkę aby zmienić jej stan.\nWciśnij przycisk "Start", aby rozpocząć automatyczną symulację, której prędkość można zmienić suwakiem.\nWciśnij przycisk "Następna", aby wyświetlić kolejną epokę.\nWciśnij przycisk "Reset", aby zresetować stan tablicy"))'))
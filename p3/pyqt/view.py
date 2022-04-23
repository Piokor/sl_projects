from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QWidget, QPushButton, QVBoxLayout, QSlider, QLabel, QMenu, QAction
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QBrush, QColor, QMouseEvent

from model import Board
from controller.controller import GolController
from pyqt.helpView import HelpWindow

class GofWindow(QMainWindow):

    def __init__(self, gameoflife: Board):
        super().__init__()
        self._model = gameoflife
        self._setupConsts()
        self._controller = GolController(gameoflife, self.update, self.INITIAL_SPEED)
        self._setupWindow()
        self._createMenu()
        self._createGeneralLayout()
        self._createTopForm()
        self._createBoard()
        self._start = False
        self._bordersPainted = False
        self._dialogs = list()

    def _setupConsts(self):
        self.BOARD_SIZE = self._model.get_size()
        self.CELL_SIZE = 22
        self.BORDER_SIZE = 2
        self.PADDING_TOP = 40
        self.PADDING = 30
        self.WINDOW_SIZE = (
            self.BOARD_SIZE[0] * (self.CELL_SIZE + self.BORDER_SIZE) + self.BORDER_SIZE + 2 * self.PADDING,
            self.BOARD_SIZE[1] * (self.CELL_SIZE + self.BORDER_SIZE) + self.BORDER_SIZE + 2 * self.PADDING + self.PADDING_TOP)
        self.BOARD_SIZE_P = (
            self.BOARD_SIZE[0] * (self.CELL_SIZE + self.BORDER_SIZE) + self.BORDER_SIZE,
            self.BOARD_SIZE[1] * (self.CELL_SIZE + self.BORDER_SIZE) + self.BORDER_SIZE)
        self.BOARD_START_POINT = (self.PADDING, self.PADDING + self.PADDING_TOP)
        self.BOARD_END_POINT = (self.WINDOW_SIZE[0] - self.PADDING, self.WINDOW_SIZE[1] - self.PADDING)
        self.BORDER_COLOR = QColor(30, 30, 30)
        self.EMPTY_COLOR = QColor(255, 255, 255)
        self.FILL_COLOR = QColor(70, 70, 70)
        self.INITIAL_SPEED = 10

    def _setupWindow(self):
        self.setGeometry(200, 50, *self.WINDOW_SIZE)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowTitle('Gra w życie')

    def _createMenu(self):
        help = self.menuBar().addMenu("&Pomoc")
        ac = help.addAction("Pokaż pomoc")
        ac.triggered.connect(self._elo)

    def _elo(self):
        hw = HelpWindow()
        self._dialogs.append(hw)
        hw.show()

    def _createGeneralLayout(self):
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._generalLayout = QVBoxLayout()
        self._centralWidget.setLayout(self._generalLayout)

    def _createTopForm(self):        
        self.formLayout = QHBoxLayout()
        self.form = {}
        self._createTopSlider()
        self.form["buttons"] = {
            "startStop": QPushButton('Start'),
            "next": QPushButton('Następna'),
            "reset": QPushButton('Reset')
        }
        for _, btn in self.form["buttons"].items():
            self.formLayout.addWidget(btn)
        self._generalLayout.addLayout(self.formLayout)      
        self._bindEvents()

    def _createTopSlider(self):
        label = QLabel('Prędkość: ')
        self.formLayout.addWidget(label)
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(1)
        slider.setMaximum(60)
        slider.setValue(self.INITIAL_SPEED)
        slider.setTickInterval(3)
        slider.valueChanged.connect(lambda: self._controller.speedChanged(slider.value()))
        self.form["slider"] = slider
        self.formLayout.addWidget(slider)

    def _bindEvents(self):
        self.form["buttons"]["next"].clicked.connect(self._controller.nextGen)
        self.form["buttons"]["reset"].clicked.connect(self._controller.resetBoard)
        self.form["buttons"]["startStop"].clicked.connect(self.startStop)

    def _createBoard(self):        
        self._boardLayout = QHBoxLayout()
        self._boardWidget = QWidget(self._centralWidget)
        self._boardLayout.addWidget(self._boardWidget)
        self._generalLayout.addLayout(self._boardLayout)          

    def paintEvent(self, e):
        if not self._bordersPainted:
            qp = QPainter(self)
            qp.setPen(self.EMPTY_COLOR)
            br = QBrush(self.EMPTY_COLOR)  
            qp.setBrush(br)   
            qp.drawRect(QRect(QPoint(*self.BOARD_START_POINT), QPoint(*self.BOARD_END_POINT)))
            qp.end()
            self._bordersPainted = True
        self._drawBorders()
        self._drawCells()

    def _drawCells(self):
        board = self._model.get_board()
        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                self._drawCell(cell, x, y)

    def _drawCell(self, state, x, y):
        color = self.FILL_COLOR if state else self.EMPTY_COLOR
        qp = QPainter(self)
        qp.setPen(color)
        br = QBrush(color) 
        qp.setBrush(br)   
        qp.drawRect(QRect(
            QPoint(
                self.BOARD_START_POINT[0] + (self.BORDER_SIZE) + x * (self.BORDER_SIZE + self.CELL_SIZE ),
                self.BOARD_START_POINT[1] + (self.BORDER_SIZE) + y * (self.BORDER_SIZE + self.CELL_SIZE ),
            ),
            QPoint(
                self.BOARD_START_POINT[0] + (self.BORDER_SIZE) + x * (self.BORDER_SIZE + self.CELL_SIZE) + self.CELL_SIZE - 2,
                self.BOARD_START_POINT[1] + (self.BORDER_SIZE) + y * (self.BORDER_SIZE + self.CELL_SIZE) + self.CELL_SIZE - 2,
            )
        ))
        qp.end()


    def _drawBorders(self):
        qp = QPainter(self)
        qp.setPen(self.BORDER_COLOR)
        br = QBrush(self.BORDER_COLOR) 
        qp.setBrush(br)   
        for i in range(self.BOARD_SIZE[0]):
            startPoint = QPoint(
                self.BOARD_START_POINT[0] + i * (self.BORDER_SIZE + self.CELL_SIZE),
                self.BOARD_START_POINT[1]
            )            
            endPoint = QPoint(
                self.BOARD_START_POINT[0] + int(2*self.BORDER_SIZE/3) + i * (self.BORDER_SIZE + self.CELL_SIZE),
                self.BOARD_END_POINT[1] - int(self.BORDER_SIZE/2)
            )
            line = QRect(startPoint, endPoint)
            qp.drawRect(line)

        for i in range(self.BOARD_SIZE[1]):
            startPoint = QPoint(
                self.BOARD_START_POINT[0],
                self.BOARD_START_POINT[1] + i * (self.BORDER_SIZE + self.CELL_SIZE),
            )            
            endPoint = QPoint(
                self.BOARD_END_POINT[0] - int(self.BORDER_SIZE/2),
                self.BOARD_START_POINT[1] + int(2*self.BORDER_SIZE/3) + i * (self.BORDER_SIZE + self.CELL_SIZE),
            )
            line = QRect(startPoint, endPoint)
            qp.drawRect(line)
        
        startPoint = QPoint(
            self.BOARD_START_POINT[0],
            self.BOARD_END_POINT[1] - int(self.BORDER_SIZE),
        )            
        endPoint = QPoint(
            self.BOARD_END_POINT[0] - int(self.BORDER_SIZE/2),
            self.BOARD_END_POINT[1] - int(self.BORDER_SIZE/2)
        )
        line = QRect(startPoint, endPoint)
        qp.drawRect(line)
        
        startPoint = QPoint(
            self.BOARD_END_POINT[0] - int(self.BORDER_SIZE),
            self.BOARD_START_POINT[1]
        )            
        endPoint = QPoint(
            self.BOARD_END_POINT[0] - int(self.BORDER_SIZE/2),
            self.BOARD_END_POINT[1] - int(self.BORDER_SIZE/2)
        )
        line = QRect(startPoint, endPoint)
        qp.drawRect(line)
        qp.end()

    def cordsToCell(self, cords):
        if cords[0] < self.BOARD_START_POINT[0] or cords[1] < self.BOARD_START_POINT[1] or \
           cords[0] > self.BOARD_END_POINT[0] or cords[1] > self.BOARD_END_POINT[1]:
           return None
        x = int((cords[0] - self.PADDING) / (self.BORDER_SIZE + self.CELL_SIZE))
        y = int((cords[1] - self.PADDING - self.PADDING_TOP) / (self.BORDER_SIZE + self.CELL_SIZE))
        return x, y
    
    def mousePressEvent(self, event: QMouseEvent):
        cords = (event.x(), event.y())
        cell = self.cordsToCell(cords)
        if cell is not None:
            self._controller.swapField(cell)

    def startStop(self):
        if self._start:
            self._controller.stopUpdating()
            self.form["buttons"]["startStop"].setText("Start")
        else:
            self._controller.startUpdating()
            self.form["buttons"]["startStop"].setText("Stop")
        self._start = not self._start

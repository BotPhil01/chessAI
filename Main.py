import MovePredictor
from MovePredictor import next_move
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot
import chess
import chess.svg
import time

from RegularBot import RegularBot
from PositionBot import PositionBot
from FirstBot import FirstBot
from LastBot import LastBot
class MainWindow(QWidget):

    # function for running the main loop of the game
    # requries selection to be done first
    @pyqtSlot()
    def run_loop(self, bengine, wengine):
        while not self.chessboard.is_game_over():
            if self.chessboard.turn == chess.WHITE:
                self.chessboard.push(MovePredictor.next_move(self.chessboard, wengine))
            else:
                self.chessboard.push(MovePredictor.next_move(self.chessboard, bengine))
            self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
            self.widgetSvg.load(self.chessboardSvg)
            QApplication.processEvents()

        print(f"Game finished between white: {wengine} and black: {bengine}")
        print(f"outcome: {self.chessboard.outcome()}")


    @pyqtSlot()
    def reset(self):
        self.chessboard = chess.Board()
        self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 1920, 1080)

        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(10, 10, 1000, 1000)

        self.chessboard = chess.Board()
        self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

        self.black = FirstBot()
        self.white = LastBot()

        self.button = QPushButton("Start loop", self)
        self.button.setGeometry(1500, 10, 100, 100)
        self.button.clicked.connect(lambda: self.run_loop(self.black, self.white))

        self.button2 = QPushButton("Reset", self)
        self.button2.setGeometry(1500, 200, 100, 100)
        self.button2.clicked.connect(self.reset)

        self.quitbutton = QPushButton("Quit", self)
        self.quitbutton.setGeometry(1720, 880, 100, 100)
        self.quitbutton.clicked.connect(quit)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
    print("executed")

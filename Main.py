import MovePredictor
from MovePredictor import next_move
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot
import chess
import chess.svg
import time

class MainWindow(QWidget):

    @pyqtSlot()
    def run_loop(self):
        while not self.chessboard.is_game_over():
            print("loop running")
            self.chessboard.push(MovePredictor.next_move(self.chessboard))
            self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
            self.widgetSvg.load(self.chessboardSvg)
            print("Updating")
            QApplication.processEvents()
            print("Updated")
            time.sleep(1)

    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 1920, 1080)

        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(10, 10, 1000, 1000)

        self.chessboard = chess.Board()
        self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

        self.button = QPushButton("Start loop", self)
        self.button.setGeometry(1500, 10, 100, 100)
        self.button.clicked.connect(self.run_loop)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
    print("executed")
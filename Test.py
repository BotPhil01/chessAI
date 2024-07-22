import chess
import MoveSelection
import BoardEvaluation
import chess.svg as svg
from time import sleep
import sys
import subprocess
print("Welcome to pychess")
print("Game will start on your input")
y = input()
b = chess.Board()
while not b.is_game_over():
    boardsvg = svg.board(b, size=600, coordinates=True)
    with open('temp.svg', 'w') as outputfile:
        outputfile.write(boardsvg)
    sleep(0.1)
    opener = "xdg-open"
    subprocess.call([opener, "temp.svg"])
    sleep(0.5)
    subprocess.call(["fuser", "-k", "-TERM", "temp.svg"])


    b.push(MoveSelection.next_move(b))
print("Game over!!!")
if b.outcome().winner == chess.WHITE:
    print("White wins!")
elif b.outcome().winner == chess.BLACK:
    print("Black wins!")
else:
    print("Draw!")

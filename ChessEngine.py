## Name - ChessEngine.py
## Purpose - Class is responsible for storing information about the state of a chess game and valid moves
## Author - Ryan Brosius
## Date - 6/21/2022

class GameState():
    def __init__(self):
        #8x8 2D list
        #bR --> Black Rook
        #bN --> Black Knight
        #bB --> Black Bishop
        #bQ --> Black Queen
        #bK --> Black King
        #bP --> Black Pawn
        #-- --> Empty Space
        self.__board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.__whiteToMove = True
        self.__moveLog = []

    def getBoard(self):
        return self.__board
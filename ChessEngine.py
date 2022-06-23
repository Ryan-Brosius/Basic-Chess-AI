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

    def makeMove(self, move):
        self.__board[move.getStartSq()[0]][move.getStartSq()[1]] = "--"
        self.__board[move.getEndSq()[0]][move.getEndSq()[1]] = move.getPieceMoved()
        self.__moveLog.append(move)
        self.__whiteToMove = not self.__whiteToMove

class Move():

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.__startRow = startSq[0]
        self.__startCol = startSq[1]
        self.__endRow = endSq[0]
        self.__endCol = endSq[1]
        self.__pieceMoved = board[self.__startRow][self.__startCol]
        self.__pieceCaptured = board[self.__endRow][self.__endCol]

    def getStartSq(self):
        return (self.__startRow, self.__startCol)

    def getEndSq(self):
        return (self.__endRow, self.__endCol)

    def getPieceMoved(self):
        return self.__pieceMoved

    def getChessNotation(self):
        return self.getRankFile(self.__startRow, self.__startCol) + self.getRankFile(self.__endRow, self.__endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
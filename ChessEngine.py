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

    def getMoveLog(self):
        return self.__moveLog

    def getWhiteToMove(self):
        return self.__whiteToMove

    def makeMove(self, move):
        self.__board[move.getStartSq()[0]][move.getStartSq()[1]] = "--"
        self.__board[move.getEndSq()[0]][move.getEndSq()[1]] = move.getPieceMoved()
        self.__moveLog.append(move)
        self.__whiteToMove = not self.__whiteToMove

    def undoMove(self):
        if len(self.getMoveLog()) > 0:
            move = self.__moveLog.pop()
            self.__board[move.getStartSq()[0]][move.getStartSq()[1]] = move.getPieceMoved()
            self.__board[move.getEndSq()[0]][move.getEndSq()[1]] = move.getPieceCaptured()
            self.__whiteToMove = not self.__whiteToMove

    def getValidMoves(self):    #All moves when in check
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):  #All moves in general
        moves = []
        for row in range(len(self.getBoard())):
            for col in range(len(self.getBoard()[row])):
                turn = self.getBoard()[row][col][0]
                if (turn == "w" and self.__whiteToMove) or (turn == "b" and not self.__whiteToMove):
                    piece = self.__board[row][col][1]
                    if piece == "P":
                        self.getPawnMoves(row, col, moves)
                    elif piece == "R":
                        self.getRookMoves(row, col, moves)
        return moves

    def getPawnMoves(self, row, col, moves):    #Gets all of the valid pawn moves
        if self.__whiteToMove and row >= 1:  #White pawn moves (SIDE NOTE: DOESNT CALCULATE ON ROW 0)
            if self.__board[row-1][col] == "--":    #Square above is empty
                moves.append(Move((row, col), (row-1, col), self.__board))
                if row == 6 and self.__board[row-2][col] == "--":   #On starting rank, and 2 squares above is empty
                    moves.append(Move((row, col), (row-2, col), self.__board))
            if col-1 >= 0:  #Checks to capture a piece from the left
                if self.__board[row-1][col-1][0] == "b":
                    moves.append(Move((row, col), (row-1, col-1), self.__board))
            if col+1 <= 7:  #Checks to capture a piece from the right
                if self.__board[row-1][col+1][0] == "b":
                    moves.append(Move((row, col), (row-1, col+1), self.__board))

        elif not self.__whiteToMove and row <= 6:   #black pawn moves (SIDE NOTE: DOESNT CALCULATE ON ROW 7)
            if self.__board[row+1][col] == "--": #Square below is empty
                moves.append(Move((row, col), (row+1, col), self.__board))
                if row == 1 and self.__board[row+2][col] == "--":   #On starting rank, and 2 squares below is empty
                    moves.append(Move((row, col), (row+2, col), self.__board))
            if col-1 >= 0:  #checks to capture a piece from the left
                if self.__board[row+1][col-1][0] == "w":
                    moves.append(Move((row, col), (row+1, col-1), self.__board))
            if col+1 <= 7:  #Checks to capture a piece from the right
                if self.__board[row+1][col+1][0] == "w":
                    moves.append(Move((row, col), (row+1, col+1), self.__board))

    def getRookMoves(self, row, col, moves):    #Gets all of the valid rook moves
        pass



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
        self.__moveID = self.__startRow * 1000 + self.__startCol * 100 + self.__endRow * 10 + self.__endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.__moveID == other.__moveID
        return False

    def getStartSq(self):
        return (self.__startRow, self.__startCol)

    def getEndSq(self):
        return (self.__endRow, self.__endCol)

    def getPieceMoved(self):
        return self.__pieceMoved

    def getPieceCaptured(self):
        return self.__pieceCaptured

    def getChessNotation(self):
        return self.getRankFile(self.__startRow, self.__startCol) + self.getRankFile(self.__endRow, self.__endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
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
        self.__whiteKingLocation = (7, 4)
        self.__blackKingLocation = (0, 4)
        self.__checkMate = False
        self.__staleMate = False
        self.__enpassantPossible = () #cords for enpassant square
        self.__currentCastlingRight = castleRights(True, True, True, True)
        self.__castleRightsLog = [castleRights(self.__currentCastlingRight.wks, self.__currentCastlingRight.bks,
                                               self.__currentCastlingRight.wqs, self.__currentCastlingRight.bqs)]

    def getBoard(self):
        return self.__board

    def getMoveLog(self):
        return self.__moveLog

    def getWhiteToMove(self):
        return self.__whiteToMove

    def getCheckMate(self):
        return self.__checkMate

    def getStaleMate(self):
        return self.__staleMate

    def makeMove(self, move):
        self.__board[move.getStartSq()[0]][move.getStartSq()[1]] = "--"
        self.__board[move.getEndSq()[0]][move.getEndSq()[1]] = move.getPieceMoved()
        self.__moveLog.append(move)
        self.__whiteToMove = not self.__whiteToMove
        if move.getPieceMoved() == "wK":
            self.__whiteKingLocation = move.getEndSq()
        elif move.getPieceMoved() == "bK":
            self.__blackKingLocation = move.getEndSq()

        #Pawn promotion
        if move.isPawnPromotion():
            self.__board[move.getEndSq()[0]][move.getEndSq()[1]] = move.getPieceMoved()[0] + "Q"

        #Enpassant move
        if move.isEnpassantMove():
            self.__board[move.getStartSq()[0]][move.getEndSq()[1]] = "--"
        if move.getPieceMoved()[1] == "P" and abs(move.getStartSq()[0] - move.getEndSq()[0]) == 2:
            self.__enpassantPossible = ((move.getStartSq()[0] + move.getEndSq()[0])//2, move.getStartSq()[1])
        else:
            self.__enpassantPossible = ()

        #Castle move
        if move.isCastleMove():
            if move.getEndSq()[1] - move.getStartSq()[1] == 2: #King Side
                self.__board[move.getEndSq()[0]][move.getEndSq()[1]-1] = self.__board[move.getEndSq()[0]][move.getEndSq()[1]+1]
                self.__board[move.getEndSq()[0]][move.getEndSq()[1]+1] = "--"
            else: #Queen Side
                self.__board[move.getEndSq()[0]][move.getEndSq()[1]+1] = self.__board[move.getEndSq()[0]][move.getEndSq()[1]-2]
                self.__board[move.getEndSq()[0]][move.getEndSq()[1]-2] = "--"



        #Castling
        self.updateCastleRights(move)
        self.__castleRightsLog.append(castleRights(self.__currentCastlingRight.wks, self.__currentCastlingRight.bks,
                                               self.__currentCastlingRight.wqs, self.__currentCastlingRight.bqs))



    def undoMove(self):
        if len(self.getMoveLog()) > 0:
            move = self.__moveLog.pop()
            self.__board[move.getStartSq()[0]][move.getStartSq()[1]] = move.getPieceMoved()
            self.__board[move.getEndSq()[0]][move.getEndSq()[1]] = move.getPieceCaptured()
            self.__whiteToMove = not self.__whiteToMove
            if move.getPieceMoved() == "wK":
                self.__whiteKingLocation = move.getStartSq()
            elif move.getPieceMoved() == "bK":
                self.__blackKingLocation = move.getStartSq()
            if move.isEnpassantMove():
                self.__board[move.getEndSq()[0]][move.getEndSq()[1]] = "--"
                self.__board[move.getStartSq()[0]][move.getEndSq()[1]] = move.getPieceCaptured()
                self.__enpassantPossible = (move.getEndSq()[0], move.getEndSq()[1])
            if move.getPieceMoved()[1] == "P" and abs(move.getStartSq()[0] - move.getEndSq()[0]) == 2:
                self.__enpassantPossible = ()
            self.__castleRightsLog.pop()
            newRights = self.__castleRightsLog[-1]
            self.__currentCastlingRight = castleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
            if move.isCastleMove():
                if move.getEndSq()[1] - move.getStartSq()[1] == 2:
                    self.__board[move.getEndSq()[0]][move.getEndSq()[1]+1] = self.__board[move.getEndSq()[0]][move.getEndSq()[1]-1]
                    self.__board[move.getEndSq()[0]][move.getEndSq()[1]-1] = "--"
                else:
                    self.__board[move.getEndSq()[0]][move.getEndSq()[1]-2] = self.__board[move.getEndSq()[0]][move.getEndSq()[1]+1]
                    self.__board[move.getEndSq()[0]][move.getEndSq()[1]+1] = "--"
            self.__checkMate = False
            self.__staleMate = False


    def updateCastleRights(self, move):
        if move.getPieceMoved() == "wK":
            self.__currentCastlingRight.wks = False
            self.__currentCastlingRight.wqs = False
        elif move.getPieceMoved() == "bK":
            self.__currentCastlingRight.bks = False
            self.__currentCastlingRight.bqs = False
        elif move.getPieceMoved() == "wR" and move.getStartSq() == (7,0):
            self.__currentCastlingRight.wqs = False
        elif move.getPieceMoved() == "wR" and move.getStartSq() == (7,7):
            self.__currentCastlingRight.wks = False
        elif move.getPieceMoved() == "bR" and move.getStartSq() == (0,7):
            self.__currentCastlingRight.bks = False

    def getValidMoves(self):    #All moves when in check
        tempEnpassantPossible = self.__enpassantPossible
        tempCastleRights = castleRights(self.__currentCastlingRight.wks, self.__currentCastlingRight.bks,
                                            self.__currentCastlingRight.wqs, self.__currentCastlingRight.bqs)
        moves = self.getAllPossibleMoves()
        if self.__whiteToMove:
            self.getCastleMoves(self.__whiteKingLocation[0], self.__whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.__blackKingLocation[0], self.__blackKingLocation[1], moves)

        for i in range(len(moves)-1, -1, -1):   #Removes invalid moves that would lead to checkmate
            self.makeMove(moves[i])
            self.__whiteToMove = not self.__whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.__whiteToMove = not self.__whiteToMove
            self.undoMove()

        if len(moves) == 0: #Checkmate or stalemate
            if self.inCheck():
                self.__checkMate = True
            else:
                self.__staleMate = True
        else:
            self.__checkMate = False
            self.__staleMate = False

        self.__enpassantPossible = tempEnpassantPossible
        self.__currentCastlingRight = tempCastleRights
        return moves

    def inCheck(self):  #Determine if the player is in check
        if self.__whiteToMove:
            return self.squareUnderAttack(self.__whiteKingLocation[0], self.__whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.__blackKingLocation[0], self.__blackKingLocation[1])

    def squareUnderAttack(self, row, col):  #Determine if enemy can attack the square (row, col)
        self.__whiteToMove = not self.__whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.__whiteToMove = not self.__whiteToMove
        for move in oppMoves:
            if move.getEndSq()[0] == row and move.getEndSq()[1] == col:
                return True
        return False

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
                    elif piece == "N":
                        self.getKnightMoves(row, col, moves)
                    elif piece == "B":
                        self.getBishopMoves(row, col, moves)
                    elif piece == "Q":  #Queen uses bishop and rook moves
                        self.getBishopMoves(row, col, moves)
                        self.getRookMoves(row, col, moves)
                    elif piece == "K":
                        self.getKingMoves(row, col, moves)
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
                elif (row-1, col-1) == self.__enpassantPossible:
                    moves.append(Move((row, col), (row-1, col-1), self.__board, isEnpassantMove=True))
            if col+1 <= 7:  #Checks to capture a piece from the right
                if self.__board[row-1][col+1][0] == "b":
                    moves.append(Move((row, col), (row-1, col+1), self.__board))
                elif (row-1, col+1) == self.__enpassantPossible:
                    moves.append(Move((row, col), (row-1, col+1), self.__board, isEnpassantMove=True))

        elif not self.__whiteToMove and row <= 6:   #black pawn moves (SIDE NOTE: DOESNT CALCULATE ON ROW 7)
            if self.__board[row+1][col] == "--": #Square below is empty
                moves.append(Move((row, col), (row+1, col), self.__board))
                if row == 1 and self.__board[row+2][col] == "--":   #On starting rank, and 2 squares below is empty
                    moves.append(Move((row, col), (row+2, col), self.__board))
            if col-1 >= 0:  #checks to capture a piece from the left
                if self.__board[row+1][col-1][0] == "w":
                    moves.append(Move((row, col), (row+1, col-1), self.__board))
                elif (row+1, col-1) == self.__enpassantPossible:
                    moves.append(Move((row, col), (row+1, col-1), self.__board, isEnpassantMove=True))
            if col+1 <= 7:  #Checks to capture a piece from the right
                if self.__board[row+1][col+1][0] == "w":
                    moves.append(Move((row, col), (row+1, col+1), self.__board))
                elif (row+1, col+1) == self.__enpassantPossible:
                    moves.append(Move((row, col), (row+1, col+1), self.__board, isEnpassantMove=True))

    def getRookMoves(self, row, col, moves):    #Gets all of the valid rook moves
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.__whiteToMove else "w"

        for d in directions:
            for i in range(1,8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.__board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((row,col), (endRow,endCol), self.__board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((row,col), (endRow,endCol), self.__board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, row, col, moves):
        rowNums = [1, 2, 2, 1, -1, -2, -2, -1]
        colNums = [-2, -1, 1, 2, -2, -1, 1, 2]
        allyColor = "w" if self.__whiteToMove else "b"
        for i in range(8):
                try:
                    if self.__board[row-rowNums[i]][col-colNums[i]][0] != allyColor and row-rowNums[i] >= 0 and col-colNums[i] >= 0:
                        moves.append(Move((row, col), (row-rowNums[i], col-colNums[i]), self.__board))
                except: 
                    pass
    
    def getBishopMoves(self, row, col, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.__whiteToMove else "w"

        for d in directions:
            for i in range(1,8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.__board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((row,col), (endRow,endCol), self.__board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((row,col), (endRow,endCol), self.__board))
                        break
                    else:
                        break
                else:
                    break

    

    
    def getKingMoves(self, row, col, moves):
        rowNums = [1,1,1,0,0,-1,-1,-1]
        colNums = [-1,0,1,-1,1,-1,0,1]
        allyColor = "w" if self.__whiteToMove else "b"
        for i in range(8):
                try:
                    if self.__board[row-rowNums[i]][col-colNums[i]][0] != allyColor and row-rowNums[i] >= 0 and col-colNums[i] >= 0:
                        moves.append(Move((row, col), (row-rowNums[i], col-colNums[i]), self.__board))
                except: 
                     pass

    def getCastleMoves(self, row, col, moves):
        if self.squareUnderAttack(row,col):
            return
        if (self.__whiteToMove and self.__currentCastlingRight.wks) or (not self.__whiteToMove and self.__currentCastlingRight.bks):
            self.getKingSideCastleMoves(row,col,moves)
        if (self.__whiteToMove and self.__currentCastlingRight.wqs) or (not self.__whiteToMove and self.__currentCastlingRight.bqs):
            self.getQueenSideCastleMoves(row,col,moves)
        
    def getKingSideCastleMoves(self, row, col, moves):
        if self.__board[row][col+1] == "--" and self.__board[row][col+2] == "--":
            if not self.squareUnderAttack(row, col+1) and not self.squareUnderAttack(row, col+2):
                moves.append(Move((row, col), (row, col+2), self.__board, isCastleMove=True))

    def getQueenSideCastleMoves(self, row, col, moves):
        if self.__board[row][col-1] == "--" and self.__board[row][col-2] == "--" and self.__board[row][col-3] == "--":
            if not self.squareUnderAttack(row, col-1) and not self.squareUnderAttack(row, col-2) and not self.squareUnderAttack(row, col-3):
                moves.append(Move((row, col), (row, col-2), self.__board, isCastleMove=True))

class castleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
    def __str__(self):
        return "WKS:" + str(self.wks) + " " + "WQS:" + str(self.wqs) + " " + "BKS:" + str(self.bks) + " " + "BQS:" + str(self.bqs)


class Move():

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):
        self.__startRow = startSq[0]
        self.__startCol = startSq[1]
        self.__endRow = endSq[0]
        self.__endCol = endSq[1]
        self.__pieceMoved = board[self.__startRow][self.__startCol]
        self.__pieceCaptured = board[self.__endRow][self.__endCol]
        self.__isPawnPromotion = (self.__pieceMoved == "wP" and self.getEndSq()[0] == 0) or (self.__pieceMoved == "bP" and self.getEndSq()[0] == 7)
        self.__isEnpassantMove = isEnpassantMove
        if self.__isEnpassantMove:
            self.__pieceCaptured = "wP" if self.__pieceCaptured == "bP" else "bP"
        self.__isCastleMove = isCastleMove
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

    def isPawnPromotion(self):
        return self.__isPawnPromotion

    def isEnpassantMove(self):
        return self.__isEnpassantMove

    def isCastleMove(self):
        return self.__isCastleMove

    def getChessNotation(self):
        return self.getRankFile(self.__startRow, self.__startCol) + self.getRankFile(self.__endRow, self.__endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
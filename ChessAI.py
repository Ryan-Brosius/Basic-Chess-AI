## Name - ChessAI.py
## Purpose - To calculate chess moves using various algorthms
## Author - Ryan Brosius
## Date - 9/1/2022

import random

pieceScores ={"K": 0,
              "Q": 10,
              "R": 5,
              "B": 3,
              "N": 3,
              "P": 1}
CHECKMATE = 1000
STALEMATE = 0

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.getWhiteToMove() else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentMoves = gs.getValidMoves()
        opponentMaxScore = -CHECKMATE
        for opponentMove in opponentMoves:
            gs.makeMove(opponentMove)
            if gs.getCheckMate():
                score = -turnMultiplier * CHECKMATE
            elif gs.getStaleMate():
                score = STALEMATE
            else:
                score = -turnMultiplier * scoreMaterial(gs.getBoard())
            if score > opponentMaxScore:
                opponentMaxScore = score
            gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove

# Score the board on material
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += pieceScores[square[1]]
            elif square[0] =="b":
                score -= pieceScores[square[1]]
    return score
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
DEPTH = 3

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMoveMinMax(gs, validMoves):
    turnMultiplier = 1 if gs.getWhiteToMove() else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentMoves = gs.getValidMoves()
        if gs.getCheckMate():
            opponentMaxScore = -CHECKMATE
        elif gs.getStaleMate():
            opponentMaxScore = STALEMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentMove in opponentMoves:
                gs.makeMove(opponentMove)
                gs.getValidMoves()
                if gs.getCheckMate():
                    score = CHECKMATE
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

def findBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    #findMoveMinMax(gs, validMoves, DEPTH, gs.getWhiteToMove())
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.getWhiteToMove() else -1)
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.getBoard())

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

def scoreBoard(gs):
    if gs.getCheckMate():
        if gs.getWhiteToMove():
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.getStaleMate():
        return STALEMATE

    score = 0
    for row in gs.getBoard():
        for square in row:
            if square[0] == "w":
                score += pieceScores[square[1]]
            elif square[0] =="b":
                score -= pieceScores[square[1]]
    return score

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
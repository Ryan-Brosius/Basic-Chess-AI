## Name - ChessMain.py
## Purpose - Main driver file, responsible for user input and displaying information
## Author - Ryan Brosius
## Date - 6/21/2022

import pygame as p
from ChessEngine import GameState, Move

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

#UI Elements
UI_SQUARE_HIGHLIGHT = p.Surface((SQ_SIZE, SQ_SIZE), p.SRCALPHA)
UI_CIRCLE_HIGHLIGHT = p.Surface((SQ_SIZE, SQ_SIZE), p.SRCALPHA)
p.draw.rect(UI_SQUARE_HIGHLIGHT, (184,139,74,150), UI_SQUARE_HIGHLIGHT.get_rect())
p.draw.circle(UI_CIRCLE_HIGHLIGHT, (184,139,74,150), (SQ_SIZE/2,SQ_SIZE/2), 10)

#Creates a dictionary of images, called only once in main
def loadImages():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK" ]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

#Draws the board to the screen
def drawGameState(screen, gs, playerClicks):
    drawBoard(screen)   #Draws the squares
    drawUIUnderPieces(screen, playerClicks) #Draws UI elements under pieces
    drawPieces(screen, gs.getBoard())  #Draws the pieces
    drawUIOverPieces(screen, playerClicks)

#Draws the board background
def drawBoard(screen):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if i % 2 == 0 and j % 2 == 0 or i % 2 == 1 and j % 2 == 1:
                p.draw.rect(screen, (177,228,185), (SQ_SIZE * j, SQ_SIZE * i, SQ_SIZE, SQ_SIZE))
            else:
                p.draw.rect(screen, (112,162,163), (SQ_SIZE * j, SQ_SIZE * i, SQ_SIZE, SQ_SIZE))

#Draws the UI elements under the pieces, like the current player piece selected
def drawUIUnderPieces(screen, playerClicks):
    if len(playerClicks) == 1:
        row = playerClicks[0][0]
        col = playerClicks[0][1]
        screen.blit(UI_SQUARE_HIGHLIGHT, (SQ_SIZE * col, SQ_SIZE * row))

#Draws the pieces to the board
def drawPieces(screen, board):
    for rows in range(DIMENSION):
        for cols in range(DIMENSION):
            if board[rows][cols] != "--":
                screen.blit(IMAGES[board[rows][cols]], (cols * SQ_SIZE, rows * SQ_SIZE))

#Draws the UI elements that are on top of the pieces
def drawUIOverPieces(screen, playerClicks):
    if len(playerClicks) == 1:
        for moves in validMoves:    #Displays the valid squares a piece can move to (NOTE: Costly operation will have to fix in future)
            if (row,col) == moves.getStartSq():
                screen.blit(UI_CIRCLE_HIGHLIGHT, (SQ_SIZE * moves.getEndSq()[1], SQ_SIZE * moves.getEndSq()[0]))

#Main funtion, handles user input and graphics
if __name__ == "__main__":
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    gs = GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            #Mouse Pressing
            elif e.type == p.MOUSEBUTTONDOWN and not gameOver:   #Saves the location of the piece clicked
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):    #If the same piece is clicked twice, nothing happens
                    sqSelected = ()
                    playerClicks = []
                elif (((gs.getWhiteToMove() and gs.getBoard()[row][col][0] == "w") or (not gs.getWhiteToMove() and gs.getBoard()[row][col][0] == "b")) and len(playerClicks) == 0) or len(playerClicks) == 1: #Only allows the player to select white/black pieces on their specific turn
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                    displayMoveableSquares = True
                if len(playerClicks) == 2:      #Once two different locations are in the list, the piece moves and the board updated
                    move = Move(playerClicks[0], playerClicks[1], gs.getBoard())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            #print(move.getChessNotation())
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade and ((gs.getWhiteToMove() and gs.getBoard()[row][col][0] == "w") or (not gs.getWhiteToMove() and gs.getBoard()[row][col][0] == "b")):
                        playerClicks = [sqSelected]
                    else:
                        sqSelected = ()
                        playerClicks = []

            #Key Pressing
            if e.type == p.KEYDOWN:
                if e.key == p.K_z:  #Undos a Move (When pressing the Z key)
                    gs.undoMove()
                    moveMade = True
                    gameOver = False
                if e.key == p.K_r:  #Resets the board (When pressing R key)
                    gs = GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    gameOver = False


        if moveMade:    #Only generates valid moves once a player moves
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs, playerClicks)
        def drawText(screen, text, Tcolor, Bcolor):
            font = p.font.SysFont("Helvitca", 32, True, False)
            textObject = font.render(text, 0, Bcolor)
            textLocation = p.Rect(0,0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
            screen.blit(textObject, textLocation)
            textObject = font.render(text, 0, Tcolor)
            screen.blit(textObject, textLocation.move(2, 2))

        if gs.getCheckMate():
            gameOver = True
            if gs.getWhiteToMove():
                drawText(screen, "Black wins by checkmate!", p.Color("Black"), (177,228,185))
            else:
                drawText(screen, "White wins by checkmate!", p.Color("White"), (112,162,163))
        elif gs.getStaleMate():
            gameOver = True
            drawText(screen, "Stalemate")

        clock.tick(MAX_FPS)
        p.display.flip()

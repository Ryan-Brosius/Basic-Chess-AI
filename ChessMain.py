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
HIGHLIGHT_COLOR = p.Surface((SQ_SIZE, SQ_SIZE), p.SRCALPHA)
p.draw.rect(HIGHLIGHT_COLOR, (184,139,74,150), HIGHLIGHT_COLOR.get_rect())

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
        screen.blit(HIGHLIGHT_COLOR, (SQ_SIZE * col, SQ_SIZE * row))

#Draws the pieces to the board
def drawPieces(screen, board):
    for rows in range(DIMENSION):
        for cols in range(DIMENSION):
            if board[rows][cols] != "--":
                screen.blit(IMAGES[board[rows][cols]], (cols * SQ_SIZE, rows * SQ_SIZE))


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
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            #Mouse Pressing
            elif e.type == p.MOUSEBUTTONDOWN:   #Saves the location of the piece clicked
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):    #If the same piece is clicked twice, nothing happens
                    sqSelected = ()
                    playerClicks = []
                elif (((gs.getWhiteToMove() and gs.getBoard()[row][col][0] == "w") or (not gs.getWhiteToMove() and gs.getBoard()[row][col][0] == "b")) and len(playerClicks) == 0) or len(playerClicks) == 1: #Only allows the player to select white/black pieces on their specific turn
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:      #Once two different locations are in the list, the piece moves and the board updated
                    move = Move(playerClicks[0], playerClicks[1], gs.getBoard())
                    if move in validMoves:
                        print(move.getChessNotation())
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []

            #Key Pressing
            if e.type == p.KEYDOWN:
                if e.key == p.K_z:  #Undos a Move (When pressing the Z key)
                    gs.undoMove()
                    moveMade = True

        if moveMade:    #Only generates valid moves once a player moves
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs, playerClicks)
        clock.tick(MAX_FPS)
        p.display.flip()

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

#Creates a dictionary of images, called only once in main
def loadImages():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK" ]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

#Draws the board to the screen
def drawGameState(screen, gs):
    drawBoard(screen)   #Draws the squares
    drawPieces(screen, gs.getBoard())  #Draws the pieces

#Draws the board background
def drawBoard(screen):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if i % 2 == 0 and j % 2 == 0 or i % 2 == 1 and j % 2 == 1:
                p.draw.rect(screen, (177,228,185), (SQ_SIZE * j, SQ_SIZE * i, SQ_SIZE, SQ_SIZE))
            else:
                p.draw.rect(screen, (112,162,163), (SQ_SIZE * j, SQ_SIZE * i, SQ_SIZE, SQ_SIZE))

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
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected == ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = Move(playerClicks[0], playerClicks[1], gs.getBoard())
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = ()
                    playerClicks = []

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

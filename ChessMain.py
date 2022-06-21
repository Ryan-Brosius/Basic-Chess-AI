## Name - ChessMain.py
## Purpose - Main driver file, responsible for user input and displaying information
## Author - Ryan Brosius
## Date - 6/21/2022

import pygame as p
from ChessEngine import GameState

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


def drawBoard(screen):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if i % 2 == 0 and j % 2 == 0 or i % 2 == 1 and j % 2 == 1:
                p.draw.rect(screen, (177,228,185), (64 * i, 64 * j, SQ_SIZE, SQ_SIZE))
            else:
                p.draw.rect(screen, (112,162,163), (64 * i, 64 * j, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    pass

#Main funtion, handles user input and graphics
if __name__ == "__main__":
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill((255,255,255))
    gs = GameState()
    loadImages()
    running = True
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

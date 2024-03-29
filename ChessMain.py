## Name - ChessMain.py
## Purpose - Main driver file, responsible for user input and displaying information
## Author - Ryan Brosius
## Date - 6/21/2022

import pygame as p
from ChessEngine import GameState, Move
import ChessAI
from multiprocessing import Process, Queue

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 200
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 5
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
def drawGameState(screen, gs, playerClicks, moveLogFont, drawMovePanel):
    drawBoard(screen)   #Draws the squares
    drawUIUnderPieces(screen, playerClicks) #Draws UI elements under pieces
    drawPieces(screen, gs.getBoard())  #Draws the pieces
    drawUIOverPieces(screen, playerClicks)
    if drawMovePanel:
        drawMoveLog(screen, gs, moveLogFont)

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

def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    moveLog = gs.getMoveLog()
    moveText = []
    padding = 18
    for i in range(0, len(moveLog), 2):
        moveString = str(moveLog[i])
        try:
            moveString += "  " + str(moveLog[i+1])
        except:
            pass
        moveText.append(moveString)
    counter = 0
    for i in range(0 if len(moveText) < 29 else len(moveText) - 28, len(moveText)):
        text = str(i+1) + ". " + moveText[i]
        textObject = font.render(text, True, p.Color("white"))
        textLocation = moveLogRect.move(4, 4 + padding * counter)
        screen.blit(textObject, textLocation)
        try:
            text = str(gs.getBoardRatingLog()[i*2] / 10) + "  " + str(gs.getBoardRatingLog()[i*2 + 1] / 10)
        except:
            text = str(gs.getBoardRatingLog()[i*2] / 10)
        textObject = font.render(text, True, p.Color("white"))
        textLocation = moveLogRect.move(MOVE_LOG_PANEL_WIDTH - textObject.get_width() - padding, 4 + padding * i)
        screen.blit(textObject, textLocation)

        counter += 1

#Main funtion, handles user input and graphics
if __name__ == "__main__":
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    moveLogFont = p.font.SysFont("Helvitca", 20, False, False)
    gs = GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    drawMovePanel = False
    playerOne = True    # If human playing True, if AI playing False
    playerTwo = False   # Same as above
    AIThinking = False
    moveFinderProcess = None
    
    while running:
        humanTurn = (gs.getWhiteToMove() and playerOne) or (not gs.getWhiteToMove() and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            #Mouse Pressing
            elif e.type == p.MOUSEBUTTONDOWN and not gameOver:   #Saves the location of the piece clicked
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col) or col >= 8:    #If the same piece is clicked twice, nothing happens
                    sqSelected = ()
                    playerClicks = []
                elif (((gs.getWhiteToMove() and gs.getBoard()[row][col][0] == "w") or (not gs.getWhiteToMove() and gs.getBoard()[row][col][0] == "b")) and len(playerClicks) == 0) or len(playerClicks) == 1: #Only allows the player to select white/black pieces on their specific turn
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                    displayMoveableSquares = True
                if len(playerClicks) == 2 and humanTurn:      #Once two different locations are in the list, the piece moves and the board updated
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
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    gameOver = False
                    gs = GameState()
                    validMoves = gs.getValidMoves()
                if e.key == p.K_m:
                    drawMovePanel = not drawMovePanel
                    if drawMovePanel:
                        screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
                    else:
                        screen = p.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))

        #AI move finder logic
        if not gameOver and not humanTurn:
            if not AIThinking:
                AIThinking = True
                print("Thinking...")
                returnQueue = Queue()
                moveFinderProcess = Process(target=ChessAI.findBestMove, args=(gs, validMoves, returnQueue))
                #moveFinderProcess = Process(target=ChessAI.findBestMoveMinMax, args=(gs, validMoves, returnQueue))
                moveFinderProcess.start()

            if not moveFinderProcess.is_alive():
                print("Done Thinking :D")
                AIMove = returnQueue.get()
                if AIMove is None:
                    AIMove = ChessAI.findRandomMove(validMoves)
                gs.makeMove(AIMove)
                moveMade = True
                AIThinking = False


        if moveMade:    #Only generates valid moves once a player moves
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs, playerClicks, moveLogFont, drawMovePanel)     #Draws everything boardwise
        def drawEndGameText(screen, text, Tcolor, Bcolor): #Draws text once a color wins
            font = p.font.SysFont("Helvitca", 32, True, False)
            textObject = font.render(text, 0, Bcolor)
            textLocation = p.Rect(0,0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width()/2, BOARD_HEIGHT/2 - textObject.get_height()/2)
            screen.blit(textObject, textLocation)
            textObject = font.render(text, 0, Tcolor)
            screen.blit(textObject, textLocation.move(2, 2))

        if gs.getCheckMate():
            gameOver = True
            if gs.getWhiteToMove():
                drawEndGameText(screen, "Black wins by checkmate!", p.Color("Black"), (177,228,185))
            else:
                drawEndGameText(screen, "White wins by checkmate!", p.Color("White"), (112,162,163))
        elif gs.getStaleMate():
            gameOver = True
            drawEndGameText(screen, "Stalemate", p.Color("Black"), (177,228,185))

        clock.tick(MAX_FPS)
        p.display.flip()

## Name - ChessAI.py
## Purpose - To calculate chess moves using various algorthms
## Author - Ryan Brosius
## Date - 9/1/2022

import random

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]
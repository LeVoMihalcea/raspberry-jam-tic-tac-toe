from sense_hat import SenseHat
import numpy as np

import telepot

import os, sys, time, pygame
from pygame.locals import *
from random import randint
from time import sleep

#False - Green
#True - Red
board = [[-1, -1, -1],
         [-1, -1, -1],
         [-1, -1, -1]]    
turn = False
sense = SenseHat()
player = telepot.Bot('1026818038:AAGc19rYT1wZFapEbopqq6aiMlB79tNDiHY')
red = [255, 0, 0]
green = [0, 255, 0]
black = [0, 0, 0]  
white = [255, 255, 255] 
    
pixel_board = [
    [white, white, black, white, white, black, white, white],
    [white, white, black, white, white, black, white, white],
    [black, black, black, black, black, black, black, black],
    [white, white, black, white, white, black, white, white],
    [white, white, black, white, white, black, white, white],
    [black, black, black, black, black, black, black, black],
    [white, white, black, white, white, black, white, white],
    [white, white, black, white, white, black, white, white]
    ]

def change_pixel_board(i, j):
    value = red
    if turn == False:
        value = green
    
    pixel_board[i][j] = value
    pixel_board[i][j+1] = value
    pixel_board[i+1][j] = value
    pixel_board[i+1][j+1] = value
    
    aux = []
    for line in pixel_board:
        for pixel in line:
            aux.append(pixel)
    
    sense.set_pixels(aux)
    
def validate_win():
    if [True, True, True] in board:
        return True
    if [False, False, False] in board:
        return False
    for i in range(0,3):
        if [row[i] for row in board] == [True, True, True]:
            return True
        if [row[i] for row in board] == [False, False, False]:
            return False
    if [board[0][0], board[1][1], board[2][2]] == [True, True, True]:
        return True
    if [board[0][0], board[1][1], board[2][2]] == [False, False, False]:
        return False
    if [board[0][2], board[1][1], board[2][0]] == [True, True, True]:
        return True
    if [board[0][2], board[1][1], board[2][0]] == [False, False, False]:
        return False
    
    return None

def handle_player(msg):
        global turn, board
        chat_id = msg['chat']['id']
        command = msg['text']
        
        x, y = command.split()
        x = int(x)
        y = int(y)
        print x, y
        if board[x][y] == -1:
            board[x][y] = turn
            turn = not turn        
            change_pixel_board(x*3, y*3)
        
if __name__ == "__main__":
    player.message_loop(handle_player)
    
    auxLst = []
    for line in pixel_board:
        for pixel in line:
            auxLst.append(pixel)
    
    sense.set_pixels(auxLst)
    msg = ""
    try:
        while 1:
            aux = validate_win()
            if aux == True:
                msg = "Green wins"
                break
            elif aux == False:
                msg = "Red wins"
                break
            sleep(1)
    except KeyBoardInterrupt:
        pass
    finally:
	sense.show_message(msg)
        sense.clear()
    

import os
import time
from pynput import keyboard
import threading
import random

DIMENSION = 50
#dimension of the gameplan
STOPFLAG = False
#flag usefull to stop the threads

snake_dimension = 1
GameMatrix = [[" " for _ in range(DIMENSION)] for _ in range(DIMENSION//2 -1)]
currentApple = None

snake = [[DIMENSION//2-1, DIMENSION//4-1, 3]]

stringClearScreen = 'cls' if os.name == 'nt' else 'clear'

def printMatrix(matrix):
    os.system(stringClearScreen)
    print("-"*(DIMENSION+2))
    for line in matrix:
        print("|",end="")
        for ch in line:
            print(ch,end="")
        print("|")
    print("-"*(DIMENSION+2))
    time.sleep(0.2)

def lose():
    global STOPFLAG
    os.system(stringClearScreen)
    print("-"*50)
    print("Man you lose, that's prety disappointing")
    print("-"*50)
    STOPFLAG = True

def win():
    global STOPFLAG
    os.system(stringClearScreen)
    print("-"*50)
    print("Bro you won thats very cool")
    print("-"*50)
    STOPFLAG = True

def moveSnakeHead(snake,matrix):
    matrix[snake[0][1]][snake[0][0]] = " "
    if snake[0][2] == 0:
        snake[0][0] = (snake[0][0]+1) % len(matrix[0])
    elif snake[0][2] == 2:
        snake[0][0] = (snake[0][0]-1) % len(matrix[0])
    elif snake[0][2] == 1:
        snake[0][1] = (snake[0][1]+1) % len(matrix)
    elif snake[0][2] == 3:
        snake[0][1] = (snake[0][1]-1) % len(matrix)

    if(matrix[snake[0][1]][snake[0][0]] == "#"):
        lose()
        return()

    matrix[snake[0][1]][snake[0][0]] = "H"
 
def moveSnakeBody(snake,matrix):
    if(len(snake)<=1):
        return
    for indSnakePart in range(1,len(snake)):
        matrix[snake[indSnakePart][1]][snake[indSnakePart][0]] = " "
        #we have to move the part and then update the part
        
        if snake[indSnakePart][2] == 0:
            snake[indSnakePart][0] = (snake[indSnakePart][0]+1 )% len(matrix[0])
        elif snake[indSnakePart][2] == 2:
            snake[indSnakePart][0] = (snake[indSnakePart][0]-1) % len(matrix[0])
        elif snake[indSnakePart][2] == 1:
            snake[indSnakePart][1] = (snake[indSnakePart][1]+1) % len(matrix)
        elif snake[indSnakePart][2] == 3:
            snake[indSnakePart][1] = (snake[indSnakePart][1]-1) % len(matrix)
        

        matrix[snake[indSnakePart][1]][snake[indSnakePart][0]] = "#"
    for indSnakePart in range(len(snake)-1,0,-1):
        snake[indSnakePart][2] = snake[indSnakePart-1][2] 

def spawnSnakeTail(matrix):
    global snake_dimension
    newSnake = snake[-1][::1]

    if newSnake[2] == 0:
        newSnake[0] = (newSnake[0]-1)% len(matrix[0])
    elif newSnake[2] == 2:
        newSnake[0] = (newSnake[0]+1) % len(matrix[0])
    elif newSnake[2] == 1:
        newSnake[1] = (newSnake[1]-1) % len(matrix)
    elif newSnake[2] == 3:
        newSnake[1] = (newSnake[1]+1) % len(matrix)

    snake_dimension+=1
    return newSnake

def spawnApple(matrix):
    global currentApple
    applePool = []
    for x in range(len(matrix[0])):
        for y in range(len(matrix)):
            if(matrix[y][x] == " "):
                applePool.append((x,y))
    if len(applePool) == 0:
        win()
        return
    currentApple = random.choice(applePool)
    matrix[currentApple[1]][currentApple[0]] = "o"


def gameInput():
    global snake
    while not STOPFLAG:
        with keyboard.Events() as events:
            event = events.get(1e6)
            if event.key == keyboard.KeyCode.from_char('w') and snake[0][2] != 1:
                snake[0][2] = 3
            elif event.key == keyboard.KeyCode.from_char('s') and snake[0][2] != 3:
                snake[0][2] = 1
            elif event.key == keyboard.KeyCode.from_char('a') and snake[0][2] != 0:
                snake[0][2] = 2
            elif event.key == keyboard.KeyCode.from_char('d') and snake[0][2] != 2:
                snake[0][2] = 0

def main():
    global currentApple

    os.system(stringClearScreen)
    #x, y, direction
    #Direction :
    #0 right
    #1 down
    #2 left
    #3 up
    GameMatrix[snake[0][1]][snake[0][0]] = "H"
    
    spawnApple(GameMatrix)

    while not STOPFLAG:
        printMatrix(GameMatrix)
        if(snake_dimension == (DIMENSION * ((DIMENSION//2)-1)) ):
            win()
            return
        moveSnakeHead(snake,GameMatrix)
        moveSnakeBody(snake,GameMatrix)
        if((snake[0][0],snake[0][1]) == currentApple):
            snake.append(spawnSnakeTail(GameMatrix))
            spawnApple(GameMatrix)

if __name__ == "__main__":
    threading.Thread(target=main).start()
    threading.Thread(target=gameInput).start()
import os
import time
from pynput import keyboard
import threading
import random

DIMENSION = 30
#dimension of the gameplan
STOPFLAG = False
#flag usefull to stop the threads

LOSESTRING = "-"*42+"\n"+" Man you lose, that's prety disappointing \n\t  Press Enter to exit"+"\n"+"-"*42
WINSTRING = "-"*42+"\n"+" Man you won, that's prety awesome \n\t  Press Enter to exit"+"\n"+"-"*42

snake_dimension = 1

currentApple = None

snake = [[DIMENSION//2-1, DIMENSION//4-1, -1]]

stringClearScreen = 'cls' if os.name == 'nt' else 'clear'

def printMatrix(matrix):
    os.system(stringClearScreen)
    
    print("-"*(DIMENSION+2))

    for line in matrix:
        print("|" + "".join(line) + "|")
    
    print("-"*(DIMENSION+2))
    
    time.sleep(0.2)

def endGame(phrase):
    global STOPFLAG
    
    os.system(stringClearScreen)
    
    print(phrase)
    
    STOPFLAG = True

def moveSnake(snake,matrix):
    for indSnakePart in range(len(snake)):
        matrix[snake[indSnakePart][1]][snake[indSnakePart][0]] = " "

        addX = 1 if snake[indSnakePart][2] == 0 else -1 if snake[indSnakePart][2] == 2 else 0
        addY = 1 if snake[indSnakePart][2] == 1 else -1 if snake[indSnakePart][2] == 3 else 0

        snake[indSnakePart][0] = (snake[indSnakePart][0]+addX) % len(matrix[0])
        snake[indSnakePart][1] = (snake[indSnakePart][1]+addY) % len(matrix)
    
        matrix[snake[indSnakePart][1]][snake[indSnakePart][0]] = "H" if indSnakePart == 0 else "#"
        
        if((snake[0][0],snake[0][1]) in [(snake[s][0],snake[s][1]) for s in range(1,len(snake))] ):
            endGame(LOSESTRING)
            return()

    for indSnakePart in range(len(snake)-1,0,-1):
        snake[indSnakePart][2] = snake[indSnakePart-1][2] 

def spawnSnakeTail(matrix):
    global snake_dimension
    newSnake = snake[-1].copy()

    addX = -1 if newSnake[2] == 0 else 1 if newSnake[2] == 2 else 0
    addY = -1 if newSnake[2] == 1 else 1 if newSnake[2] == 3 else 0

    newSnake[0] = (newSnake[0]+addX) % len(matrix[0])
    newSnake[1] = (newSnake[1]+addY) % len(matrix)

    snake_dimension+=1

    return newSnake

def spawnApple(matrix):
    global currentApple
    
    possiblePositionForApple = [(x,y) for x in range(len(matrix[0])) for y in range(len(matrix)) if matrix[y][x] == " "]

    currentApple = random.choice(possiblePositionForApple)
    matrix[currentApple[1]][currentApple[0]] = "o"


def gameInput(snake):
    
    #TODO Change input system because this can have some flaws

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
    #Direction : 0 right 1 down 2 left 3 up

    GameMatrix = [[" " for _ in range(DIMENSION)] for _ in range(DIMENSION//2 -1)]
    GameMatrix[snake[0][1]][snake[0][0]] = "H"
    
    spawnApple(GameMatrix)

    while not STOPFLAG:
        printMatrix(GameMatrix)
        
        if(snake_dimension == (DIMENSION * ((DIMENSION//2)-1)) ):
            endGame(WINSTRING)
            return

        moveSnake(snake,GameMatrix)
        
        if((snake[0][0],snake[0][1]) == currentApple):
            snake.append(spawnSnakeTail(GameMatrix))
            spawnApple(GameMatrix)

if __name__ == "__main__":
    threading.Thread(target=main).start()
    threading.Thread(target=gameInput(snake)).start()
import os
import time
import msvcrt
from threading import Thread
import random

random.seed()
clear = lambda: os.system('cls')

#Map variables
mapHeight = 5
mapWidth = 5

#The map itself
snakeMap = [[str for i in range(mapHeight)] for j in range(mapWidth)]

#Keep track of snake head seperatly
snakeHead = {
    "X": int(mapWidth / 2),
    "Y": int(mapHeight / 2)
}
snakeLength = 3
#Keep track of tail of snake
prevLocations = []

#Currently moving direction uses wasd keys
currentDirection = b'w'
running = True
won = False
score = 0

def drawMap():
    clear()
    for row in range(mapHeight):
        if row != 0: print()
        for col in range(mapWidth):
            print(snakeMap[col][row], end='')
    print()
    print(snakeHead)
    print("Score: " + str(score))
    
def setMap():
    for row in range(mapHeight):
        for col in range(mapWidth):
            if col in [0, mapWidth - 1] or row in [0, mapHeight - 1]:
                snakeMap[col][row] = '.'
            else:
                snakeMap[col][row] = ' '
            
            if row == snakeHead['Y'] and col == snakeHead['X']:
                snakeMap[col][row] = 'O'

def getDirection(getch):
    if getch in [b'w', b'a', b's', b'd']:
        return getch

#Handle movement
def processMove():
    global prevLocations, running
    prevLoc = snakeHead.copy()
    
    #Handle _getch input characters as bytes
    if currentDirection == b'w':
        snakeHead['Y'] -= 1
    elif currentDirection == b'a':
        snakeHead['X'] -= 1
    elif currentDirection == b's':
        snakeHead['Y'] += 1
    elif currentDirection == b'd':
        snakeHead['X'] += 1

    checkFood()
    #If checkCollision returns true, end the game
    if checkCollision(): 
        snakeMap[snakeHead['X']][snakeHead['Y']] = '#'
        snakeMap[prevLoc['X']][prevLoc['Y']] = 'X'
        running = False
        return

    #Update snakeHead position
    snakeMap[snakeHead['X']][snakeHead['Y']] = 'O'

    #Append previous locations until array meets snake length
    prevLocations.append(prevLoc)
    if (len(prevLocations) >= snakeLength):
        #Clear first element then slice it
        snakeMap[prevLocations[0]['X']][prevLocations[0]['Y']] = ' '
        prevLocations = prevLocations[1::]
    
    #Set last snakeHead location to snakebody
    snakeMap[prevLoc['X']][prevLoc['Y']] = 'X'

    #Check if all squares filled with snake
    if checkWin():
        running = False
        return

#Generate food that isnt in an occupied square
def generateFood():
    freeLocations = []
    for i in range(mapHeight):
        for j in range(mapWidth):
            if snakeMap[j][i] == ' ':
                freeLocations.append(getLoc(j, i))
    if freeLocations == []: return

    index = random.randint(0, len(freeLocations)-1)
    snakeMap[freeLocations[index]['X']][freeLocations[index]['Y']] = '@'

#Return a random map location
def getLoc(x, y):
    location = {
        'X': x,
        'Y': y
    }
    return location

#Check if head of snake is at the food, add length and score and generate more food.
def checkFood():
    global snakeLength, score
    if snakeMap[snakeHead['X']][snakeHead['Y']] == '@':
        snakeLength+=1
        score+=1
        return generateFood()

#If all prevLocations length is same as internal play area, game is won
def checkWin():
    global won
    # +1 for snakeHead
    if (mapHeight - 2) * (mapWidth - 2) == len(prevLocations) + 1:
        won = True
        return True
    else:
        return False

#Check for collisions with snake body or wall
def checkCollision():
    return True if snakeMap[snakeHead['X']][snakeHead['Y']] in ['X', '.'] else False

#Main game loop to processMovement and draw the map
def game():
    while running:
        processMove()
        drawMap()
        time.sleep(1.1)
    if won == False:
        print("You lose!")
    else:
        print("You win!")

#Initial setup
setMap()
drawMap()
generateFood()

#Start game thread
thread = Thread(target=game)
thread.start()

#Check for character input and set the currentDirection of travel
while running:
    ch = msvcrt.getch()
    currentDirection = getDirection(ch)

#Stop thread
thread.join()

#Prevent accidently closing after losing game
input()

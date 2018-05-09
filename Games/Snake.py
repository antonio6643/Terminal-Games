# Snake :p
# This one was a tad hard to make, but I eventually figured it out :p.

import os
import msvcrt
import random
import time

ViewportX = 30 # Keep it even for better position calculations.
ViewportY = 30

GameOver = False
LastGrow = time.time()

sign = lambda n: 1 if n > 0 else -1 if n < 0 else 0 # Basic sign function.

def clear():
    os.system('cls')

def GetKeydown():
    if msvcrt.kbhit():
        key = msvcrt.getch().decode('UTF-8')
        return key
    return None



class Vector2: # Created to make snake positions easier when printing the grid.
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
    
    def __repr__(self):
        return "({0}, {1})".format(self.x, self.y)

    def __eq__(self, what): # Designed specifically for [x,y]
        if type(what) == list:
            if self.x == what[0] and self.y == what[1]:
                return True
        else:
            if self.x == what.x and self.y == what.y:
                return True
        return False

    def Translate(self, x=0, y=0):
        self.x += x
        self.y += y
    
class Snake:

    SnakeBody = u"\u25A1"

    def __init__(self):
        self.body = [
            Vector2(ViewportX/2, ViewportY/2)
        ] # Center of the board
        self.direction = 1 # 1,-1,2,-2 = [North, South, East, West]

    def IsUnitOccupied(self, x, y): # Used simple x,y to prevent having to create a whole new class object.
        for b in self.body:
            if b.x == x and b.y == y:
                return True
        if x == 0 or x == ViewportX or y == 0 or y == ViewportY:
            return True

        return False

    def Grow(self):
        tail = self.body[len(self.body)-1]
        self.body.append(Vector2(tail.x, tail.y))

    def Move(self):
        global GameOver
        main = self.body[0]
        for i,b in reversed(list(enumerate(self.body))):
            if i != 0:
                previous = self.body[i-1]
                if previous.x == b.x and previous.y == b.y:
                    continue
                else:
                    b.x = previous.x
                    b.y = previous.y
        if abs(self.direction) == 1:
            main.Translate(y=self.direction)
        else:
            main.Translate(x= 1*sign(self.direction))
        if main.x >= ViewportX-1 or main.x <= 0 or main.y >= ViewportY-1 or main.y <= 0:
            GameOver = True

    def GetBodyInRow(self, row):
        listReturn = []
        for b in self.body:
            if b.y == row:
                listReturn.append(b.x)
        return listReturn

Player = Snake()
FruitPos = Vector2( random.randint(1, ViewportX-2), random.randint(1, ViewportY-2) )

def PrintGame():
    global FruitPos
    global GameOver
    global LastGrow

    if FruitPos == Player.body[0]:
        Player.Grow()
        FruitPos = Vector2( random.randint(1, ViewportX-2), random.randint(1, ViewportY-2) )
        LastGrow = time.time()

    for y in range(0, ViewportY):
        if y == 0 or y == ViewportY-1:
            print("-"*ViewportX, end=" ") # TODO: Combine these two print statements using formatting.
            if y == 0:
                print("Score: {0}".format( len(Player.body)-1 ))
            else:
                print("")
        else:
            snakeRow = Player.GetBodyInRow(y)
            #print("|"+(" "*(BoardSize-2))+"|")
            toPrint = ""
            for x in range(0, ViewportX):
                if x in snakeRow:
                    if snakeRow.count(x) > 1 and time.time()-LastGrow > 2:
                        GameOver = True
                        break
                    toPrint += "X"#u"\u25A1"
                elif FruitPos.x == x and FruitPos.y == y:
                    toPrint += "@"
                else:
                    if x == 0 or x == ViewportX-1:
                        toPrint += "|"
                    else:
                        toPrint += " "
            print(toPrint)

clear()
PrintGame()

while GameOver == False:
    key = GetKeydown()

    if key == "x":
        break

    if key == "a" and abs(Player.direction) == 1:
        Player.direction = -2
    elif key == "d" and abs(Player.direction) == 1:
        Player.direction = 2
    elif key == "w" and abs(Player.direction) == 2:
        Player.direction = -1
    elif key == "s" and abs(Player.direction) == 2:
        Player.direction = 1

    Player.Move()

    clear()
    PrintGame()
    time.sleep(1/60)

print("GAME OVER!")
print("Score: {0}".format(len(Player.body)-1))
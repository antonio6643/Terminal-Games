# Yes, this will be a challenge.
# But if it wasn't, it wouldn't be fun so ¯\_(ツ)_/¯

import os
import msvcrt
import random
import time

ViewportX = 30
ViewportY = 30
InProgress = True
RunIt = True

def Clamp(num, min, max):
    if num < min:
        return min
    if num > max:
        return max
    return num

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

# Now here's where the *real* code begins.

Blocks = []
curBlock = None # Just define it for now.

def IsBlockAt(x,y,ignore=False):
    #if any(b.x == x and b.y == y for b in Blocks):
    #    return True
    for b in Blocks:
        if any(p.x == x and p.y == y for p in b.pieces):
            return True
    if curBlock and not ignore:
        if any(p.x == x and p.y == y for p in curBlock.pieces):
            return True

class Block:

    def __init__(self, represent):
        self.pieces = represent # 3x3 grid
        self.locked = False

    def Update(self):
        global curBlock
        if self.locked == False:
            for p in self.pieces:
                p.Translate(y=1)
                if IsBlockAt(p.x, p.y+1, True) or p.y+1 == ViewportY-1:
                    self.locked = True
                    Blocks.append(curBlock)
                    curBlock = None

    def Move(self, dir):
        if self.locked == False:
            for p in self.pieces:
                p.x = Clamp(p.x+dir, 1, ViewportX-1)

class TBlock(Block):

    def __init__(self):
        super().__init__([
                Vector2(1, 1), Vector2(2, 1), Vector2(3, 1),
                Vector2(2, 2),
                Vector2(2, 3)
            ])

BlockSelections = [TBlock]

def GetNewBlock():
    global curBlock
    selected = random.choice(BlockSelections)
    curBlock = selected()

def PrintGame():
    global curBlock
    global RunIt
    for y in range(0, ViewportY):
        if y == 0 or y == ViewportY-1:
            print("-"*ViewportX)
        else:
            toPrint = ""
            for x in range(0, ViewportX):
                if IsBlockAt(x,y):
                    toPrint += "#"
                elif x == 0 or x == ViewportX-1:
                    toPrint += "|"
                else:
                    toPrint += " "
            print(toPrint)
    if curBlock is not None and RunIt is not False:
        curBlock.Update()
    else:
        if curBlock is None:
            GetNewBlock()
    RunIt = not RunIt

while InProgress:
    key = GetKeydown()

    if key == "x":
        print("EXITING")
        break

    if curBlock:
        if key == "a":
            curBlock.Move(-1)
        elif key == "d":
            curBlock.Move(1)

    time.sleep(1/60)
    clear()
    PrintGame()
    
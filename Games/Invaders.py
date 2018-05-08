# Basically just Space Invaders

import os
import msvcrt
import math
import time

ViewportX = 40
ViewportY = 30

Bullets = []
Enemies = []
lastShot = time.time()

Score = 0

Direction = 1

ShotDelay = 1

def clear():
    os.system('cls')

def GetKeydown():
    if msvcrt.kbhit():
        key = msvcrt.getch().decode('UTF-8')
        return key
    return None

def Clamp(num, min, max):
    if num < min:
        return min
    if num > max:
        return max
    return num

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

class Ship:
    def __init__(self, hp, startPos):
        self.hp = hp
        self.position = startPos
        self.representation = "V" # Λ For Player
        self.status = 1 # 1 = enemy, -1 = ally.
    
    def Translate(self, x=0, y=0):
        self.position.x = Clamp( self.position.x + x, 1, ViewportX-2 )
        self.position.y = Clamp( self.position.y + y, 1, ViewportY-2 )
        return self.position

    def Fire(self):
        return Bullets.append( [Vector2(self.position.x, self.position.y), self.status] )

class PlayerShip(Ship):
    def __init__(self, hp):
        super().__init__(hp, Vector2(ViewportX/2, math.floor(ViewportY*(3/4)) ))
        self.representation = "Λ"
        self.status = -1

Player = PlayerShip(3)

for s in range(0, 10):
    Enemies.append( 
        Ship(
            1, # Health
            Vector2( (ViewportX/2) - 5 + s, 5 ) # Starting Position
        ) 
    )

def Update():
    global Direction

    eMoveDown = False

    for i,b in enumerate(Bullets):
        b[0].y += b[1]
        if b[0].y <= 0:
            del Bullets[i]

    #if Enemies[0].position.x == 1 or Enemies[len(Enemies)-1].position.x == ViewportX-1:
    if any(enemy.position.x == 0 or enemy.position.x == ViewportX-1 for enemy in Enemies):
        eMoveDown = True
        Direction = Direction * -1

    for e in Enemies:
        e.position.Translate(x=Direction, y=1 if eMoveDown == True else 0)
        if any(bullet[0] == e.position for bullet in Bullets):
            e.hp -= 1
            Bullets.remove( [[e.position.x, e.position.y], -1] )

def PrintGame():
    global Score
    for y in range(0, ViewportY):
        if y == 0 or y == ViewportY-1:
            print("-"*ViewportX)
        else:
            toPrint = ""
            for x in range(0, ViewportX):
                bulletFound = False
                if x == 0 or x == ViewportX-1:
                    toPrint += "|"
                    bulletFound = True # shhhhhhhhhhhhhh
                else:
                    if x == Player.position.x and y == Player.position.y:
                        toPrint += "+"#u"\u0245"#"O"
                        bulletFound = True
                    else:
                        for i,e in enumerate(Enemies):
                            if e.position.x == x and e.position.y == y:
                                if e.hp > 0:
                                    toPrint += "X"
                                else:
                                    toPrint += "&"
                                    Score += 1
                                    del Enemies[i]
                                bulletFound = True
                        for b in Bullets:
                            if b[0].x == x and b[0].y == y:
                                toPrint += "|"
                                bulletFound = True
                if bulletFound == False:
                    toPrint += " "
            try:
                print(toPrint)
            except OSError:
                print(toPrint) # Try again.

while True:
    key = GetKeydown()

    if key == "x":
        print("EXITING")
        break

    if key == "a":
        Player.Translate(x=-1)
    elif key == "d":
        Player.Translate(x=1)
    elif key == "f":
        if time.time()-lastShot >= 0.75: # .75 second shot delay
            Player.Fire()
            lastShot = time.time()

    # Rendering
    clear()
    Update()
    PrintGame()

    if len(Enemies) == 0:
        break

    time.sleep(1/60) # 60 because 60 frames per second.

print("GAME OVER!")
print("Score: {0}".format(str(Score)))
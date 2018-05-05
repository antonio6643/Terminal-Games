# Basically like subway surfers but in the terminal.

import msvcrt
import os
from random import randrange
from time import sleep

speed = 0.5 # The time it takes to go to move up.

Course = [] # Entries will be simple strings formatted like so: "- O X" (5 characters)
Position = 0
Score = -9

Dead = False

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

def ReplaceAtIndex(string, index, char):
    return string[:index]+char+string[index+1:]

def GenerateObstacle():
    oPos = randrange(0, 5, 2)
    line = ReplaceAtIndex("- - -", oPos, "X")
    Course.insert(0, line)
    if len(Course) > 6:
        Course.pop()

clear()


for i in range(1, 10):
    Course.insert(0, "- - -")
    

while True:
    
    # Movement first.
    key = GetKeydown()
    
    if key == "a":
        Position = Clamp(Position-2, 0, 5)
    elif key == "d":
        Position = Clamp(Position+2, 0, 5)
    elif key == "x":
        print("EXITING!")
        clear()
        break

    # Course Printing.

    clear()
    for i,o in enumerate(Course):
        if i == len(Course)-1:
            if o[Position:Position+1] == "X":
                Dead = True
                break
            else:
                print(ReplaceAtIndex(o, Position, "+"))
        else:
            try:
                print(o)
            except OSError:
                print(o) # Try again :P
    if Dead:
        break
    Score += 1
    GenerateObstacle()
    sleep(speed)
    
print("YOU DIED!")
print("Final Score: {0}".format(str(Score)))
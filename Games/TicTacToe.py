# Just some good 'ol 2-player Tic Tac Toe.

# Yes I realized I may have mislabeled rows and columns in the code but ¯\_(ツ)_/¯

import msvcrt
import os

Board = [               # Yes, I realize I could've just done this all in one List.
    ["1", "2", "3"],     # I used this method in order to make it easier to decide victories.
    ["4", "5", "6"],
    ["7", "8", "9"]
]

TurnOne = True
WrongMove = False
Exited = False

def clear():
    os.system('cls')

def GetKeydown():
    if msvcrt.kbhit():
        key = msvcrt.getch().decode('UTF-8')
        try:
            return int(key)
        except ValueError:
            if key == "x":
                return key
    return None

def SpaceIsOpen(num):
    row = 0
    if num <= 3:
        row = 0
    elif num <= 6:
        row = 1
    else:
        row = 2
    
    if num > 3:
        space = num - (3*(row)) - 1
    else:
        space = num - 1

    bSpot = Board[row][space]
    if bSpot != "O" and bSpot != "X":
        print("Move in.")
        return row,space
    return False, False

def PrintBoard():
    for i,r in enumerate(Board):
        print("      |       |       |       |")
        print( "      |   {0}   |   {1}   |   {2}   |".format(r[0], r[1], r[2]) )
        print("      |       |       |       |")
        if i != 2:
            print( "------|-------|-------|-------|------" )

    print("Player One's Turn" if TurnOne else "Player Two's Turn", end=" ")
    print("(Try Again)" if WrongMove else "")

def CheckVictory():
    for i in range(0, 3):
        if Board[i][0] == Board[i][1] and Board[i][1] == Board[i][2]: # Row Checking.
            return Board[i][0]
        if Board[0][i] == Board[1][i] and Board[1][i] == Board[2][i]: # Column Checking
            return Board[0][i]

    if Board[0][0] == Board[1][1] and Board[1][1] == Board[2][2]:
        return Board[1][1] # Whoever holds the middle is the one with the diagonal win.
    if Board[2][0] == Board[1][1] and Board[1][1] == Board[0][2]:
        return Board[1][1]
clear()

PrintBoard()

while True:
    key = GetKeydown()

    if key == "x":
        Exited = True
        break

    if key and key is not False:
        row, space = SpaceIsOpen(key)

        if row is not False:
            Board[row][space] = "X" if TurnOne else "O"
            if CheckVictory():
                break
            TurnOne = not TurnOne
            WrongMove = False
        else:
            WrongMove = True

        clear()
        PrintBoard()

if Exited == False:
    clear()
    PrintBoard()
    print("Player One wins!" if TurnOne else "Player Two wins!")
else:
    print("Game quit by Player One" if TurnOne else "Game quit by Player Two")
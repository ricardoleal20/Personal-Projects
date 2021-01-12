##----------------------------------------------##
## This is one code that I use to play the cat  ##
## game. I made this for a homework to learn how##
## to use Python and learn what i can make with ##
## this programming languaje.                   ##
##                                              ##
## Made if by Ricardo Leal.            08/09/20 ##
## email: ricardo_lealpz@gmail.com              ##
## github.com/ricardoleal20                     ##
##----------------------------------------------##

#Some libraries that we are gonna import.
import math
import random

#Define a function that can works to place the brand in the board.
def coordinate(cord, inf, sup):
  while True:
   value=input(cord)
   while(not value.isnumeric()):
   	print("Only numbers [0] and [1] will be admitted.".format(inf,sup))
   	print(" ")
   	value=input(cord)
   cord=int(value)
   if(cord>=inf and cord<=sup):
    return cord

   else:
   	print("The number is incorrect, choose a number between [0] and [1].".format(inf,sup))
   	print(" ")

#This function print the place in the board of our domain.
def VisualBoard():
	pos=0
	print(("-"*19))
	for row in range(3):
		for Column in range(3):
			print("| ",board[pos]," ",end="")
			pos+=1
		print("|\n",("-"*18))

def spaceWin(space,brandd,i,j):
 f=math.floor(space/BOARD_ROWS)
 c=space % BOARD_COLUMNS
 new_row=f+i
 if(new_row<0 or new_row>=BOARD_ROWS):
 	return 0
 new_column=c+j
 if(new_column<0 or new_column>=BOARD_COLUMNS):
 	return 0
 pos=(new_row*BOARD_COLUMNS+new_column)
 if(board[pos]!=brandd):
  return 0
 else:
  return 1+spaceWin(pos,brandd,i,j)


#Define how we can put the brand in the board.
def ColocateBrand(brandd):
  print("Tell me where you want to place your brand.")
  while True:
   row=coordinate("Choose the space in the row (only between 1 & 3): ", 1,3)-1
   Column=coordinate("Choose the space in the column (only between 1 & 3): ", 1,3)-1
   space=row*BOARD_COLUMNS+Column
   if(board[space]!=' '):
    print("This space is occupied. Choose another one.") #This is if the space is occupied.
    print(" ")
   else:
    board[space]=brandd
    return space

#This function defina a IA that can play with us.
def ColocateBrandIA(brandd,IAbrand):
	random.shuffle(BlankSpace)
	for space in BlankSpace:
		if(win(space,brandd)):
			board[space]=brandd
			return space
	for space in BlankSpace:
		if(win(space,IAbrand)):
			board[space]=brandd
			return space
	for space in BlankSpace:
		board[space]=brandd
		return space

#Define the function that will tell us if someone win the game.
def win(space,brandd):
 	numbers=spaceWin(space,brandd,-1,-1)+spaceWin(space,brandd,1,1)
 	if(numbers==2):
 		return True
 	numbers=spaceWin(space,brandd,1,-1)+spaceWin(space,brandd,-1,1)
 	if(numbers==2):
 		return True
 	numbers=spaceWin(space,brandd,-1,0)+spaceWin(space,brandd,1,0)
 	if(numbers==2):
 		return True
 	numbers=spaceWin(space,brandd,0,-1)+spaceWin(space,brandd,0,1)
 	if(numbers==2):
 		return True

#Define the magnitude of the board.
board=[]
BlankSpace=[]
BOARD_COLUMNS=3
BOARD_ROWS=3
for x in range(9):
   board.append(' ')
   BlankSpace.append(x)

#Definition of the players

players=[]
numberPlayers=coordinate("Number of players: ",0,2)
for y in range(numberPlayers):
	players.append({"Name":input("Name of the player "+str(y+1)+": "),"type":"H"})
for y in range(2-numberPlayers):
	players.append({"Name":"Machine "+str(y+1),"type":"M"})

print("\n The game starts with the players:")
for player in players:
	print("\t",player["Name"])

Starts=coordinate("Which player starts? [1="+players[0]["Name"]+",2="+players[1]["Name"]+"]: ",1,2)
if(Starts==2):
	players.reverse()

#Write some variables to use during the game.
keepgame=True
brand=0

#This is the core of the game, where you put all the things.
while keepgame:
 VisualBoard()
 numPlayer=(brand&1)
 brandd='X' if numPlayer==1 else '0'
 if(players[numPlayer]["type"]=="H"):
 	space=ColocateBrand(brandd)
 else:
 	space=ColocateBrandIA(brandd,'X' if numPlayer==0 else '0')
 BlankSpace.remove(space)
 if(win(space,brandd)):
   keepgame=False
   print(" ")
   print(players[numPlayer]["Name"],"congratulations, you win!!!!!!!.")
 brand+=1
 if(brand==9):
   keepgame=False
VisualBoard()
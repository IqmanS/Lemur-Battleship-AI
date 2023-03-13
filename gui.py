import pygame
from engine import *
pygame.init()
pygame.display.set_caption("Battleship")

#global variables
CELL_SIZE = 35
H_MARGIN,V_MARGIN = CELL_SIZE*2,CELL_SIZE*3
WIDTH,HEIGHT = CELL_SIZE*10*2+V_MARGIN,CELL_SIZE*10*2+H_MARGIN
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
INDENT  = 8
#colors
GREY = (50,50,60)
WHITE = (255,250,250)
GREEN = (50,250,120)

#function to draw a grid
def drawGrid(left = 0,top=0):
    for i in range(100):
        x = left + i % 10 * CELL_SIZE
        y = top+ i // 10 * CELL_SIZE
        square = pygame.Rect(x,y,CELL_SIZE,CELL_SIZE)
        pygame.draw.rect(SCREEN,WHITE,square,width=1)

def drawShipsOnGrids(player,left = 0,top=0):

    for ship in player.ships:
        x = left + ship.col * CELL_SIZE +INDENT
        y = top+ ship.row * CELL_SIZE +INDENT
        if ship.orientation == "h":
            widthShip = ship.size * CELL_SIZE - INDENT *2
            heightShip = CELL_SIZE - INDENT *2
        else:
            widthShip = CELL_SIZE - INDENT *2
            heightShip = ship.size * CELL_SIZE - INDENT *2
        shipRect = pygame.Rect(x,y,widthShip,heightShip)
        pygame.draw.rect(SCREEN,GREEN,shipRect,border_radius=14)

player1 = Player()
player2 =Player()
# player1.showShips()
# player2.showShips()
#game
animating = True
pausing = False
while animating:

    #track user input
    for event in pygame.event.get():

        #pygame closed
        if event.type == pygame.QUIT:
            animating = False

        #keyboard press
        if event.type == pygame.KEYDOWN:

            #escape to close
            if event.key == pygame.K_ESCAPE:
                animating = False
            #spce to pause
            if event.key == pygame.K_SPACE:
                pausing = not pausing

    if not pausing:
        #draw background
        SCREEN.fill(GREY)

        #search grids
        drawGrid()                                          #TOP LEFT
        drawGrid(CELL_SIZE*10+V_MARGIN,CELL_SIZE*10+H_MARGIN)#BOTTOM RIGHT

        #position grids
        drawGrid(CELL_SIZE*10+V_MARGIN)                     #TOP RIGHT
        drawGrid(0,CELL_SIZE*10+H_MARGIN)                   #BOTTOM LEFT
        #draw ships
        drawShipsOnGrids(player1,CELL_SIZE*10+V_MARGIN)
        drawShipsOnGrids(player2, 0,CELL_SIZE*10+H_MARGIN)
        #update screen
        pygame.display.flip()



import pygame
from engine import *
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("fresansttf",100)
pygame.display.set_caption("Battleship")

#global variables
CELL_SIZE = 35
H_MARGIN,V_MARGIN = CELL_SIZE*2,CELL_SIZE*3
WIDTH,HEIGHT = CELL_SIZE*10*2+V_MARGIN,CELL_SIZE*10*2+H_MARGIN
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
INDENT  = 8

HUMAN1 = True
HUMAN2 = False

#colors
GREY = (50,50,60)
WHITE = (255,250,250)
GREEN = (50,250,120)
BLUE = (50,120,250)
ORANGE = (225,165,0)
RED = (255,50,50)
SEARCH_COLORS = {"U":GREY,"M":BLUE,"H":ORANGE,"S":RED}

#function to draw a grid
def drawGrid(player,left = 0,top=0,search = False):
    for i in range(100):
        x = left + i % 10 * CELL_SIZE
        y = top+ i // 10 * CELL_SIZE
        square = pygame.Rect(x,y,CELL_SIZE,CELL_SIZE)
        pygame.draw.rect(SCREEN,WHITE,square,width=1)
        if search:
            x+= CELL_SIZE//2
            y+= CELL_SIZE//2
            pygame.draw.circle(SCREEN,SEARCH_COLORS[player.search[i]],(x,y),radius=CELL_SIZE//4)

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


game = Game(human1=HUMAN1,human2=HUMAN2)
def player1Turn(game):
    if x < CELL_SIZE * 10 and y < CELL_SIZE * 10:
        row = y // CELL_SIZE
        col = x // CELL_SIZE
        index = row * 10 + col
        game.makeMove(index)


def player2Turn(game):
    if x > CELL_SIZE * 10 + V_MARGIN and y > CELL_SIZE * 10 + H_MARGIN:
        row = (y - CELL_SIZE * 10- H_MARGIN) // CELL_SIZE
        col = (x - CELL_SIZE * 10- V_MARGIN) // CELL_SIZE
        index = row * 10 + col
        game.makeMove(index)
       
#game
animating = True
pausing = False
while animating:

    #track user input
    for event in pygame.event.get():

        #pygame closed
        if event.type == pygame.QUIT:
            animating = False
        
        #mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            (x,y) = pygame.mouse.get_pos()
            
            if not game.gameOver and game.player1_turn:
                player1Turn(game)

            elif not game.gameOver and not game.player1_turn:
                player2Turn(game)
   
        #keyboard press
        if event.type == pygame.KEYDOWN:

            #escape to close
            if event.key == pygame.K_ESCAPE:
                animating = False
            #spce to pause
            if event.key == pygame.K_SPACE:
                pausing = not pausing
            
            #enter key to restart the game
            if event.key == pygame.K_RETURN:
                game = Game(human1=HUMAN1,human2=HUMAN2)
                
    if not pausing:
        #draw background
        SCREEN.fill(GREY)

        #search grids
        drawGrid(game.player1,search=True)                                          #TOP LEFT
        drawGrid(game.player2,CELL_SIZE*10+V_MARGIN,CELL_SIZE*10+H_MARGIN,search= True)#BOTTOM RIGHT

        #position grids
        drawGrid(game.player1,CELL_SIZE*10+V_MARGIN)                   #BOTTOM LEFT
        drawGrid(game.player2 ,0,CELL_SIZE*10+H_MARGIN)                 #TOP RIGHT

        #draw ships
        drawShipsOnGrids(game.player2,CELL_SIZE*10+V_MARGIN)
        drawShipsOnGrids(game.player1, 0,CELL_SIZE*10+H_MARGIN)
        
        if not game.gameOver and game.computerTurn:
            game.RandomAI()
        
        #game over
        if game.gameOver:
            text = game.result+" WON!"
            textbox = font.render(text,False,GREY,WHITE)
            SCREEN.blit(textbox,(WIDTH//2-200,HEIGHT//2-50))
        
        #update screen
        pygame.display.flip()



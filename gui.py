import pygame
import asyncio
from engine import *

pygame.init()
pygame.font.init()
fontH = pygame.font.SysFont("fresansttf", 66)
fontS = pygame.font.SysFont("fresansttf", 45)
fontM = pygame.font.SysFont("fresansttf", 30)
pygame.display.set_caption("Battleship")

# global variables
CELL_SIZE = 35
H_MARGIN, V_MARGIN = CELL_SIZE * 2, CELL_SIZE * 3
WIDTH, HEIGHT = CELL_SIZE * 10 * 2 + V_MARGIN + 80, CELL_SIZE * 10 * 2 + H_MARGIN
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
INDENT = 8

humanVShuman = False
humanVScomputer = True
computerVScomputer = False

# colors
GREY = (70, 100, 150)
WHITE = (255, 250, 250)
GREEN = (80, 250, 120)
BLUE = (200, 200, 200)
ORANGE = (225, 165, 0)
RED = (255, 50, 50)
SEARCH_COLORS = {"U": GREY, "M": BLUE, "H": ORANGE, "S": RED}


# function to draw a grid
def drawGrid(player, left=0, top=0, search=False):
    for i in range(100):
        x = left + i % 10 * CELL_SIZE
        y = top + i // 10 * CELL_SIZE
        square = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(SCREEN, WHITE, square, width=1)


def drawShipsOnGrids(player, isComputer, left=0, top=0):
    for ship in player.ships:
        x = left + ship.col * CELL_SIZE + INDENT
        y = top + ship.row * CELL_SIZE + INDENT
        if ship.orientation == "h":
            widthShip = ship.size * CELL_SIZE - INDENT * 2
            heightShip = CELL_SIZE - INDENT * 2
        else:
            widthShip = CELL_SIZE - INDENT * 2
            heightShip = ship.size * CELL_SIZE - INDENT * 2
        shipRect = pygame.Rect(x, y, widthShip, heightShip)
        # pygame.draw.rect(SCREEN,GREEN,shipRect,border_radius=14)
        ship_img = pygame.image.load(str(ship.size) + "r.png")
        shipVer_img = pygame.transform.flip(pygame.transform.rotate(ship_img, 90), False, True)
        if not isComputer or ship.isSunk:
            if ship.orientation == "h":
                SCREEN.blit(ship_img, (x - INDENT, y - INDENT))
            elif ship.orientation == "v":
                SCREEN.blit(shipVer_img, (x - INDENT, y - INDENT))


def drawHits(player, left=0, top=0, search=False):
    for i in range(100):
        x = left + i % 10 * CELL_SIZE
        y = top + i // 10 * CELL_SIZE
        if player.search[i] != "U":
            x += CELL_SIZE // 2
            y += CELL_SIZE // 2
            pygame.draw.circle(SCREEN, SEARCH_COLORS[player.search[i]], (x, y), radius=CELL_SIZE // 4)


async def main():
    game = Game(humanVShuman=humanVShuman,
                humanVScomputer=humanVScomputer, computerVScomputer=computerVScomputer)
    
    def player1Turn(game):
        if x < CELL_SIZE * 10 and y < CELL_SIZE * 10:
            row = y // CELL_SIZE
            col = x // CELL_SIZE
            index = row * 10 + col
            if game.player1.search[index] == "U":
                game.makeMove(index)
    
    def player2Turn(game):
        if x > CELL_SIZE * 10 + V_MARGIN and y > CELL_SIZE * 10 + H_MARGIN:
            row = (y - CELL_SIZE * 10 - H_MARGIN) // CELL_SIZE
            col = (x - CELL_SIZE * 10 - V_MARGIN) // CELL_SIZE
            index = row * 10 + col
            if game.player2.search[index] == "U":
                game.makeMove(index)
    
    # game
    animating = True
    pausing = False
    bg = pygame.image.load("bg.jpg")
    while animating:
        
        # track user input
        for event in pygame.event.get():
            
            # pygame closed
            if event.type == pygame.QUIT:
                animating = False
            
            # mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()
                (x, y) = (x - 40, y - 75)
                if not game.gameOver and game.player1_turn and not game.computerTurn:
                    # print("p1")
                    player1Turn(game)
                
                elif not game.gameOver and not game.player1_turn and not game.computerTurn:
                    # print("p2")
                    player2Turn(game)
            
            if (not game.gameOver) and game.computerTurn and not game.player1_turn:
                # print("\ncomputer")
                game.ImprovedSearchAIwithNeighbour()
            
            # keyboard press
            if event.type == pygame.KEYDOWN:
                
                # escape to close
                if event.key == pygame.K_ESCAPE:
                    animating = False
                # spce to pause
                
                # enter key to restart the game
                if event.key == pygame.K_RETURN:
                    game = Game(humanVShuman=humanVShuman,
                                humanVScomputer=humanVScomputer, computerVScomputer=computerVScomputer)
        
        if not pausing:
            await asyncio.sleep(0)
            # draw background
            SCREEN.fill(GREY)
            SCREEN.blit(bg, (0, 0))
            # search grids
            drawGrid(game.player1, 40, 75, search=True)  # TOP LEFT
            drawGrid(game.player2, CELL_SIZE * 10 + V_MARGIN + 40, 75, search=True)  # BOTTOM RIGHT
            
            # position grids
            # drawGrid(game.player1,CELL_SIZE*10+V_MARGIN)                   #BOTTOM LEFT
            # drawGrid(game.player2 ,0,CELL_SIZE*10+H_MARGIN)                 #TOP RIGHT
            
            # draw ships
            drawShipsOnGrids(game.player2, True, 40, 75)
            drawShipsOnGrids(game.player1, False, CELL_SIZE * 10 + V_MARGIN + 40, 75)
            
            drawHits(game.player1, 40, 75, search=True)  # TOP LEFT
            drawHits(game.player2, CELL_SIZE * 10 + V_MARGIN + 40, 75, search=True)
            
            playerInfo = "Player Grid"
            platerDets = "You hit here"
            playerInfoBox = fontH.render(playerInfo, True, (0, 0, 0))
            platerDetsBox = fontS.render(platerDets, True, (0, 0, 0))
            SCREEN.blit(playerInfoBox, (40, 100 + CELL_SIZE * 10))
            SCREEN.blit(platerDetsBox, (40, 100 + CELL_SIZE * 10 + 50))
            
            AIInfo = "AI Bot Grid"
            AIDets1 = "Your Ships go here"
            AIDets2 = "AI hits here"
            AIInfoBox = fontH.render(AIInfo, True, (0, 0, 0))
            AIDetsBox1 = fontS.render(AIDets1, True, (0, 0, 0))
            AIDetsBox2 = fontS.render(AIDets2, True, (0, 0, 0))
            SCREEN.blit(AIInfoBox, (CELL_SIZE * 10 + V_MARGIN + 40, 100 + CELL_SIZE * 10))
            SCREEN.blit(AIDetsBox1, (CELL_SIZE * 10 + V_MARGIN + 40, 100 + CELL_SIZE * 10 + 50))
            SCREEN.blit(AIDetsBox2, (CELL_SIZE * 10 + V_MARGIN + 40, 100 + CELL_SIZE * 10 + 85))
            
            key1 = "Press ENTER - Randomize Your Ships"
            key2 = "Press LMB - Hit on Opponents Grid"
            keyBox1 = fontS.render(key1, True, (0, 0, 0))
            keyBox2 = fontS.render(key2, True, (0, 0, 0))
            SCREEN.blit(keyBox1, ((CELL_SIZE * 10 + 40) // 2, 100 + CELL_SIZE * 10 + 135))
            SCREEN.blit(keyBox2, ((CELL_SIZE * 10 + 40) // 2, 100 + CELL_SIZE * 10 + 170))
            
            githubBox = fontM.render("github.com/IqmanS", True, (0, 0, 0))
            SCREEN.blit(githubBox, (CELL_SIZE * 19, CELL_SIZE * 20 + 25))
            # game over
            if game.gameOver:
                pygame.time.delay(500)
                text = None
                if game.result == "Player 1":
                    text = "YOU WON!!"
                else:
                    text = "YOU LOST :("
                textbox = fontH.render(text, True, (0, 0, 0), (255, 255, 255))
                SCREEN.blit(textbox, (WIDTH // 2 - 125, HEIGHT // 2 - 35))
            
            # update screen
            pygame.display.flip()


asyncio.run(main())
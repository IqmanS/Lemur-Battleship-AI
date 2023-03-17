import random

class Ship:
    def __init__(self,size):
        self.row = random.randrange(0,9)
        self.col = random.randrange(0,9)
        self.size = size
        self.orientation = random.choice(["h","v"])
        self.indexes = self.compute_indexes()

    def compute_indexes(self):
        start_index = self.row *10 +self.col
        if self.orientation=="h":
            return [start_index+i for i in range(self.size)]
        elif self.orientation=="v":
            return [start_index+i*10 for i in range(self.size)]

class Player:
    def __init__(self):
        self.ships = []
        self.search = ["U" for i in range(100)] #"U" for unknown
        self.placeShips(sizes = [5,4,3,3,2])
        list_of_lists_of_indexes = [ship.indexes for ship in self.ships]
        self.indexOfAllShips = [index for sublist in list_of_lists_of_indexes for index in sublist]
        self.sunkCount = 0
    def placeShips(self,sizes):
        for size in sizes:
            placed = False
            while not placed:
                #create a new ship
                ship = Ship(size)
                #check if placement is possible
                possible = True
                
                #checks
                for i in ship.indexes:
                    #indexes <100
                     if i>=100:
                         possible = False
                         break
                     new_row = i // 10
                     new_col = i % 10
                    # ships can not be placed over edges and next lines
                     if new_row!=ship.row and new_col!=ship.col:
                         possible = False
                         break
                     # cannot intersect other ships
                     for other_ship in self.ships:
                         if i in other_ship.indexes:
                             possible = False
                             break

                #after passing place the ship
                if possible:
                    self.ships.append(ship)
                    placed = True

    def showShips(self):
         indexes = []
         for i in range(100):
             if i not in self.indexOfAllShips:
                 indexes.append("-")
             else :
                 indexes.append("x")
         for row in range(10):
             for col in range(10):
                 print(indexes[row*10+col],end=" ")
             print()

class Game:
    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        self.player1_turn = True
        self.gameOver = False
        
    def makeMove(self,i):
        player = self.player1 if self.player1_turn else self.player2
        opponent = self.player2 if self.player1_turn else self.player1
        
        #set miss "M" or hit "H"
        if i in opponent.indexOfAllShips:
            player.search[i] = "H"
            #check if ship sunk "S"
            for ship in opponent.ships:

                sunk = True
                for i in ship.indexes:
                    if player.search[i]=="M" or player.search[i]=="U":
                        sunk = False
                        break
                if sunk:
                    for i in ship.indexes:
                        player.search[i] = "S"
                        player.sunkCount+=1
        
        else:
            # set miss "M"
            player.search[i] = "M"
        self.player1_turn = not self.player1_turn
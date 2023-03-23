import random

class Ship:
    def __init__(self,size):
        self.row = random.randrange(0,9)
        self.col = random.randrange(0,9)
        self.size = size
        self.orientation = random.choice(["h","v"])
        self.indexes = self.compute_indexes()
        self.isSunk = False

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
        self.unknown = []
        for i in range(0, 10, 1):
            for j in range(0, 10, 2):
                if i % 2 == 0:
                    k = (i * 10 + j)
                else:
                    k = (i * 10 + j + 1)
                self.unknown.append(k)
        
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
    def __init__(self,humanVShuman,humanVScomputer,computerVScomputer):
        self.humanVShuman = humanVShuman
        self.humanVScomputer = humanVScomputer
        self.computerVSComputer = computerVScomputer
        self.player1 = Player()
        self.player2 = Player()
        self.player1_turn = True
        if(humanVShuman):
            self.computerTurn = False
        if(humanVScomputer):
            self.computerTurn = False
        if(computerVScomputer):
            self.computerTurn = True
        self.gameOver = False
        self.result = None

    def makeMove(self,i):
        player = self.player1 if self.player1_turn else self.player2
        opponent = self.player2 if self.player1_turn else self.player1
        hit = False
        #set miss "M" or hit "H"
        if i in opponent.indexOfAllShips:
            player.search[i] = "H"
            hit = True
            player.sunkCount += 1
            # print("player1" if self.player1_turn else "player2",i,player.sunkCount)
            #check if ship sunk "S"
            for ship in opponent.ships:
                if ship.isSunk==False:
                    ship.isSunk = True
                    for i in ship.indexes:
                        if player.search[i]=="M" or player.search[i]=="U":
                            ship.isSunk = False
                            break
                    if ship.isSunk:
                        for i in ship.indexes:
                            player.search[i] = "S"

        else:
            # set miss "M"
            player.search[i] = "M"
            
        #check if GAMEOVER
        if player.sunkCount >= 17:
            # print(player.sunkCount)
            #opponent won
            self.gameOver = True
            self.result = "Player 1" if self.player1_turn else "Player 2"
        
        # if hit:
        #     player.unknown.remove(i)
        
        #switch turns for both humans
        if not hit:
            self.player1_turn = not self.player1_turn
        print(hit)
        #switch between human and computer
        if (not hit) and self.humanVScomputer==True:
            self.computerTurn = not self.computerTurn
        
    def RandomAI(self):
        player = self.player1 if self.player1_turn else self.player2
        search = player.search
        unknown = []
        for i in range(100):
            if search[i] == "U":
                unknown.append(i)
        if len(unknown) > 0:
            random_index_to_hit = random.choice(unknown)
            self.makeMove(random_index_to_hit)
            
    def RandomAIwithNeighbour(self):
        player = self.player1 if self.player1_turn else self.player2
        search = player.search
        hits = []
        for i in range(100):
            if search[i] == "H":
                hits.append(i)
        if len(hits)>0:
            for j in hits:
                i = random.choice(hits)
                neighbours = []
                if (i+1<100) and search[i + 1] == "U":
                    neighbours.extend([i + 1])
                if (i-1>0) and search[i - 1] == "U":
                    neighbours.extend([i - 1])
                if (i+10<100) and search[i + 10] == "U":
                    neighbours.extend([i + 10])
                if (i-10>0) and search[i - 10] == "U":
                    neighbours.extend([i - 10])
                if len(neighbours) > 0:
                    index = random.choice(neighbours)
                    if index in player.unknown:
                        player.unknown.remove(index)
                    self.makeMove(index)
                else:
                    hits.remove(i)
            else:
                self.ImprovedSearchPattern()
        else:
            self.ImprovedSearchPattern()

    def ImprovedSearchPattern(self):
        player = self.player1 if self.player1_turn else self.player2
        if len(player.unknown) > 0:
            random_index_to_hit = random.choice(player.unknown)
            player.unknown.remove(random_index_to_hit)
            self.makeMove(random_index_to_hit)
            
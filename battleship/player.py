import board

class Player():
    def __init__(self):
        self.shipBoard = board.Board() #board w/ player's ships on it
        self.attackBoard = board.Board() #board where player attacks
        #self.shipList = []

    def addShip(self, ship = board.Ship):
        self.shipList.append(ship)
        self.shipBoard.addToBoard(ship)
    
    def attack(self): #select target on board to attack
        pass

    def wasShipHit(self, x, y): #see if own ship was hit by other player's attack
        #check other player's most recent attack coords (x and y input)
        #compare it with ship placements on shipBoard, change ship status accordingly
        #this might make more sense to add to board.py idk 
        pass



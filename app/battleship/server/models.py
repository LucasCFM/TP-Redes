from random import randint


MAX_SHIP_SIZE = 5
MIN_SHIP_SIZE = 2


class Ship(object):
    size: int
    orientation: str


    def __init__(self, size: int, orientation: str, location: dict):
        self.size = size
        self.orientation = orientation
        self.location = location
  
    def getCoords(self) -> dict:
        return self.coordinates

    # def filled(self): # isInBoard(sel, board)
    #     for coords in self.coordinates:
    #         if board[coords['row']][coords['col']] == 1:
    #             return True
    #     return False

    def contains(self, location):
        """ If the ship has that board location (spot) """

        for coords in self.coordinates:
            if coords == location:
                return True
        return False
  
  
    def destroyed(self, board: list):
        for coords in self.coordinates:
            if board[ coords['row'] ][ coords['col'] ] == 'O':
                return False
            elif board[ coords['row'] ][ coords['col'] ] == '*':
                raise RuntimeError( "Board display inaccurate" )
        return True



class Board(object):
    board: list = []
    shipList: list = []
    rowSize: int
    colSize: int


    def __init__(self, size: int = 8, shipDesc: dict = None):
        if shipDesc:
            numShips = shipDesc['numShips']
            shipSizes = shipDesc['shipSizes']
            self.shipList = randomBoardShipList( numShips=numShips, sizes=shipSizes)
        else:
            numShips = int( size/2 )
            self.shipList = randomBoardShipList( numShips=numShips )
        self.shipList = randomBoardShipList( numShips=numShips )
        self.rowSize = size
        self.colSize = size
        
        self.board = [ ["0"] * self.col_size for x in range(self.row_size) ]
        self.fillBoard()
    

    def setShipCoord(self, coords: dict):
        self.board[ coords['row'] ][ coords['col'] ] = '1'
    

    def setShoot(self, shootCoords: dict):
        self.board[ coords['row'] ][ coords['col'] ] = '*'
    

    def setHit(self, shootCoords: dict):
        self.board[ coords['row'] ][ coords['col'] ] = 'X'


    def isSpotFilled(self, shipCoords: dict):
        for coords in shipCoords:
            if self.board[ shipCoords['row'] ][ shipCoords['col'] ] == '1':
                return True
        return False


    def fillBoard(self):
        for ship in self.shipList:
            ship: Ship = ship
            shipCoords = ship.getCoords()
            for coord in shipCoords:
                self.setShipCoord( coord )


    def __setNewShip(self):
        self.shipList.append( self.__getNewFreeShip() )

    def __getNewFreeShip(self):
        # orientation = ship.getOrientation() # TODO:
        # coordinates = ship.getCoords()
        # row_size -> self.rowSize
        # col_size -> self.colSize
        # size -> ship.getSize
        return randomShip(self.board)

        # if orientation == 'horizontal':
        #     if location['row'] in range(row_size):
        #         coordinates = []
        #         for index in range(size):
        #             if location['col'] + index in range(col_size):
        #                 self.coordinates.append({'row': location['row'], 'col': location['col'] + index})
        #             else:
        #                 raise IndexError("Column is out of range.")
        #     else:
        #         raise IndexError("Row is out of range.")
        # elif orientation == 'vertical':
        #     if location['col'] in range(col_size):
        #         self.coordinates = []
        #         for index in range(size):
        #             if location['row'] + index in range(row_size):
        #                 self.coordinates.append({'row': location['row'] + index, 'col': location['col']})
        #             else:
        #                 raise IndexError("Row is out of range.")
        #     else:
        #         raise IndexError("Column is out of range.")

        def __str__():
            pass # TODO:



###---###   UTILS   ###---###

def searchLocations(board: list, shipSize: int, orientation: str, rowSize: int, colSize: int):
    locations = []

    if orientation != 'horizontal' and orientation != 'vertical':
        raise ValueError("Orientation must have a value of either 'horizontal' or 'vertical'.")

    if orientation == 'horizontal':
        if shipSize <= colSize:
            for r in range(rowSize):
                for c in range(colSize - shipSize + 1):
                    if 1 not in board[r][c:c+shipSize]:
                        locations.append({'row': r, 'col': c})
    elif orientation == 'vertical':
        if shipSize <= rowSize:
            for c in range(colSize):
                for r in range(rowSize - shipSize + 1):
                    if 1 not in [board[i][c] for i in range(r, r+shipSize)]:
                        locations.append({'row': r, 'col': c})

    if not locations:
        return 'None'
    else:
        return locations


def randomShip(board: Board, size: int = None) -> Ship:
    """ Finds a free area for a Ship on a Board """"

    if not size:
        size = randint( MIN_SHIP_SIZE, MAX_SHIP_SIZE )
    orientation = 'horizontal' if randint(0, 1) == 0 else 'vertical'
    
    while locations == 'None':
        locations = searchLocations( board, size, orientation, board.rowSize, board.colSize)
    ship = Ship(size=size, orientation=orientation, location=locations)
    return ship

        return 'None'
    else:
        return {
            'location': locations[ randint( 0, len(locations) - 1 ) ],
            'size': size,
            'orientation': orientation
        }


def randomBoardShipList(numShips: int, sizes: list = None) -> list:
    """ Returns a random board """

    if len(sizes) != numShips:
        print('Does not have all ships sizes, gonna use random ones')
        sizes = None

    temp = 0
    board = []
    while temp < numShips:
        if sizes:
            shipInfo = randomShip( board, size=sizes[temp] )
        else:
            shipInfo = randomShip( board )
        
        if shipInfo == 'None':
            continue
        else:
            board.append(
                Ship( shipInfo['size'], shipInfo['orientation'], shipInfo['location'] )
            )
            temp += 1
    
    del temp
    return shipList


def shootOnBoar(board: list, shipList: list, shootCoords: dict) -> (bool, bool):
    shipHit = False
    shipDestroyed = False
    for ship in shipList:
        if ship.contains(shootCoords):
        shipHit = True
        # SE SHIP HIT FOR ACERTADO TEM QUE COLOCAR "X" NO TABULEIRO
        if ship.destroyed(board):
            shipDestroyed = True
            shipList.remove(ship)
        break
    
    return shipHit, shipDestroyed

    ## CADA USUARIO TEM QUE TER UM BOARD DISPLAY
    if not shipHit:
        board[ shootCoords['row'] ][ shootCoords['col'] ] = '*'
        print("You missed!")
    
    return board


def alreadyHasShooted(board: list, shootCoords: dict) -> bool:
    if board[ guess_coords['row'] ][ guess_coords['col'] ] == 'X' \
    or board[ guess_coords['row'] ][ guess_coords['col'] ] == '*':
        return True
    return False



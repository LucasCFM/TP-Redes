MAX_SHIP_SIZE = 5
MIN_SHIP_SIZE = 2


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


def randomLocation(board: list) -> Ship:
    size = randint( MIN_SHIP_SIZE, MAX_SHIP_SIZE )
    orientation = 'horizontal' if randint(0, 1) == 0 else 'vertical'
    ship = Ship

    locations = searchLocations( board, size, orientation )
    if locations == 'None':
        return 'None'
    else:
        return {
            'location': locations[ randint( 0, len(locations) - 1 ) ],
            'size': size,
            'orientation': orientation
        }


def randomBoard(numShips: int = 4) -> list:
    board = []
    while temp < numShips:
        shipInfo = randomLocation( board )
        if shipInfo == 'None':
            continue
        else:
            board.append(
                Ship( shipInfo['size'], shipInfo['orientation'], shipInfo['location'] )
            )
            temp += 1
    
    del temp
    return board


def isGoodShoot(board: list, shipList: list, shootCoords: dict) -> (bool, bool):
    shipHit = False
    shipDestroyed = False
    for ship in shipList:
        if ship.contains(shootCoords):
        True
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

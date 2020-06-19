import sys


RANDOM_BOARD_OPTION = 1
FILE_BOARD_OPTION = 2


def getClientParams():
    """ Gets the arguments of the command and set the server configs
        or uses the defaults ones if no is specified
    """

    try:
        serverHost = sys.argv[1]
    except IndexError:
        print(f'ERROR!! No server config was informed, gonna run on defaults')
        sys.exit()
    
    try:
        serverPort = sys.argv[2]
    except IndexError:
        print(f'ERROR!! No server config was informed, gonna run on defaults')
        sys.exit()
    
    return str(serverHost), int(serverPort)


def getBoardFromFile(filePath: str) -> list:
    f = open(filePath, "r")
    board f.read()
    return board


def printBoard(board: list):
    colSize = rowSize = len( board )
    
    print("\n  " + " ".join(str(x) for x in range(1, colSize + 1)))
    for r in range(rowSize):
        print(str(r + 1) + " " + " ".join(str(c) for c in board[r]))
    print()

def printBoards(boards: dict):
    print(f'-- SERVER --')
    printBoard( boards['server'] )
    print()
    print(f'-- CLIENT --')
    printBoard( boards['client'] )
    print()


def getShootCoordenates() -> (int, int):
    print(f"Digite a linha do tiro")
    row = int(float( input() ))
    
    print(f"Digite a coluna do tiro")
    col = int(float( input() ))

    return row, col


def printShootResults(shootResults: dict):
    if shootResults['success'] is True:
        print(f'ACERTOU! Seu tiro acertou um alvo')
    else:
        print(f'ERROU! Seu tiro foi no mar')


def getRestartOption():
    restartInput = input().strip()
    if not restartInput:
        return True # Nothing in input, RESTART
    return False # DO NOT RESTART


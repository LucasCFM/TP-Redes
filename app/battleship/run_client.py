import sys

from app.battleship.client.utils import (
    getClientParams, getBoardFromFile,
    printBoards, getShootCoordenates, printShootResults, getRestartOption
)

from app.battleship.client.tcp_client import Client


def printWelcomeMsg():
    print("""
Client Batalha Naval Iniciado!

Escolha:
1 - Para digitar o tamanho do tabuleiro
2 - Para ler o tabuleiro de um arquivo

    """)

def printWrongBoardInput():
    print("""

Opção inválida!!! Por favor digite uma das opições abaixo:
1 - Para digitar o tamanho do tabuleiro
2 - Para ler o tabuleiro de um arquivo

    """)


def printBattleEnded():
    print("""

A batalha terminou!

Aperte ENTER para TERMINAR;
Ou QUALQUER TECLA e ENTER para JOGAR NOVAMENTE

    """)


####===#### MAIN ####===####
serverHost, serverPort = getClientParams()
cnx = Client(serverHost=serverHost, serverPort=serverPort)

printWelcomeMsg()
while True:
    boardOption = int(float( input() ))
    if boardOption == RANDOM_BOARD_OPTION:
        cnx.setNewGame()
    elif FILE_BOARD_OPTION:
        board : list = getBoardFromFile()
        cnx.sendClientBoard()
    else:
        printWrongBoardInput()
        continue

    ended = False
    while not ended:
        boards = cnx.getBoardsFromServer()
        printBoards( boards )

        shootRow, shootCol = getShootCoordenates()
        shootResults = cnx.makeShoot( shootRow, shootCol )
        if shootResults['ended'] is True:
            break
        
        printShootResults( shootResults )

        boards = cnx.getBoardsFromServer()
        printBoards( boards )
    
    printBattleEnded()
    restart = getRestartOption()
    if not restart:
        sys.exit() # DO NOT RESTART, EXIT !!
    
    printWelcomeMsg()


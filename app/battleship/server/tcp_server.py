from random import randint

from app.battleship.server.models import Board, Ship, shootOnBoar, alreadyHasShooted



USERS = []
"""{
id = UUID = {
    
    userBoard = BOARD
    serverBoard = BOARD
}}
"""


class Server(object):
    connector: Connector = None


    def __init__(self, address: str = '127.0.0.1', port: int = 9000):
        self.connector = Connector(server_ip=address, server_port=port)


    def get_message(self):
        msg = self.connector.get_message()
        if not msg:
            return None, None
        
        msg_bytes, client_address = msg
        print(f'bytes Message received {msg_bytes}')
        print(f'client address {client_address}')

        return byte_to_json( msg_bytes ), client_address


    def send_msg_response(self, msg: dict, address: tuple):
        print(f'Sending json msg: {msg}')
        byte_msg = json_to_byte(msg)

        print(f'Sending msg: {byte_msg}')
        self.connector.send_msg( byte_msg=byte_msg, destiny_address=address )
    

    def send_success_response(self, address_tuple, msg = None):
        print(f'Sending confirmation message')
        response = {
            'success': True
        }
        if msg: response['msg'] = msg
        
        self.send_msg_response( response, address_tuple )
        print(f'Confirmation message sent')
    
    def send_error_response(self, address_tuple, msg = None):
        print(f'Sending confirmation message')
        response = {
            'success': False
        }
        if msg: response['msg'] = msg
        
        self.send_msg_response( response, address_tuple )
        print(f'Confirmation message sent')

    
    def setRandomBoard(self, userId: str, boardSize: int = 10):
        try:
            self.users[ userId ]
        except Exception:
            shipDesc = {
                'numShips': 10
                'shipSizes': [
                    5, 
                    4, 4, 
                    3, 3, 3, 
                    2, 2, 2, 2
                ]
            }
            self.users[ userId ] = {}
            userBoard = Board( boardSize, shipDesc )
            serverBoard = Board( boardSize, shipDesc )
            
            setUserBoard(userId, userBoard)
            setServerBoard(userId, serverBoard)
    

    def serverShoot(self, userId: str):
        shootCords = {
            'row': randint()
            'col': randint()
        }
        results = {
            'shootCoords': shootCords
            'hit' = False,
            'destroyed' = False,
            'valid' = True
        }
        userBoard = getUserBoard( userId )

        if alreadyHasShooted( userBoard, shootCords ):
            results['valid'] = 'Location (spot) has already been shot'
            return results

        shipHit, shipDestroyed = shootOnBoar( userBoard, shootCords )
        results['hit'] = shipHit
        results['destroyed'] = shipDestroyed
        if not shipHit and not shipDestroyed:
            userBoard.setShoot(shootCoords)
        if shipHit:
            userBoard.setHit(shootCoords)
        setUserBoard(userId, userBoard)
        return results
    
    def userShoot(self, userId: str, shootCords: dict):
        results = {
            'shootCoords': shootCords
            'hit' = False,
            'destroyed' = False,
            'valid' = True
        }
        serverBoard = getServerBoard( userId )

        if alreadyHasShooted( serverBoard, shootCords ):
            results['valid'] = 'Location (spot) has already been shot'
            return results
        
        shipHit, shipDestroyed = shootOnBoar( serverBoard, shootCords )
        results['hit'] = shipHit
        results['destroyed'] = shipDestroyed
        if not shipHit and not shipDestroyed:
            serverBoard.setShoot(shootCoords)
        if shipHit:
            serverBoard.setHit(shootCoords)
        setServerBoard(userId, serverBoard)
        return results
    

    def sendUserBoards(self, userId: str, clientAddress):
        boards = getUserBoards( userId )
        if boards:
            return self.send_success_response(clientAddress, boards)
        return self.send_error_response( clientAddress, 'Client has no boards' )
    

    def isGameEnded(self, userId: str) -< bool:
        boards = getUserBoards
        userBoard: Board = boards['client']
        serverBoard: Board = boards['server']
        
        userBoardDestroyed = False
        for ship in userBoard.shipList:
            ship: Ship = ship
            if not ship.destroyed(userBoard):
                break
            userBoardDestroyed = True
        
        serverBoardDestroyed = False
        for ship in serverBoard.shipList:
            ship: Ship = ship
            if not ship.destroyed(serverBoard):
                break
            serverBoardDestroyed = True
        
        if userBoardDestroyed or serverBoardDestroyed:
            return True
        return False
        



###---###   UTILS   ###---###
# BOARD_DISPLAY = [["O"] * col_size for x in range(row_size)]

def getUserBoards(userId: str) -> dict:
    global USERS
    try:
        user = USERS[userId]
    except Exception as e:
        print(f'ERROR !!! {e}')
        return None
    
    return {
        'client': str(user['userBoard']),
        'server': str(user['userBoard'])
    }

def getUserBoard(userId: str) -> Board:
    boards = getUserBoards()
    return boards['client']

def getServerBoard(userId: str) -> Board:
    boards = getUserBoards()
    return boards['server']


def setUserBoard(userId: str, board: Board):
    globals USERS
    USERS[ userId ]['userBoard'] = board

def setServerBoard(userId: str, board: Board):
    globals USERS
    USERS[ userId ]['serverBoard'] = board


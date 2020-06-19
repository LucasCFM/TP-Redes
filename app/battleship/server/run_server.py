from app.battleship.server.tcp_server import Server


def get_port() -> int:
    """ Gets the port to run the server """

    return int( sys.argv[1] )


port = get_port()
s = Server( port = port )


def setRandomBoardAction(msg: dict, clientAddress: tuple):
    clientId = msg['id']
    s.setRandomBoard( userId=clientId )
    s.send_success_response(address_tuple=clientAddress, msg='Your boards has been sat')


def setCustomBoardAction(msg: dict, clientAddress: tuple):
    clientId = msg['id']
    board = msg['board']
    s.setCustomBoard( userId=clientId, board=board )
    s.send_success_response(address_tuple=clientAddress, msg='Your boards has been sat')


def showBoardsAction(msg: dict, clientAddress: tuple):
    clientId = msg['id']
    s.sendUserBoards( userId=clientId, clientAddress=clientAddress )


def shootAction(msg: dict, clientAddress: tuple):
    clientId = msg['id']
    coordenates = msg['coordenates']
    shootCords = {
        'row': coordenates[0]
        'col' = coordenates[0]
    }
    userShootResult = s.userShoot(userId=clientId, shootCords=shootCords)
    if userShootResult['valid'] is True:
        serverShootResult = s.serverShoot( userId=clientId )
        while serverShootResult['valid'] is not True:
            serverShootResult = s.serverShoot( userId=clientId )
        s.send_success_response(address_tuple=clientAddress, msg='Your shoot has been done')
    
    else:
        s.send_error_response( clientAddress, msg=userShootResult['valid'] )


def invalidAction(clientAddress: tuple):
    s.send_error_response(address_tuple=clientAddress, msg='Invalid action')


def logMsg(msg: dict):
    print(f"""
Server received a new msg:
{msg}
    """)




while True:
    msg, clientAddress = s.get_message()
    logMsg(msg)
    msgAction = msg['action']

    if msgAction is SET_RANDOM_BOARD:
        setRandomBoardAction( msg, clientAddress )
    
    elif msgAction is SET_CUSTOM_BOARD:
        setCustomBoardAction( msg, clientAddress )
    
    elif msgAction is SHOW_BOARDS:
        showBoardsAction( msg, clientAddress )
    
    elif msgAction is SHOOT:
        shootAction( msg, clientAddress )
    
    else:
        invalidAction( clientAddress )


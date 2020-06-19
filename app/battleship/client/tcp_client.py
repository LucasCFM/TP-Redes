"""

A Client for Battleship game, built on top of TCP protocol

"""

from app.client.udp_connector import Connector

from uuid import uuid4

from random import randint


class Client(object):
    identifier = str( uuid4() )
    
    serverHost : str = None
    serverPort : int = None
    serverAddress : tuple = None
    connector : Connector = None


    def __init__(self, serverHost : str, serverPort : int):
        print(f'Strating client {self.identifier} for server {serverHost}:{serverPort}')
        self.serverHost = serverHost
        self.serverPort = serverPort
        self.serverAddress = (serverHost, serverPort)

        self.__connect()
        print(f'Battleship Client running')


    def __connect(self):
        self.connector = Connector(
            server_ip = self.serverHost, server_port = self.serverPort
        )


    def get_message(self) -> dict:
        print(f'Getting new message')
        try:
            msg = self.connector.get_message()
        except Exception:
            return False
        
        if not msg:
            print('No message has been received')
            return False
        
        return byte_to_json( msg )


    def send_msg(self, json_data: json):
        json_data['clientId' : self.identifier]

        print(f'Sending json msg: {json_data}')
        byte_msg = json_to_byte(json_data)

        print(f'Sending msg: {byte_msg}')
        self.connector.send_msg( byte_msg=byte_msg )
    

    ###---###   ACTIONS   ###---###
    def setNewGame(self, boardSize: int = None) -> (list, list):
        if not boardSize:
            boardSize = randint(1, 10)
        jsonMSG = {
            'action': 'newGame',
            'boardSize': boardSize
        }
        self.send_msg( json_data = jsonMSG )
        
        boardsJson = self.get_message()
        return boardsJson['client', 'server']
    
    
    def sendClientBoard(self, customBoard: list) -> (list, list):
        jsonMSG = {
            'action': 'newCustomGame',
            'clientBoard': customBoard
        }
        self.send_msg( json_data = jsonMSG )
        
        boardsJson = self.get_message()
        return boardsJson['client', 'server']


    def getBoardsFromServer(self) -> (list, list):
        jsonMSG = {
            'action': 'getBoards'
        }
        self.send_msg( json_data = jsonMSG )
        
        boardsJson = self.get_message()
        return boardsJson['client', 'server']


    def makeShoot(self, x: int, y: int) -> dict:
        jsonMSG = {
            'action': 'shoot',
            'coordenates': [x, y]
        }
        self.send_msg( json_data = jsonMSG )
        
        shootResults = self.get_message()
        return shootResults


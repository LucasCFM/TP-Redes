'''

        Client UPD connector

implements retransmission of messages sent

'''

import socket, json

from time import sleep

from app.utils.data import byte_to_json


bufferSize = 1024


# Create a UDP socket at client side

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))


class Connector():
    def __init__(self, server_ip: str, server_port: int):
        global UDPServerSocket
        
        self.server_ip = server_ip
        self.server_port = server_port
        UDPServerSocket.bind( (server_ip, server_port) )


    def change_server(self, server_ip: str, server_port: int):
        global UDPServerSocket
        
        self.server_address = (server_ip, server_port)
        UDPServerSocket.bind( self.server_address )
        
        print(f'Server changed to {self.server_address}')


    def set_timeout(self, timeout: float):
        global UDPServerSocket
        UDPServerSocket.settimeout(timeout)

    # TODO: Can split the function and make a send method and call send 2x inside it
    '''
    settimeout
    https://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
    '''
    def get_message(self, byte_msg: bytearray = None):
        global UDPServerSocket
        
        self.set_timeout(3.0)

        try:
            bytes_received = UDPServerSocket.recvfrom(bufferSize)
        except Exception as e:
            print('------ Exception while sending msg ------')
            print(e)
            print('retrying')
            return False
        msg_received = byte_to_json( bytes_received )
        print(f'Message received {msg_received}')
        return msg_received
    
    
    def send_msg(self, byte_msg: bytearray = None, destiny_address: tuple):
        global UDPServerSocket
        self.set_timeout(3.0)

        print(f'sending byte msg {byte_msg}')
        try:
            UDPServerSocket.sendto(byte_msg, destiny_address)
        except Exception as e:
            print('------ Exception while sending msg ------')
            print(e)
            print('retrying')
            self.set_timeout(3.0)
            try:
                UDPServerSocket.sendto(byte_msg, destiny_address)
            except Exception as e:
                print('------ Exception while sending msg ------')
                print(e)
            return False
        
        print('sent')
        self.set_timeout(3.0)
        try:
            byte_rsp = UDPServerSocket.recvfrom(bufferSize)
        except Exception as e:
            print('------ Exception while watting for server msg ------')
            print(e)
            return False
        
        json_data = byte_to_json( byte_rsp )
        if json_data['success'] == True:
            return True
        
        return False
    
    




        



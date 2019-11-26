'''

        Client UPD connector

implements retransmission of messages sent

'''

import socket, json

from time import sleep

from app.utils.data import byte_to_json


bufferSize = 1024


# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


class Connector():
    def __init__(self, server_ip: str, server_port: int):
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_address = (server_ip, server_port)
    

    def change_server(self, server_ip: str, server_port: int):
        self.server_address = (server_ip, server_port)
        print(f'Server changed to {self.server_address}')


    def set_timeout(self, timeout: float):
        global UDPClientSocket
        UDPClientSocket.settimeout(timeout)

    # TODO: Can split the function and make a send method and call send 2x inside it
    '''
    settimeout
    https://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
    '''
    def send_msg(self, byte_msg: bytearray = None):
        global UDPClientSocket
        self.set_timeout( 3.0 )

        print(f'sending byte msg {byte_msg}')
        try:
            UDPClientSocket.sendto(byte_msg, self.server_address)
        except Exception as e:
            print('------ Exception while sending msg ------')
            print(e)
            print('retrying')
            self.set_timeout(3.0)
            try:
                UDPClientSocket.sendto(byte_msg, self.server_address)
            except Exception as e:
                print('------ Exception while sending msg ------')
                print(e)
            return False
        
        print('sent')
        self.set_timeout(3.0)
        try:
            byte_rsp = UDPClientSocket.recvfrom(bufferSize)
        except Exception as e:
            print('------ Exception while watting for server msg ------')
            print(e)
            return False
        
        json_data = byte_to_json( byte_rsp )
        if json_data['success'] == True:
            return True
        
        return False

    
    




        



'''

        Client UPD connector

implements retransmission of messages sent

'''

import socket, json

from time import sleep

from app.utils.data import byte_to_json, json_to_byte


bufferSize = 1024


# Create a UDP socket at client side

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# UDPServerSocket.bind((localIP, localPort))


class Connector():
    def __init__(self, server_ip: str, server_port: int):
        global UDPServerSocket
        
        self.server_ip = server_ip
        self.server_port = server_port
        UDPServerSocket.bind( (server_ip, server_port) )


    '''
    settimeout
    https://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
    '''
    def set_timeout(self, timeout: float):
        global UDPServerSocket
        UDPServerSocket.settimeout(timeout)


    def send_msg(self, byte_msg: bytearray, destiny_address: tuple):
        
        
        global UDPServerSocket
        self.set_timeout(3.0)

        print(f'Sending byte msg: {byte_msg}')
        print(f'to address: {destiny_address}')
        try:
            UDPServerSocket.sendto(byte_msg, destiny_address)
        except Exception as e:
            print('------ Exception while sending msg ------')
            print(e)
            raise e


    def get_message(self):
        global UDPServerSocket
        
        self.set_timeout(3.0)
        try:
            bytes_received, client_addrs = UDPServerSocket.recvfrom(bufferSize)
        except Exception as e:
            print('------ Exception while getting msg ------')
            print(e)
            print('retrying')
            return
        print(f'bytes received {bytes_received}')
        
        self.send_msg_received_confirmation( address=client_addrs )

        return bytes_received
    

    def send_msg_received_confirmation(self, address : tuple):
        print(f'Sending confirmation message')
        confirmation_msg = {
            'success': True
        }
        confimationByteMsg : bytearray = json_to_byte( confirmation_msg )
        print(f'Sending ...')
        self.send_msg( confimationByteMsg, address )
        print(f'Confirmation message sent!')


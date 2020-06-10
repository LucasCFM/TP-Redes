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


    def change_server(self, server_ip: str, server_port: int):
        global UDPServerSocket
        
        self.server_address = (server_ip, server_port)
        UDPServerSocket.bind( self.server_address )
        
        print(f'Server changed to {self.server_address}')

    '''
    settimeout
    https://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
    '''
    def set_timeout(self, timeout: float):
        global UDPServerSocket
        UDPServerSocket.settimeout(timeout)


    def __send(self, byte_msg: bytearray, destiny_address: tuple):
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
        self.__send( confimationByteMsg, address )
        print(f'Confirmation message sent!')


    def send_msg(self, byte_msg: bytearray, destiny_address: tuple):
        """ Public method to send messages
        Implements retransmission of messages, sending another message if the first fails
        only returns False if both of them don't send properly 

        param: byte_message : byte representation of the message string
        param: destiny_address : address tuple that the message will be sent
        returns: bool : If message was successfully sent or it faild
        """
        
        print(f'Sending message')
        try:
            self.__send( byte_msg, destiny_address )
        except Exception:
            print(f'Could not send message properly')
            print(f'Retrying ....')

            try:
                self.__send( byte_msg, destiny_address )
            except Exception:
                print(f'Could not send message properly')
                print(f'Aborted !!')
                return False
        
        try:
            byte_rsp = self.get_message()
        except Exception:
            print(f'Could not get response properly')
            print(f'Aborted')
            return False
        
        json_data = byte_to_json( byte_rsp ) # ERROR - Maybe does not need to receive response on line 97 (up here)
        if json_data['success'] == True:
            return True
        
        return False


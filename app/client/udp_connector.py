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
        print(f'Running connectio on {self.server_address}')


    '''
    settimeout - https://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
    '''
    def __set_timeout(self, timeout: float):
        global UDPClientSocket
        UDPClientSocket.settimeout(timeout)


    def get_message(self) -> bytearray:
        """ Waits for a message from the server """
        
        print(f'Getting message from server')
        try:
            msg, address = UDPClientSocket.recvfrom(bufferSize)
        except Exception as e:
            print('------ Exception while watting for server msg ------')
            print(e)
            raise e
        print(f'Message received: {msg}')
        return msg
    

    def __send(self, byte_msg: bytearray, timeout: float = 3.0):
        global UDPClientSocket
        self.__set_timeout( timeout )

        print(f'Sending byte msg {byte_msg}')
        try:
            UDPClientSocket.sendto(byte_msg, self.server_address)
        except Exception as e:
            print('------ Exception while sending msg ------')
            print(e)
            raise e
        print(f' Message sent')
    
    
    def send_msg(self, byte_msg: bytearray = None):
        """ Public method to send messages
        Implements retransmission of messages, sending another message if the first fails
        only returns False if both of them don't send properly 

        param: byte_message : byte representation of the message string
        param: destiny_address : address tuple that the message will be sent
        returns: bool : If message was successfully sent or it faild
        """

        print(f'Sending message')
        try:
            self.__send( byte_msg )
        except Exception as e:
            print('Retrying ...')
            try:
                self.__send( byte_msg )
            except Exception as e:
                print(f'Could not send message properly. ABORTED IT')
                return False

        # Checks if message was successfuly gotten by server
        byte_rsp = self.get_message()
        json_data = byte_to_json( byte_rsp )
        if json_data['success'] is True:
            print(f'Server successfully responded')
            return True
        
        print(f'ERROR - Server did not respond')
        return False

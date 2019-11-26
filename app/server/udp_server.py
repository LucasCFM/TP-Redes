import socket

from app.utils.data import byte_to_json, json_to_byte
from app.utils.fuel import *

from app.db.utils import insert_fuel_registry, search_fuel_registry

from app.server.udp_connector import Connector


# https://pythontic.com/modules/socket/udp-client-server-example

 
# localIP     = "127.0.0.1"
# localPort   = 20001
# bufferSize  = 1024

# msgFromServer = "Hello UDP Client"
# bytesToSend = str.encode(msgFromServer)

# Create a datagram socket
# UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
# UDPServerSocket.bind((localIP, localPort))

# print("UDP server up and listening")

# Listen for incoming datagrams

# while(True):
#     bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    
#     message = bytesAddressPair[0]
#     address = bytesAddressPair[1]
#     clientMsg = "Message from Client:{}".format(message)
#     clientIP  = "Client IP Address:{}".format(address)
    
#     print(clientMsg)
#     print(clientIP)
#     # Sending a reply to client

#     UDPServerSocket.sendto(bytesToSend, address)




class Server():
    connector: Connector = None


    def __init__(self, address: str = '127.0.0.1', port: int = 9000):
        self.connector = Connector(server_ip=address, server_port=port)


    def get_message(self):
        msg = self.connector.get_message()
        print(f'Message received: {msg}')
        return byte_to_json( msg )


    def send_msg_response(self, msg: dict, address: tuple):
        print(f'Sending json msg: {msg}')
        byte_msg = json_to_byte(msg)

        print(f'Sending msg: {byte_msg}')
        self.connector.send_msg( byte_msg=byte_msg, destiny_address=address )


    def insert_fuel(self, fuel_type: int, fuel_price: float, station_lat: float, station_lon: float):
        insert_fuel_registry(
            station_lat=station_lat, station_lon=station_lon, 
            fuel_type=fuel_type, fuel_price=fuel_price
        )


    def insert_gasolina_price(self, fuel_price: float, station_lat: float, station_lon: float):
        print(f'Inserting gasosa: price: {fuel_price}, station_lat: {station_lat}, station_lon: {station_lon}')
        return self.insert_fuel(
            price = fuel_price, fuel_type = GASOLINA_FUEL_TYPE,
            station_lat=station_lat, station_lon=station_lon
        )

    def insert_alcool_price(self, fuel_price: float, station_lat: float, station_lon: float):
        print(f'Inserting alcool: price: {fuel_price}, station_lat: {station_lat}, station_lon: {station_lon}')
        return self.insert_fuel(
            price = fuel_price, fuel_type = ALCOOL_FUEL_TYPE,
            station_lat=station_lat, station_lon=station_lon
        )

    def insert_diesel_price(self, fuel_price: float, station_lat: float, station_lon: float):
        print(f'Inserting diesel: price: {fuel_price}, station_lat: {station_lat}, station_lon: {station_lon}')
        return self.insert_fuel(
            price = fuel_price, fuel_type = DIESEL_FUEL_TYPE,
            station_lat=station_lat, station_lon=station_lon
        )



    def search_fuel(self, fuel_type: int, search_raidus: float, center_lat: float, center_lon: float):
        search_fuel_registry(
            fuel_type=fuel_type, center_lat=center_lat, center_lon=center_lon, max_distance=search_raidus
        )


    def search_gasolina_price(self, search_raidus: float, center_lat: float, center_lon: float):
        print(f'Inserting diesel: center_lat: {center_lat}, center_lon: {center_lon}, radius: {search_raidus}')
        return self.search_fuel(
            fuel_type = GASOLINA_FUEL_TYPE, search_raidus=search_raidus,
            center_lat=center_lat, center_lon=center_lon
        )

    def search_alcool_price(self, search_raidus: float, center_lat: float, center_lon: float):
        print(f'Inserting diesel: center_lat: {center_lat}, center_lon: {center_lon}, radius: {search_raidus}')
        return self.search_fuel(
            fuel_type = ALCOOL_FUEL_TYPE, search_raidus=search_raidus,
            center_lat=center_lat, center_lon=center_lon
        )

    def search_diesel_price(self, search_raidus: float, center_lat: float, center_lon: float):
        print(f'Inserting diesel: center_lat: {center_lat}, center_lon: {center_lon}, radius: {search_raidus}')
        return self.search_fuel(
            fuel_type = DIESEL_FUEL_TYPE, search_raidus=search_raidus,
            center_lat=center_lat, center_lon=center_lon
        )





import json

from app.client.udp_connector import Connector
from app.utils.fuel import *
from app.utils.data import byte_to_json, json_to_byte


'''
https://pythontic.com/modules/socket/udp-client-server-example


# Send to server using created UDP socket

UDPClientSocket.sendto(bytesToSend, serverAddressPort)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)

msg = "Message from Server {}".format(msgFromServer[0])

print(msg)
'''


MSG_ID_COUNT = 0


class Client():
    connector: Connector = None
    name: str = ''


    def __init__(self, 
        client_name: str, 
        server_address: str = '127.0.0.1', server_port: int = 10000
    ):
        print(f'Strating client {client_name} for server {server_address}:{server_port}')
        self.name = client_name
        self.server_address = server_address
        self.server_port = server_port
        self.connect( server_address=server_address, server_port=server_port )


    def connect(self, server_address: str, server_port: int):
        self.connector = Connector(
            server_ip = server_address, server_port = server_port
        )


    def send_msg(self, json_data: json):
        print(f'Sending json msg: {json_data}')
        byte_msg = json_to_byte(json_data)

        print(f'Sending msg: {byte_msg}')
        self.connector.send_msg( byte_msg=byte_msg )



    #### --------- ACTIONS ---------
    ############ INSERT DATA PICE
    def send_fuel_price(self, price: float, fuel_type: int, station_lat: float, station_lon: float):
        global MSG_ID_COUNT

        data = {
            'type': INSERT_FUEL_PRICE_TYPE,
            'id': MSG_ID_COUNT,
            'fuel_type': fuel_type,
            'fuel_price': price,
            'station_lat': station_lat,
            'station_lon': station_lon
        }

        if self.send_msg( json_data=data ):
            MSG_ID_COUNT += 1
            return True
        return False
    

    def send_gasolina_price(self, price: float, station_lat: int, station_lon: int):
        print(f'Sending gasosa price: price: {price}, station_lat: {station_lat}, station_lon: {station_lon}')
        return self.send_fuel_price(
            price = price, fuel_type = GASOLINA_FUEL_TYPE,
            station_lat=station_lat, station_lon=station_lon
        )
    
    def send_alcool_price(self, price: float, station_lat: int, station_lon: int):
        print(f'Sending alcool price: price: {price}, station_lat: {station_lat}, station_lon: {station_lon}')
        return self.send_fuel_price(
            price = price, fuel_type = ALCOOL_FUEL_TYPE,
            station_lat=station_lat, station_lon=station_lon
        )
    
    def send_diesel_price(self, price: float, station_lat: int, station_lon: int):
        print(f'Sending diesel price: price: {price}, station_lat: {station_lat}, station_lon: {station_lon}')
        return self.send_fuel_price(
            price = price, fuel_type = DIESEL_FUEL_TYPE,
            station_lat=station_lat, station_lon=station_lon
        )


    ############ SEARCH PICE
    def search_fuel_price(self, fuel_type: int, search_radius: float, center_lat: float, center_lon: float):
        global MSG_ID_COUNT

        data = {
            'type': SEARCH_FUEL_PRICE_TYPE,
            'id': MSG_ID_COUNT,
            'fuel_type': fuel_type,
            'search_radius': search_radius,
            'center_lat': center_lat,
            'center_lon': center_lon
        }

        if self.send_msg( json_data=data ):
            MSG_ID_COUNT += 1
            return True
        return False
    
    def search_gasolina_price(self, search_radius: float, center_lat: float, center_lon: float):
        print(f'Search gasosa price: radius: {search_radius}, center_lat: {center_lat}, center_lon: {center_lon}')
        return self.search_fuel_price(
            fuel_type = GASOLINA_FUEL_TYPE, search_radius=search_radius,
            center_lat=center_lat, center_lon=center_lon
        )
    
    def search_alcool_price(self, search_radius: float, center_lat: float, center_lon: float):
        print(f'Search alcool price: radius: {search_radius}, center_lat: {center_lat}, center_lon: {center_lon}')
        return self.search_fuel_price(
            fuel_type = ALCOOL_FUEL_TYPE, search_radius=search_radius,
            center_lat=center_lat, center_lon=center_lon
        )
    
    def search_diesel_price(self, search_radius: float, center_lat: float, center_lon: float):
        print(f'Search diesel price: radius: {search_radius}, center_lat: {center_lat}, center_lon: {center_lon}')
        return self.send_fuel_price(
            fuel_type = DIESEL_FUEL_TYPE, search_radius=search_radius,
            center_lat=center_lat, center_lon=center_lon




        




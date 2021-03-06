import socket

from app.utils.data import byte_to_json, json_to_byte
from app.utils.fuel import *

from app.db.utils import insert_fuel_registry, search_fuel_registry

from app.server.udp_connector import Connector


class Server():
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


    def search_fuel(self, fuel_type: int, search_radius: float, center_lat: float, center_lon: float):
        return search_fuel_registry(
            fuel_type=fuel_type, center_lat=center_lat, center_lon=center_lon, max_distance=search_radius
        )


    def insert_fuel(self, fuel_type: int, fuel_price: float, station_lat: float, station_lon: float):
        return insert_fuel_registry(
            station_lat=station_lat, station_lon=station_lon, 
            fuel_type=fuel_type, fuel_price=fuel_price
        )

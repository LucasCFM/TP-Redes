import sys

from app.server.udp_server import Server

from app.utils.fuel import INSERT_FUEL_PRICE_TYPE, SEARCH_FUEL_PRICE_TYPE, GET_ALL_ENTRIES_TYPE



def get_port():
    """ Gets the port to run the server """

    return int( sys.argv[1] )
    

def get_msg_type(msg_dict: dict):
    """ Filter the msg type of a received msg """

    msg_type = msg_dict['type']
    if msg_type not in [INSERT_FUEL_PRICE_TYPE, SEARCH_FUEL_PRICE_TYPE]:
        return None
    return msg_type



if __name__ == '__main__':
    """ Runs a server instance on a specific port and listen to messages (insert or search actions) """

    server_port = get_port()
    s = Server( port=server_port )

    while True:
        msg, client_address = s.get_message()
        if not msg:
            continue
        print(f'Server has received a message: {msg}')
        s.send_success_response(client_address)
        print('Message confirmed to client')

        msg_type = get_msg_type(msg)
        if not msg_type:
            print('WARNING: Message has no type')
            continue

        if msg_type == INSERT_FUEL_PRICE_TYPE:
            s.insert_fuel(
                fuel_type=msg['fuel_type'], fuel_price=msg['fuel_price'],
                station_lat=msg['station_lat'], station_lon=msg['station_lon']
            )
            s.send_success_response(client_address, msg='Fuel has been successfully inserted')
        elif msg_type == SEARCH_FUEL_PRICE_TYPE:
            search_result = s.search_fuel(
                fuel_type=msg['fuel_type'], search_radius=msg['search_radius'],
                center_lat=msg['center_lat'], center_lon=msg['center_lon']
            )
            s.send_success_response(client_address, msg=search_result)
        else:
            print('Invalid message')





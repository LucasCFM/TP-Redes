import sys

from app.server.udp_server import Server



def get_port():
    """ Get the port to run the server """

    return int( sys.argv[1] )
    

def get_msg_type():
    """ Filter the msg type of a received msg """

    msg_type = msg['type']
    if msg_type not in [INSERT_OPT, SEARCH_OPT]:
        return None
    return msg_type



if __name__ == '__main__':
    """ Runs a server instance on a specific port """

    server_port = get_port()
    s = Server( port=server_port )

    while True:
        msg = s.get_message()
        if not msg:
            continue

        msg_type = get_msg_type(msg)
        if not msg_type:
            continue

        if msg_type == INSERT_OPT:
            s.insert_fuel(
                fuel_type=msg['fuel_type'], fuel_price=msg['fuel_price'],
                station_lat=msg['station_lat'], station_lon=msg['station_lon']
            )
        elif msg_type == SEARCH_OPT:
            s.search_fuel(
                fuel_type=msg['fuel_type'], search_radius=msg['search_radius'],
                center_lat=msg['center_lat'], center_lon=msg['center_lon']
            )
        else:
            print('Invalid message')





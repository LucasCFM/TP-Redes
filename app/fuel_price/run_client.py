import sys

from time import time

from app.client.udp_client import Client
from app.utils.fuel import *


EXIT_OPT = 0
INSERT_OPT = 1
SEARCH_OPT = 2


def get_server_config():
    """ Gets the arguments of the command and set the server configs
        or uses the defaults ones if no is specified
    """

    try:
        server_address = sys.argv[1]
    except IndexError:
        print(f'No server config was informed, gonna run on defaults')
        return None, None
    
    try:
        server_port = sys.argv[2]
    except IndexError:
        print(f'No server port was informed, \
                gonna run on default port and address: {server_address}')
        return server_address, None
    return str(server_address), int(server_port)


def get_request_type():
    print(f'')
    print(f'{EXIT_OPT} - Sair')
    print(f'{INSERT_OPT} - Inserir preco')
    print(f'{SEARCH_OPT} = Pesquisar preco')

    return int( input(f'Selecione uma opcao: ') )


def get_fuel_type():
    print(f'')
    print(f'{DIESEL_FUEL_TYPE} - Diesel')
    print(f'{ALCOOL_FUEL_TYPE} - Alcool')
    print(f'{GASOLINA_FUEL_TYPE} - Gasolina')

    return int( input(f'Selecione um combustivel: ') )


def get_fuel_price():
    """ Request the fuel price and get it (Integer repreesnting float with 3 decimal places) """
    print(f'')
    price = int( input(f'Digite o preco do combustivel: ') )
    return price/1000.0


def get_lat_lon():
    lat = 0.0
    lon = 0.0

    print(f'')
    lat = float( input(f'Digite uma latitude: ') )
    lon = float( input(f'Digite uma longitude: ') )

    return (lat, lon)


def get_radius():
    print(f'')
    return float( input(f'Digite o tamanho do raio (em km): ') )


def insert_data():
    fuel_type = get_fuel_type()
    fuel_price = get_fuel_price()
    lat, lon = get_lat_lon()
    
    if fuel_type == GASOLINA_FUEL_TYPE:
        confirmation = c.send_gasolina_price(fuel_price, lat, lon)
    elif fuel_type == DIESEL_FUEL_TYPE:
        confirmation = c.send_diesel_price(fuel_price, lat, lon)
    elif fuel_type == ALCOOL_FUEL_TYPE:
        confirmation = c.send_alcool_price(fuel_price, lat, lon)
    
    if confirmation:
        print('Dado foi inserido com sucesso')
    else:
        print('Erro ao inserir dado')

def search_data():
    fuel_type = get_fuel_type()
    radius = get_radius()
    lat, lon = get_lat_lon()

    if fuel_type == GASOLINA_FUEL_TYPE:
        result = c.search_gasolina_price(radius, lat, lon)
    elif fuel_type == DIESEL_FUEL_TYPE:
        result = c.search_diesel_price(radius, lat, lon)
    elif fuel_type == ALCOOL_FUEL_TYPE:
        result = c.search_alcool_price(radius, lat, lon)

    if result:
        print(f'Resultado da pesquisa: {result}')
    else:
        print('Erro ao pesquisar dado')


if __name__ == '__main__':
    """ Runs a client instance to connect on a server in a specific address and port """

    server_address, server_port = get_server_config()

    c = Client(f'teste {time()}', server_address, server_port)

    request_type = get_request_type()

    while request_type != EXIT_OPT:
        if request_type == INSERT_OPT:
            insert_data()
        
        elif request_type == SEARCH_OPT:
            search_data()
        
        else:
            print(f'Invalid request type: {request_type}')
        
        request_type = get_request_type()

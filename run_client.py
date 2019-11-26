
from time import time

from app.client.udp_client import Client
from app.utils.fuel import *


EXIT_OPT = 0
INSERT_OPT = 1
SEARCH_OPT = 2


def get_request_type():
    print(f'')
    print(f'{EXIT_OPT} - Sair')
    print(f'{INSERT_OPT} - Inserir preco')
    print(f'{SEARCH_OPT} = Pesquisar preco')

    return int( input(f'Selecione uma opcao ') )


def get_fuel_type():
    print(f'')
    print(f'{GASOLINA_FUEL_TYPE} - Gasolina')
    print(f'{ALCOOL_FUEL_TYPE} - Alcool')
    print(f'{DIESEL_FUEL_TYPE} - Diesel')

    return int( input(f'Selecione um combustivel ') )


def get_fuel_price():
    print(f'')
    price = int( input(f'Digite o preco do combustivel ') )
    return price/1000.0


def get_lat_lon():
    lat = 0.0
    lon = 0.0

    print(f'')
    lat = float( input(f'Digite uma latitude ') )
    lon = float( input(f'Digite uma longitude ') )

    return (lat, lon)


def get_radius():
    print(f'')
    return input(f'Digite o tamanho do raio ')


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

    result = c.search_fuel_price()

    if confirmation:
        print(f'Resultado: {result}')
    else:
        print('Erro ao pesquisar dado')


if __name__ == '__main__':
    """ Runs a client instance to connect on a server in a specific address and port """

    c = Client(f'teste {time()}')

    request_type = get_request_type()

    while request_type != EXIT_OPT:
        if request_type == INSERT_OPT:
            insert_data()
        
        elif request_type == SEARCH_OPT:
            search_data()
        
        else:
            print(f'Invalid request type: {request_type}')
        
        request_type = get_request_type()

    



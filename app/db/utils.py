from app.db import db
from app.db.models import Station, Fuel



def create_station(lat: float, lon: float):
    with db.atomic():
        Station.create(lat=lat, lon=lon)
    print(f'station created')


def get_all_statations():
    """ retrieves all stations """

    return Station.select()
    # Station.select().where()


def get_all_entries():
    print(f'ALL ENTRIES TEST: {Station.select().join(Fuel)}')
    return Station.select().join(Fuel)


def get_station_by_coordanates(lat: float, lon: float) -> Station:
    with db.atomic():
        station = (Station.select().where( 
            (Station.lat == lat) &
            (Station.lon == lon)
        ))
    return station



def insert_fuel_registry(station_lat: float, station_lon: float, fuel_type: int, fuel_price: float):
    """ Inserts or updates a fuel registry associated with a station """
    station = get_station_by_coordanates(station_lat, station_lon)
    if not station:
        print('Station does not exists yet, gonna create it')
        create_station( station_lat, station_lon )
        print(f'Station has been created')
        station = get_station_by_coordanates(station_lat, station_lon)
    
    print(f'Station: {station}')
    fuel = get_station_fuel( station, fuel_type )
    print(f'Insert-fuel fuel: {fuel}')

    if fuel:
        print(f'Station already has this fuel, gonna update its price')
        fuel.price = fuel_price
        fuel.save()
    else:
        print(f'Station does not have this fuel, creating it ...')
        fuel = Fuel.create(type=fuel_type, price=fuel_price, station=station)
    print(f'Fuel has been inserted/updated')


def get_all_fuels_by_station(station: Station):
    """ Gets all fuels registered on a station """

    return Fuel.select().where( Fuel.station == station )


def get_station_fuel(station: Station, fuel_type: int) -> Fuel:
    """ Gets a specific type fuel registered on a certain station """

    fuels = get_all_fuels_by_station(station)
    print(f'Station fuels: {fuels}')
    for fuel in fuels:
        if fuel.type == fuel_type:
            return fuel



def search_fuel_registry(fuel_type: int, center_lat: float, center_lon: float, max_distance: float):
    """ This method gets fuels prices in stations that are within a max distance from a point in earth """

    fuel_result = None
    
    stations = get_all_statations()
    print(f'All stattions: {stations}')
    for station in stations:
        station : Station = station
        station_distance_from_location = station.distance_from_location(lat=center_lat, lon=center_lon)
        if station_distance_from_location <= max_distance:
            fuel = get_station_fuel(station, fuel_type)
            if not fuel_result or fuel_result['price'] > fuel.price:
                fuel_result = {
                    'price': fuel.price,
                    'station': station.id
                }
    
    if fuel_result:
        return fuel_result




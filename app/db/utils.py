from app.db.models import Station, Fuel



def get_all_statations():
    """ retrieves all stations """

    return Station.select()
    # Station.select().where()



def insert_fuel_registry(station_lat: float, station_lon: float, fuel_type: int, fuel_price: float):
    """ Inserts or updates a fuel registry associated with a station """

    station = Station.get_or_create(
        Station.lat == station_lat, Station.lon == station_lon
    )
    print(f'Insert-fuel station: {station}')
    fuel = get_station_fuel( station )
    print(f'Insert-fuel fuel: {fuel}')
    if fuel:
        fuel.price = fuel_price
        fuel.save()
    else:
        fuel = Fuel(type=fuel_type, price=fuel_price, station=station)



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

    fuels = []
    
    stations = get_all_statations()
    print(f'All stattions: {stations}')
    for station in stations:
        station : Station = station
        station_distance_from_location = station.distance_from_location(lat=center_lat, lon=center_lon)
        if station_distance_from_location <= max_distance:
            fuel = get_station_fuel(station, fuel_type)
            fuel_dict = {
                'station': station.id,
                'fuel_price': fuel.price
            }
            fuels.append( fuel_dict )
    
    if fuels:
        return fuels




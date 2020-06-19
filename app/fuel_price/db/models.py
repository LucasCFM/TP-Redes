from math import radians, cos, sin, asin, sqrt, atan2

from peewee import *

from app.db import db


'''
https://github.com/coleifer/peewee
'''


class BaseModel(Model):
    class Meta:
        database = db


class Station(BaseModel):
    id = PrimaryKeyField(unique=True)

    lat = FloatField()
    lon = FloatField()
    
    
    def __str__(self):
        return f'{self.id} ({self.lat}, {self.lon})'
    

    def __hash__(self):
        return hash((self.__class__, self._get_pk_value()))
    
    @property
    def _hash(self):
        return self.__hash__()


    # https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    def distance_from_location(self, lat, lon):
        R = 6373.0

        lat1 = radians(self.lat)
        lon1 = radians(self.lon)
        lat2 = radians(lat)
        lon2 = radians(lon)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance
    
    
    def get_zero_distance(self):
        return self.get_distance( self.lat, self.lon )


    # https://stackoverflow.com/questions/42686300/how-to-check-if-coordinate-inside-certain-area-python
    # def distance_from_location(self, lat, lon):
    #     # convert decimal degrees to radians 
    #     lon1, lat1, lon2, lat2 = map(radians, [self.lon, self.lat, lon, lat])

    #     # haversine formula 
    #     dlon = lon2 - lon1
    #     dlat = lat2 - lat1
    #     a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    #     c = 2 * asin(sqrt(a)) 
    #     r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        
    #     return c * r


class Fuel(BaseModel):
    id = PrimaryKeyField(unique=True)

    type = IntegerField()
    price = FloatField()
    
    station = ForeignKeyField(Station, backref='fuels')

    def __hash__(self):
        return hash((self.__class__, self._get_pk_value()))
    
    @property
    def _hash(self):
        return self.__hash__()

    # def __init__(self, type: int = None, price: float = None, station: Station = None):
    #     print(f'Initiating fuel: type {type}, price {price}, station {station}')
    #     self.type = type
    #     self.price = price
    #     self.station = station





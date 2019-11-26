from peewee import *
import datetime


'''
https://github.com/coleifer/peewee
'''


db = SqliteDatabase('pratical.db')





from app.db.models import Station, Fuel


db.connect()
db.create_tables( [Station, Fuel] )



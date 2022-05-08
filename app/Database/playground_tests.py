from typing import Any
from app.Database.data_types import DateType, GeoPointType, IntegerType, StringType, UUIDType
from app.Database.users_db import Column, Database, GeoColumn, Table, dumbshit


# create new databse instance and initailize with credentials

def add_table_to_database(table: str, db: Database):
    # # add a new table to databse and select the new table
    db.add_table(table)

def initialize_table_with_fields(fields, table: Table):
    cols = []

    # # prepare columns to add to table
    for field in fields:
        if field['key'] == 'location':
            cols.append(GeoColumn(key=field['key'],type=field['type']))
        else:
            cols.append(Column(key=field['key'],type=field['type']))
    
        # initialize selected table with the column properties
    table.initialize_table(cols)


def add_record_to_table(records: list[dict[str, Any]], table: Table):
    
    # add new data to the created columns
    for record in records:
        cols = []
        for key in record:
            if key == 'location':
                cols.append(GeoColumn(key=key, longitude=record[key]['longitude'], latitude=record[key]['latitude']))
            else:
                cols.append(Column(key=key, value=record[key]))

        table.insert_column(cols)


def select_table_field(table: Table):
    hands = table.select('location')
    print('Table: ',hands)

setup_table = [
    {
        'key': 'id',
        'type': IntegerType(not_null=True, primary_key=True, auto_increase=True)
    },
    {
        'key': 'date',
        'type': DateType( not_null=True )
    },
    {
        'key':'name',
        'type': StringType(length=50, not_null=True)
    },
    {
        'key': 'height',
        'type': StringType(length=50, not_null=True)
    },
    {
        'key': 'location',
        'type': GeoPointType(not_null=True)
    },
    {
        'key': 'uuid',
        'type': UUIDType(not_null=True, default=True)
    }
]

users = [
    {
        'name': "Farah J Fresh",
        'height': "15",
        'date': "1996-08-16",
        'location': {
            'longitude': 69.3504869,
            'latitude':24.9104797
        }

    },
    {
        'name': "Samuel Damilola Atiku",
        'height': "18.3",
        'date': "1998-11-6",
        'location': {
            'longitude': 29.3504669,
            'latitude':14.9107797
        }

    }
]


db = Database(host="localhost", database="test", user="postgres", password="admin")
add_table_to_database('hands', db)
table: Table = db.select_table('hands')
initialize_table_with_fields(setup_table, table )
# name = table.get_field_value('name', 'name', 'Farah J Fresh' )
print(table.select('name'))
add_record_to_table(users, table)
# print(f'Users Name is {name}')

# commit changes to database
db.commit()
db.close_cursor()
db.close()
# playground ---END
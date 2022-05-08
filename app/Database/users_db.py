from calendar import day_abbr
from operator import indexOf
from typing import Any
from colorama import Cursor
import psycopg2 as postgres
from ppygis3 import Point, LineString, Geometry
from app.Database.data_types import DataType, GeoPointType


SRID_WGS84 = 4326


def dumbshit():
    cur = postgres.connect(host="localhost", database="test", user="postgres", password="admin")
    cursor = cur.cursor()
    # cursor.execute('INSERT INTO hands (date, name, height, location) VALUES ( %s, %s, %s, %s)',("1975-01-01", "mathew sith", "3", Point(69.3504869,24.9104797)))
    # hands = cursor.fetchall()
    # print(f'HANDS {hands}')
    # cursor.execute('CREATE TABLE books (id SERIAL PRIMARY KEY, title varchar (150) NOT NULL, author varchar (50) NOT NULL, pages_num integer NOT NULL, review text, date_added date DEFAULT CURRENT_TIMESTAMP);')

    # cursor.execute('INSERT INTO books (title, author, pages_num, review)'
    #         'VALUES (%s, %s, %s, %s)',
    #         ('A Tale of Two Cities',
    #          'Charles Dickens',
    #          489,
    #          'A great classic!')
    #         )


    # cursor.execute('INSERT INTO books (title, author, pages_num, review)'
    #             'VALUES (%s, %s, %s, %s)',
    #             ('Anna Karenina',
    #             'Leo Tolstoy',
    #             864,
    #             'Another great classic!')
    #             )
    cur.commit()
    cursor.close()
    cur.close()


def extract_keys_values(arr):
    """
        Extract key and values from Column object and return them as coma seperated strings
        e.g. "key1, key2, key3" and "value1, value2, value3" for insert query. 
        
        example : 
        INSERT INTO table1 (key1, key2, key3) VALUES (value1, value2, value3)

        used in Table.insert_column method
    """
    keys = ""
    op = ''
    values = []
    for i in range(0, len(arr)):
        keys += arr[i].key 
        if arr[i].type:
            keys += ' '+arr[i].type.value
        
        # if arr[i].type == GeoPointType().type and not values == None:


        keys +=  ', ' if len(arr) > 1 and not i+1 == len(arr) else ''
        op += '%s'
        op +=  ', ' if len(arr) > 1 and not i+1 == len(arr) else ''
        if hasattr(arr[i], 'longitude')  and hasattr(arr[i], 'latitude'):
            point = Point(arr[i].longitude, arr[i].latitude)
            point.srid = SRID_WGS84
            arr[i].value = point
        values.append(arr[i].value) 
       
    return keys, tuple(values), op





class Column:
    def __init__(self, key,  type: DataType=None, primary_key=False, serial: bool = False, value: Any = None):
        """
            Create a new table column instance

            for new columns specify:
                    Column(
                            key="column_name", 
                            type=One_OF_Datatype_Types( see data_type.py ),
                            primary_key: bool = default is False,
                            serial: bool = default is False (use for Integer fields),
                             )
            to add to existing table:
                    Columns(
                        key="column_name",
                        value="value to be added"
                    )
        """
        self.key = key
        self.value = value
        self.primary_key = primary_key
        self.type = type
        self.serial = serial

    


class GeoColumn(Column):
    def __init__(self, key, primary_key=False, value=None, type: GeoPointType = None, longitude: float=None, latitude: float=None):
        if longitude and latitude:
            self.value = None
        else:
            self.value = value

        self.key = key
        self.type = type
        self.primary_key = primary_key
        self.longitude = longitude
        self.latitude = latitude


class Table:
    def __init__(self, name, cursor=None):
        """
            create a new table instance
        """
        self.cursor = cursor
        self.name = name

    def execute(self, *args):
        """
            Execute your query on the selected table
        """
        try:
            return self.cursor.execute(*args)
        except Exception as e:
            raise e

    def insert_column(self, column: list):
        '''
        formulate insert query 
        returns strin in the format:
        INSERT INTO table_name (column1, column2, column3,..,column(n)) VALUES (value(1), value(2), value(3),...,value(n))
        '''
        # extract key value pairs
        keys, values, op = extract_keys_values(column)

        # TESING - printing query
        print(f'INSERT INTO {self.name} ({keys}) VALUES ({op}))' % values)

        # execute insert query
        query = self.execute(f'INSERT INTO {self.name} ({keys}) VALUES ({op})', values)
        return query
    
    def initialize_table(self, column: list):
        keys, values, op = extract_keys_values(column)

        self.execute(f'DROP TABLE IF EXISTS {self.name};')
        query = f'CREATE TABLE {self.name} ({keys});'
        return self.execute(query, values)


    def select(self, keys: str = None):
        key = keys
        if not keys:
            key = '*'
        query = f'SELECT {key} FROM {self.name};'
        print(query)
        self.execute(query)
        return self.cursor.fetchall()
    
    def get_field_value(self, row, field, field_value):
        query = f'SELECT name from {self.name} WHERE name = %(fv)s;'
        self.execute(query, {'r': row, 'f': field, 'fv': field_value})
        return self.cursor.fetchall()

    


class Database:
    def __init__(self, **kwargs):
        """
            initialize with credentails:
            Database(
                host=your_host_url,
                database=your_database_name,
                user=your_database_user_name,
                password=your_database_password
            )
        """
        self.db = self.__initialize(host=kwargs['host'], db=kwargs['database'], user=kwargs['user'], password=kwargs['password'])
        self.cursor = self.db.cursor()
        self.table = {}


    def __initialize(self, host, db, user, password):
        """
            establish connection to database
        """
        return postgres.connect(host=host, database=db, user=user, password=password)



    def add_table(self, name) -> dict[str, Table]:
        """
            add new tables to database
            returns a dict [table_name, Table instance]
        """
        self.table[name] =  Table(name, self.cursor)

    def select_table(self, name: str):
        self.table[name] = Table(name, self.cursor)
        return self.table[name]
    
    def commit(self):
        """
            commit changes to database
        """
        return self.db.commit()
    

    def close_cursor(self):
        """
            detatch cursor
        """
        self.cursor.close()


    def close(self):
        """
            close connection to database
        """
        self.db.close()

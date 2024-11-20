from psycopg2 import connect
import pandas as pd


from .encrypt_decrypt_data import decrypt

from configparser import ConfigParser
config_object = ConfigParser()
config_object.read("./processing_modules/config.ini")
db_config = config_object['DBCONFIG']

database = decrypt(db_config['dbname'])
host     = decrypt((db_config['host']))
user     = decrypt(db_config['user'])
password = decrypt(db_config['password'])
port     = db_config['port']


# print(database,user,password,host,port)
def dbconn():
    return connect(database=database, user=user, password=password,host= host,port = port) 
    

def db_insert(query):
    with connect(database=database, user=user, password=password,host= host,port = port) as conn:
        status = True 
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.close()
        conn.commit()
        return status

def db_fetch(query):
    with connect(database=database, user=user, password=password,host= host,port = port) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        out = cursor.fetchone()
        cursor.close()
        conn.commit()
    return out


def db_fetch_content(query):
    with connect(database=database, user=user, password=password,host= host,port = port) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        out = cursor.fetchall()
        
        cursor.close()
        conn.commit()
    return out


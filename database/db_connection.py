import psycopg2
from pymongo import MongoClient

def get_rds_source_conn():
    # Define the connection parameters
    db_params = {
        'dbname': 'ecommerce_source_db', #database Name
        'user': 'postgres', #database username
        'password': 'admin', # database password
        'host': 'localhost',  # or the IP address of the database server
        'port': '5432'  # default PostgreSQL port
    }
    return db_params

def get_rds_destination_conn():
    db_connection_str = 'postgresql://postgres:admin@localhost:5432/ecommerce_destination_db'
    return db_connection_str

def get_mango_db_connection():
    client = MongoClient('mongodb://localhost:27017/')
    return client
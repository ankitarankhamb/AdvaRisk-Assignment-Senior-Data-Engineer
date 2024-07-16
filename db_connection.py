import psycopg2

def get_db_connection():
    # Define the connection parameters
    db_params = {
        'dbname': 'ecommerce', #db Name
        'user': 'postgres', #db username
        'password': 'admin', # db password
        'host': 'localhost',  # or the IP address of the database server
        'port': '5432'  # default PostgreSQL port
    }
    return db_params


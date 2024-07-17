import os
import sys
import psycopg2
import pandas as pd
from sqlalchemy import create_engine


# Database connection parameters
current_path = os.getcwd()
db_conn_directory = os.path.join(current_path, "ETL", "database")
if db_conn_directory not in sys.path:
    sys.path.append(db_conn_directory)

mail_directory = os.path.join(current_path, "ETL", "email_notifications")
if mail_directory not in sys.path:
    sys.path.append(mail_directory)

from db_connection import get_rds_source_conn
from db_connection import get_rds_destination_conn
from send_email import send_error_email


def extract_data():
    try:
        # Establish the connection
        db_params = get_rds_source_conn()
        conn = psycopg2.connect(**db_params)
        print("Connection to the database established successfully.")
        # List of table names
        tables = ['customers', 'orders', 'order_items', 'products', 'categories', 'reviews']
        # Example query
        for table in tables:
            #Get source data as per incremental logic on the basis of date if data is huge while doing staging
            query = f'SELECT * FROM {table}' 
            df = pd.read_sql(query, conn)
            #Perform  necessary data cleaning, handling missing values, duplicates
            df.fillna('', inplace=True) # Handling missing values (assuming no specific handling instructions)
            df.drop_duplicates(inplace=True) #drop duplicates from dataframe
            db_connection_str=get_rds_destination_conn()
            engine = create_engine(db_connection_str)
            df.to_sql(table, con=engine, index=False, if_exists='replace')
        print("Staging data load completed ")  
    except Exception as e:
        print(f"An error occurred: {e}")
        #Send an email to the development team if the job fails, including the cause of the failure
        error_message = str(e)
        sender_email = 'ankitarankhamb98@gmail.com'
        receiver_email = 'ankitarankhamb98@gmail.com'
        subject = 'E-commerce Data Extraction ETL Script Failure'
        send_error_email(error_message, sender_email, receiver_email,subject)
        sys.exit()
    finally:
        if conn:
            conn.close()

staging_data = extract_data()

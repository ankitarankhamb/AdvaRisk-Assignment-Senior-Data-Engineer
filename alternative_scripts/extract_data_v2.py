import os
import sys
import psycopg2
import pandas as pd

# Database connection parameters
current_path = os.getcwd()
db_conn_directory = os.path.join(current_path, "ETL", "database")
if db_conn_directory not in sys.path:
    sys.path.append(db_conn_directory)

mail_directory = os.path.join(current_path, "ETL", "email_notifications")
if mail_directory not in sys.path:
    sys.path.append(mail_directory)

# Directory where CSV files are stored
csv_directory = os.path.join(current_path, "ETL", "database", "data")
if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)

from db_connection import get_rds_db_connection
from send_email import send_error_email

def extract_data():
    try:
        # Establish the connection
        db_params = get_rds_db_connection()
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
            #Save the cleaned data for further use into any database or file
            file_path = f"{csv_directory}/{table}.csv"
            df.to_csv(file_path, index=False)
            print(f"Data from {table} extracted, cleaned, and saved to {table}.csv")
        return df 
    except Exception as e:
        print(f"An error occurred: {e}")
        #Send an email to the development team if the job fails, including the cause of the failure
        error_message = str(e)
        sender_email = 'ankitarankhamb98@gmail.com'
        receiver_email = 'ankitarankhamb98@gmail.com'
        subject = 'E-commerce Data Extraction ETL Script Failure'
        send_error_email(error_message, sender_email, receiver_email,subject)
        return None
    finally:
        if conn:
            conn.close()

staging_data = extract_data()

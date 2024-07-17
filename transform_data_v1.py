import os
import sys
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

current_path = os.getcwd()
# Directory where email notification will send if failure
mail_directory = os.path.join(current_path, "ETL", "email_notifications")
if mail_directory not in sys.path:
    sys.path.append(mail_directory)

# Database connection parameters
db_conn_directory = os.path.join(current_path, "ETL", "database")
if db_conn_directory not in sys.path:
    sys.path.append(db_conn_directory)

from db_connection import get_rds_destination_conn
from send_email import send_error_email

def transform_data():
    try:
        db_connection_str=get_rds_destination_conn()
        conn = create_engine(db_connection_str)
        # Define SQL queries for joins and aggregations
        query = '''
            SELECT
                c.customer_id,
                c.name,
                c.email,
                c.country,
                COALESCE(SUM(o.total_amount), 0) AS total_amount_spent,
                COUNT(DISTINCT o.order_id) AS total_orders,
                COALESCE(AVG(o.total_amount), 0) AS average_amount_spent,
                COUNT(DISTINCT oi.product_id) AS total_products_ordered,
                COALESCE(AVG(CAST(r.rating AS Decimal)), 0) AS average_rating
            FROM
                customers c
            LEFT JOIN
                orders o ON c.customer_id = o.customer_id
            LEFT JOIN
                order_items oi ON o.order_id = oi.order_id
            LEFT JOIN
                products p ON oi.product_id = p.product_id
            LEFT JOIN
                categories cat ON p.category_id = cat.category_id
            LEFT JOIN
                reviews r ON p.product_id = cast(r.product_id as int) AND c.customer_id = cast(r.customer_id as int)
            GROUP BY
                c.customer_id, c.name, c.email, c.country;
        '''
        aggregated_df = pd.read_sql_query(query, conn)
        aggregated_df = aggregated_df.round({'total_amount_spent': 2, 'average_amount_spent': 2})
        db_connection_str=get_rds_destination_conn()
        engine = create_engine(db_connection_str)
        aggregated_df.to_sql('ecommerce_transform_data', con=engine, index=False, if_exists='replace')
        return aggregated_df 
    except Exception as e:
        print(f"An error occurred: {e}")
        #Send an email to the development team if the job fails, including the cause of the failure
        error_message = str(e)
        sender_email = 'ankitarankhamb98@gmail.com'
        receiver_email = 'ankitarankhamb98@gmail.com'
        subject = 'E-commerce Data Extraction ETL Script Failure'
        send_error_email(error_message, sender_email, receiver_email,subject)
        sys.exit()

transformation_data = transform_data()
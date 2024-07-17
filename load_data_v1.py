import os
import sys
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from pymongo import MongoClient

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

def load_data():
    try:
        db_connection_str=get_rds_destination_conn()
        conn = create_engine(db_connection_str)
        # Get top 5 customers by total amount spent
        top_customers='''SELECT
                c.customer_id,
                c.name,
                c.email,
                c.country,
                COALESCE(SUM(o.total_amount), 0) AS total_amount_spent
            FROM
                customers c
            LEFT JOIN
                orders o ON c.customer_id = o.customer_id
            GROUP BY
                c.customer_id, c.name, c.email, c.country
            ORDER BY
                total_amount_spent DESC
            LIMIT 5; '''
        top_customers_df = pd.read_sql_query(top_customers, conn)
        # Get top 5 products
        top_products ='''SELECT
            p.product_id,
            p.product_name,
            COUNT(oi.order_id) AS order_count
        FROM
            products p
        LEFT JOIN
            order_items oi ON p.product_id = oi.product_id
        GROUP BY
            p.product_id, p.product_name
        ORDER BY
            order_count DESC
        LIMIT 5;
        '''
        top_products_df = pd.read_sql_query(top_products , conn)
        # Get average rating by category
        avg_rating_category ='''SELECT
            cat.category_name,
            COALESCE(AVG(CAST(r.rating AS Decimal)), 0) AS average_rating
        FROM
            categories cat
        LEFT JOIN
            products p ON cat.category_id = p.category_id
        LEFT JOIN
            reviews r ON p.product_id = CAST(r.product_id AS int)
        GROUP BY
            cat.category_name
        ORDER BY
            average_rating DESC;
        '''
        avg_rating_category_df = pd.read_sql_query(avg_rating_category , conn)
        # Calculate monthly sales trend
        monthly_sales ='''SELECT
            DATE_TRUNC('month', o.order_date) AS month_year,
            SUM(o.total_amount) AS total_sales
        FROM
            orders o
        GROUP BY
            DATE_TRUNC('month', o.order_date)
        ORDER BY
            month_year;
        '''
        monthly_sales_df = pd.read_sql_query(monthly_sales , conn)
        # Calculate monthly sales trend
        aggregated_query ='''SELECT
            e.customer_id,
            e.name,
            e.country,
            e.total_amount_spent,
            e.total_orders,
            e.average_amount_spent,
            e.total_products_ordered,
            e.average_rating
        FROM
            ecommerce_transform_data e
            ;
        '''
        aggregated_df = pd.read_sql_query(aggregated_query , conn)
        # Connect to MongoDB
        client = get_mango_db_connection()
        db = client['ecommerce_insights']
        # Define collections
        aggregated_data_collection = db['aggregated_data']
        insights_collection = db['insights']
        # Data models
        aggregated_data_model = aggregated_df.to_dict('records')
        insights_model = {
            'top_customers': top_customers_df.to_dict('records'),
            'top_products': top_products_df.to_dict('records'),
            'average_rating_by_category': avg_rating_category_df.to_dict('records'),
            'monthly_sales': monthly_sales_df.to_dict('records')
        }
        
        # Insert data into MongoDB
        aggregated_data_collection.insert_many(aggregated_data_model)
        insights_collection.insert_one(insights_model)
        # Close MongoDB connection
        client.close()
        print("Data loaded into MongoDB successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        #Send an email to the development team if the job fails, including the cause of the failure
        error_message = str(e)
        sender_email = 'ankitarankhamb98@gmail.com'
        receiver_email = 'ankitarankhamb98@gmail.com'
        subject = 'E-commerce Data Extraction ETL Script Failure'
        send_error_email(error_message, sender_email, receiver_email,subject)
        sys.exit()

load_data=load_data()
import os
import sys
import psycopg2
import pandas as pd
from pymongo import MongoClient

current_path = os.getcwd()
# Directory where email notification will send if failure
mail_directory = os.path.join(current_path, "ETL", "email_notifications")
if mail_directory not in sys.path:
    sys.path.append(mail_directory)

# Directory where CSV files are stored
csv_directory = os.path.join(current_path, "ETL", "database", "data")
if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)

# Database connection parameters
from db_connection import get_rds_db_connection
from db_connection import get_mango_db_connection
from send_email import send_error_email

def load_data(csv_directory):
    try:
        # Read CSV files into Pandas DataFrames
        customers_df = pd.read_csv(f"{csv_directory}/customers.csv")
        orders_df = pd.read_csv(f"{csv_directory}/orders.csv")
        order_items_df = pd.read_csv(f"{csv_directory}/order_items.csv")
        products_df = pd.read_csv(f"{csv_directory}/products.csv")
        categories_df = pd.read_csv(f"{csv_directory}/categories.csv")
        reviews_df = pd.read_csv(f"{csv_directory}/reviews.csv")
        transform_df = pd.read_csv(f"{csv_directory}/transform_data.csv")
        # Merge customer and  tables
        merged_df = pd.merge(customers_df, orders_df, on='customer_id')
        merged_df = pd.merge(merged_df, order_items_df, on='order_id')
        # Calculate total amount spent by each customer
        customer_spending = merged_df.groupby(['customer_id', 'name'])['total_amount'].sum().reset_index()
        # Get top 5 customers by total amount spent
        top_customers = customer_spending.nlargest(5, 'total_amount')
        # Calculate number of orders per product
        product_orders = merged_df.groupby(['product_id', 'product_name'])['order_id'].nunique().reset_index()
        # Get top 5 products by number of orders
        top_products = product_orders.nlargest(5, 'order_id')
        # Merge products with categories and reviews
        products_reviews_df = pd.merge(products_df, reviews_df, on='product_id')
        products_reviews_categories_df = pd.merge(products_reviews_df, categories_df, on='category_id')
        # Calculate average rating by category
        avg_rating_by_category = products_reviews_categories_df.groupby('category_name')['rating'].mean().reset_index()
        # Convert order_date to datetime
        orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
        # Calculate monthly sales trend
        monthly_sales = orders_df.resample('M', on='order_date')['total_amount'].sum().reset_index()
        # Connect to MongoDB
        client = get_mango_db_connection()
        db = client['ecommerce_insights']
        # Define collections
        transformed_data_collection = db['transformed_data']
        insights_collection = db['insights']
        # Data models
        transformed_data_model = transform_df.to_dict('records')
        insights_model = {
            'top_customers': top_customers.to_dict('records'),
            'top_products': top_products.to_dict('records'),
            'average_rating_by_category': avg_rating_by_category.to_dict('records'),
            'monthly_sales': monthly_sales.to_dict('records')
        }
        
        # Insert data into MongoDB
        transformed_data_collection.insert_many(transformed_data_model)
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
        return None

load_data=load_data(csv_directory)
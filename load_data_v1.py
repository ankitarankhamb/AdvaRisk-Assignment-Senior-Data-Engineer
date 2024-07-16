import pandas as pd
import os
from pymongo import MongoClient

# Directory where CSV files are stored
csv_directory = "/Users/DELL/Desktop/ETL/Data/"

def load_data(csv_directory):
    try:
        # Read CSV files into Pandas DataFrames
        customers_df = pd.read_csv(f"{csv_directory}/customers.csv")
        orders_df = pd.read_csv(f"{csv_directory}/orders.csv")
        order_items_df = pd.read_csv(f"{csv_directory}/order_items.csv")
        products_df = pd.read_csv(f"{csv_directory}/products.csv")
        categories_df = pd.read_csv(f"{csv_directory}/categories.csv")
        reviews_df = pd.read_csv(f"{csv_directory}/reviews.csv")
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
        monthly_sales_trend = orders_df.resample('M', on='order_date')['total_amount'].sum().reset_index()
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['ecommerce_insights']
        # Convert DataFrames to dictionaries for MongoDB insertion
        top_customers_dict = top_customers.to_dict(orient='records')
        top_products_dict = top_products.to_dict(orient='records')
        avg_rating_by_category_dict = avg_rating_by_category.to_dict(orient='records')
        monthly_sales_trend_dict = monthly_sales_trend.to_dict(orient='records')
        # Insert data into MongoDB collections
        db['top_customers'].insert_many(top_customers_dict)
        db['top_products'].insert_many(top_products_dict)
        db['avg_rating_by_category'].insert_many(avg_rating_by_category_dict)
        db['monthly_sales_trend'].insert_many(monthly_sales_trend_dict)
        # Close MongoDB connection
        client.close()
        print("Data loaded into MongoDB successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        error_message = str(e)
        #Send an email to the development team if the job fails, including the cause of the failure
        sender_email = 'ankitarankhamb98@gmail.com'
        receiver_email = 'ankitarankhamb98@gmail.com'
        subject = 'E-commerce Load ETL Script Failure'
        body = f'Dear Team,\n\nThe E-commerce Load ETL Script has encountered an error:\n\nError Message: {error_message}\n\nPlease investigate and take necessary actions.\n\nRegards,\nETL Team'
        command = f'echo "{body}" | mail -s "{subject}" {receiver_email}'
        os.system(command)
        print("Email sent successfully!")
        return None
import pandas as pd
import os

# Directory where CSV files are stored
csv_directory = "/Users/DELL/Desktop/ETL/Data/"

def load_staging_data(csv_directory):
    try:
        # Read CSV files into Pandas DataFrames
        customers_df = pd.read_csv(f"{csv_directory}/customers.csv")
        orders_df = pd.read_csv(f"{csv_directory}/orders.csv")
        order_items_df = pd.read_csv(f"{csv_directory}/order_items.csv")
        products_df = pd.read_csv(f"{csv_directory}/products.csv")
        categories_df = pd.read_csv(f"{csv_directory}/categories.csv")
        reviews_df = pd.read_csv(f"{csv_directory}/reviews.csv")
        
        # Perform joins and aggregation as needed
        # Merge orders dataframe with order_items  dataframe using inner join
        merged_df = pd.merge(orders_df, order_items_df, on='order_id', how='left')
        
        # Merge with products dataframe using inner join
        merged_df = pd.merge(merged_df, products_df, on='product_id', how='left')
        
        # Merge with customers dataframe using inner join
        merged_df = pd.merge(merged_df, customers_df, on='customer_id', how='left')
        
        # Merge with categories dataframe using left join
        merged_df = pd.merge(merged_df, categories_df, on='category_id', how='left')
        
        # Merge with reviews dataframe using left join
        merged_df = pd.merge(merged_df, reviews_df, on=['product_id', 'customer_id'], how='left')
        #Aggregate data
        aggregated_df = merged_df.groupby('customer_id').agg(
                    {'total_amount': ['sum','mean'],  # Calculate total amount and avarage amount for each customer's
                     'order_id': 'nunique',  # Calculate unique  order for each customer's
                     'product_id': 'count',  # Calculate Total products ordered
                     'rating': 'mean'        # Calculate Average rating received
                    }).reset_index()
        aggregated_df.columns = ['customer_id', 'total_amount_spent', 'average_amount_spent', 'total_orders', 'total_products_ordered',         'average_rating']
        
        final_df = aggregated_df.merge(customers_df, on='customer_id',how='inner') 
        # Round numerical columns to 2 decimal places
        final_df['average_rating'] = final_df['average_rating'].fillna(0).astype(int)
        final_df = final_df.round({'total_amount_spent': 2, 'average_amount_spent': 2})
        # Select required columns
        result_df = final_df[['customer_id', 'name', 'email', 'country', 'total_amount_spent', 'total_orders', 'average_amount_spent',         'total_products_ordered', 'average_rating']]
         
        return result_df
        
    except Exception as e:
        print(f"An error occurred: {e}")
        error_message = str(e)
        #Send an email to the development team if the job fails, including the cause of the failure
        sender_email = 'ankitarankhamb98@gmail.com'
        receiver_email = 'ankitarankhamb98@gmail.com'
        subject = 'E-commerce Transformation ETL Script Failure'
        body = f'Dear Team,\n\nThe E-commerce Transformation ETL Script has encountered an error:\n\nError Message: {error_message}\n\nPlease investigate and take necessary actions.\n\nRegards,\nETL Team'
        command = f'echo "{body}" | mail -s "{subject}" {receiver_email}'
        # Execute the command using os.system
        os.system(command)
        print("Email sent successfully!")
        return None

staging_data = load_staging_data(csv_directory)
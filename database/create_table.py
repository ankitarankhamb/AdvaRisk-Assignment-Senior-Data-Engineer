import os
import sys
import time
import psycopg2

# PostgreSQL connection settings
current_path = os.getcwd()
db_conn_directory = os.path.join(current_path, "ETL", "database")
if db_conn_directory not in sys.path:
    sys.path.append(db_conn_directory)

from db_connection import get_rds_source_conn
db_params = get_rds_source_conn()
conn = psycopg2.connect(**db_params)

# Open a cursor to perform database operations
cur = conn.cursor()

#Table: customers
create_customers_table_query = '''
CREATE TABLE IF NOT EXISTS customers (
customer_id INT PRIMARY KEY,
name VARCHAR(100) NOT NULL,
email VARCHAR(100) UNIQUE NOT NULL,
country VARCHAR(50) NOT NULL
);
'''

#Table: orders
create_orders_table_query = '''
CREATE TABLE IF NOT EXISTS orders (
order_id INT PRIMARY KEY,
customer_id INT NOT NULL,
order_date DATE NOT NULL,
total_amount DECIMAL(10, 2) NOT NULL,
status VARCHAR(20) NOT NULL,
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
'''

#Table: categories
create_categories_table_query = '''
CREATE TABLE IF NOT EXISTS categories (
category_id INT PRIMARY KEY,
category_name VARCHAR(100) NOT NULL
);
'''

#Table: products
create_products_table_query = '''
CREATE TABLE IF NOT EXISTS products (
product_id INT PRIMARY KEY,
product_name VARCHAR(100) NOT NULL,
category_id INT NOT NULL,
FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
'''

#Table: order_items
create_order_items_table_query = '''
CREATE TABLE IF NOT EXISTS  order_items (
item_id INT PRIMARY KEY,
order_id INT NOT NULL,
product_id INT NOT NULL,
quantity INT NOT NULL,
price DECIMAL(10, 2) NOT NULL,
FOREIGN KEY (order_id) REFERENCES orders(order_id),
FOREIGN KEY (product_id) REFERENCES products(product_id)
);
'''

#Table: reviews
create_reviews_table_query = '''
CREATE TABLE reviews (
review_id INT PRIMARY KEY,
product_id INT NOT NULL,
customer_id INT NOT NULL,
rating INT CHECK (rating BETWEEN 1 AND 5),
review_date DATE NOT NULL,
FOREIGN KEY (product_id) REFERENCES products(product_id),
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
'''

# Execute the create table queries
cur.execute(create_customers_table_query)
cur.execute(create_orders_table_query)
cur.execute(create_categories_table_query)
cur.execute(create_products_table_query)
cur.execute(create_order_items_table_query)
cur.execute(create_reviews_table_query)

#insert into customers table
insert_customers_query = '''
INSERT INTO customers (customer_id, name, email, country) VALUES
(1, 'Alice Smith', 'alice@example.com', 'USA'),
(2, 'Bob Johnson', 'bob@example.com', 'Canada'),
(3, 'Charlie Brown', 'charlie@example.com', 'UK'),
(4, 'Alice Smith', 'alice.smith@example.com', 'USA'),
(5, 'David Miller', 'david@example.com', 'Australia');
'''
cur.execute(insert_customers_query)


# Insert data into the orders table
insert_orders_query = '''
INSERT INTO orders (order_id, customer_id, order_date, total_amount, status)
VALUES
  (1, 1, '2024-07-15', 150.00, 'Shipped'),
  (2, 2, '2024-07-14', 200.50, 'Processing'),
  (3, 1, '2024-07-13', 75.25, 'Delivered'),
  (4, 3, '2024-07-12', 300.75, 'Shipped'),
  (5, 2, '2024-07-11', 180.00, 'Delivered');
'''
cur.execute(insert_orders_query)

# Insert data into the orders table
insert_categories_query = '''
INSERT INTO categories (category_id, category_name) VALUES
(1, 'Electronics'),
(2, 'Books'),
(3, 'Clothing'),
(4, 'Electronics'),
(5, 'Food');
'''
cur.execute(insert_categories_query)

# Insert data into the products table
insert_products_query = '''
INSERT INTO products (product_id, product_name, category_id) VALUES
(1, 'Smartphone', 1),
(2, 'Laptop', 1),
(3, 'Fiction Book', 2),
(4, 'T-Shirt', 3),
(5, 'Laptop', 1),
(6, 'Headphones', 3),
(7, 'Headphones', 1);
'''
cur.execute(insert_products_query)

# Insert data into the order_items table
insert_order_items_query = '''
INSERT INTO order_items (item_id, order_id, product_id, quantity, price) VALUES
(1, 1, 1, 1, 699.99),
(2, 1, 3, 2, 19.99),
(3, 2, 2, 1, 999.99),
(4, 3, 4, 3, 9.99),
(5, 1, 1, 1, 699.99),
(6, 2, 2, 2, 999.99);
'''
cur.execute(insert_order_items_query)

# Insert data into the reviews table
insert_reviews_query = '''
INSERT INTO reviews (review_id, product_id, customer_id, rating, review_date) VALUES
(1, 1, 1, 5, '2023-07-04 08:00:00'),
(2, 3, 2, 4, '2023-07-05 09:00:00'),
(3, 4, 3, 3, '2023-07-06 10:00:00'),
(4, 1, 1, 5, '2023-07-04 08:00:00'),
(5, 2, 2, 2,  '2023-07-07 11:00:00');
'''

# Commit changes to the database
conn.commit()
time.sleep(3) # Sleep for 3 seconds

# Close cursor and connection
cur.close()
conn.close()

print("Tables created and records inserted successfully!")

Data source table structure

-- Table: customers
CREATE TABLE customers (
customer_id INT PRIMARY KEY,
name VARCHAR(100) NOT NULL,
email VARCHAR(100) UNIQUE NOT NULL,
country VARCHAR(50) NOT NULL
);


-- Insert data into customers
INSERT INTO customers (customer_id, name, email, country) VALUES
(1, 'Alice Smith', 'alice@example.com', 'USA'),
(2, 'Bob Johnson', 'bob@example.com', 'Canada'),
(3, 'Charlie Brown', 'charlie@example.com', 'UK'),
(4, 'Alice Smith', 'alice.smith@example.com', 'USA'), -- Duplicate name
(5, 'David Miller', 'david@example.com', 'Australia');

-- Table: orders
CREATE TABLE orders (
order_id INT PRIMARY KEY,
customer_id INT NOT NULL,
order_date DATE NOT NULL,
total_amount DECIMAL(10, 2) NOT NULL,
status VARCHAR(20) NOT NULL,
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

INSERT INTO orders (order_id, customer_id, order_date, total_amount, status)
VALUES
  (1, 1, '2024-07-15', 150.00, 'Shipped'),
  (2, 2, '2024-07-14', 200.50, 'Processing'),
  (3, 1, '2024-07-13', 75.25, 'Delivered'),
  (4, 3, '2024-07-12', 300.75, 'Shipped'),
  (5, 2, '2024-07-11', 180.00, 'Delivered');


-- Table: categories
CREATE TABLE categories (
category_id INT PRIMARY KEY,
category_name VARCHAR(100) NOT NULL
);

INSERT INTO categories (category_id, category_name) VALUES
(1, 'Electronics'),
(2, 'Books'),
(3, 'Clothing'),
(4, 'Electronics'), -- Duplicate category
(5, 'Food'); -- Null category_id

-- Table: products
CREATE TABLE products (
product_id INT PRIMARY KEY,
product_name VARCHAR(100) NOT NULL,
category_id INT NOT NULL,
FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

INSERT INTO products (product_id, product_name, category_id) VALUES
(1, 'Smartphone', 1),
(2, 'Laptop', 1),
(3, 'Fiction Book', 2),
(4, 'T-Shirt', 3),
(5, 'Laptop', 1), -- Duplicate product
(6, 'Headphones', 3), -- Null product name
(7, 'Headphones', 1); -- Null price

-- Table: order_items
CREATE TABLE order_items (
item_id INT PRIMARY KEY,
order_id INT NOT NULL,
product_id INT NOT NULL,
quantity INT NOT NULL,
price DECIMAL(10, 2) NOT NULL,
FOREIGN KEY (order_id) REFERENCES orders(order_id),
FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO order_items (item_id, order_id, product_id, quantity, price) VALUES
(1, 1, 1, 1, 699.99),
(2, 1, 3, 2, 19.99),
(3, 2, 2, 1, 999.99),
(4, 3, 4, 3, 9.99),
(5, 1, 1, 1, 699.99), -- Duplicate order item
(6, 2, 2, 2, 999.99); -- Null quantity


-- Table: reviews
CREATE TABLE reviews (
review_id INT PRIMARY KEY,
product_id INT NOT NULL,
customer_id INT NOT NULL,
rating INT CHECK (rating BETWEEN 1 AND 5),
review_date DATE NOT NULL,
FOREIGN KEY (product_id) REFERENCES products(product_id),
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

INSERT INTO reviews (review_id, product_id, customer_id, rating, review_date) VALUES
(1, 1, 1, 5, '2023-07-04 08:00:00'),
(2, 3, 2, 4, '2023-07-05 09:00:00'),
(3, 4, 3, 3, '2023-07-06 10:00:00'),
(4, 1, 1, 5, '2023-07-04 08:00:00'), -- Duplicate review
(5, 2, 2, 2,  '2023-07-07 11:00:00'); -- Null customer_id


--------------------------------------------------------insert data----------------------------------------------
-- Insert data into customers
INSERT INTO customers (customer_id, name, email, country) VALUES
(1, 'Alice Smith', 'alice@example.com', 'USA'),
(2, 'Bob Johnson', 'bob@example.com', 'Canada'),
(3, 'Charlie Brown', 'charlie@example.com', 'UK'),
(4, 'Alice Smith', 'alice.smith@example.com', 'USA'), -- Duplicate name
(5, 'David Miller', 'david@example.com', 'Australia'); -- Null email

-- Insert data into orders
-- Inserting sample data into the orders table
INSERT INTO orders (order_id, customer_id, order_date, total_amount, status)
VALUES
  (1, 1, '2024-07-15', 150.00, 'Shipped'),
  (2, 2, '2024-07-14', 200.50, 'Processing'),
  (3, 1, '2024-07-13', 75.25, 'Delivered'),
  (4, 3, '2024-07-12', 300.75, 'Shipped'),
  (5, 2, '2024-07-11', 180.00, 'Delivered');


-- Insert data into categories
INSERT INTO categories (category_id, category_name) VALUES
(1, 'Electronics'),
(2, 'Books'),
(3, 'Clothing'),
(4, 'Electronics'), -- Duplicate category
(5, 'Food'); -- Null category_id

-- Insert data into products
INSERT INTO products (product_id, product_name, category_id) VALUES
(1, 'Smartphone', 1),
(2, 'Laptop', 1),
(3, 'Fiction Book', 2),
(4, 'T-Shirt', 3),
(5, 'Laptop', 1), -- Duplicate product
(6, 'Headphones', 3), -- Null product name
(7, 'Headphones', 1); -- Null price


-- Insert data into order_items
INSERT INTO order_items (order_item_id, order_id, product_id, quantity, price) VALUES
(1, 1, 1, 1, 699.99),
(2, 1, 3, 2, 19.99),
(3, 2, 2, 1, 999.99),
(4, 3, 4, 3, 9.99),
(5, 1, 1, 1, 699.99), -- Duplicate order item
(6, 2, 2, NULL, 999.99); -- Null quantity


-- Insert data into reviews
INSERT INTO reviews (review_id, product_id, customer_id, rating, review_text, review_date) VALUES
(1, 1, 1, 5, 'Great smartphone!', '2023-07-04 08:00:00'),
(2, 3, 2, 4, 'Interesting read.', '2023-07-05 09:00:00'),
(3, 4, 3, 3, 'Average quality.', '2023-07-06 10:00:00'),
(4, 1, 1, 5, 'Great smartphone!', '2023-07-04 08:00:00'), -- Duplicate review
(5, 2, NULL, 2, 'Not worth the price.', '2023-07-07 11:00:00'); -- Null customer_id

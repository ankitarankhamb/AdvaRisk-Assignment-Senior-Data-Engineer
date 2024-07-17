## ETL Pipeline Project README
## Introduction
Welcome to the ETL Pipeline Project README. This document provides an overview of setting up, running, and understanding the ETL pipeline designed for transforming E-commerce data.

## Follow these steps to run the ETL pipeline for the eCommerce project:

ecommerce_etl_pipeline/
├── README.md
├── dags/
│   ├── ecommerce_etl_dag.py
├── extract_data_v1.py
├── load_data_v1.py
└── transform_data_v1.py
├── database/
│   ├── db_connection.py
├── email_notifications/
│   ├── mail.py
├── alternative_scripts/
│   ├── extract_data_v1.py
│   ├── transform_data_v1.py
│   ├── load_data_v1.py
│   └── sample_data/
│       ├── customers.csv
│       ├── orders.csv
│       ├── products.csv
│       ├── categories.csv
│       └── reviews.csv

## Run the Extract Script :  extract_data_v1.py

This script connects to the source database using the db_connection.py file for database details.
It extracts the required data, performs data cleaning operations such as dropping duplicates and filling missing values (fillna).
The cleaned data is then written into the PostgreSQL destination database.

## Note ##
Skipping the Staging Step:
If the data is small and doesn't need to be staged for further requirements, you can skip the staging step entirely. Instead, you can directly extract, transform, and load (ETL) the data into MongoDB. This approach streamlines the process and reduces the time required for data processing.
This alternative solution is particularly useful for quick, ad-hoc analyses or when you need to load data directly into MongoDB for new requirements without the intermediate step of staging in a database or file. By storing data directly in the destination database, you maintain flexibility to accommodate changing requirements without the extra load of managing a staging environment..

## Run the Transformation Script : transform_data_v1.py
This script retrieves the cleaned data from the PostgreSQL database.
It applies necessary transformation logic, including calculating averages, counts, and other metrics.
The script merges data from the five tables into a single transformed table.

## Run the Load Script : load_data_v1.py
This script accesses the transformed data and generates the required insights, such as the top 5 customers by total amount spent, top 5 products by number of orders, average product ratings by category, and the monthly sales trend.
The aggregated data and insights are then stored in MongoDB.
The MongoDB setup includes one client and two collections: one for aggregated data and one for insights.

## Alternative Method (Using CSV Files)
In addition to the primary method, there are alternative scripts provided for cases where data is stored in files such as CSV, JSON, or Parquet on an S3 bucket.

By following these steps, you can ensure that the ETL pipeline runs smoothly, extracting, transforming, and loading data while generating valuable insights from the eCommerce data.

## SQL Database (PostgreSQL)
## Source PostgreSQL Database Connection Details:
Host: localhost
Port: 5432
Username: <your_username>
Password: <your_password>

## SQL Database Tables:
customers: Stores customer information.
orders: Contains order details including customer references.
order_items: Lists items in each order with product references.
products: Describes products available with category references.
categories: Categorizes products.
reviews: Holds product reviews by customers.

## NoSQL Database (MongoDB)
## NoSQL Database Collection:
database connection :  mongodb://localhost:27017
create one client : ecommerce_insights
create two collections :
  1. aggregated_data_collection : Stores aggregated customer.
  2. insights_data_collection : Stores insights.

## Running the Pipeline
## Using Airflow for Orchestration
To run Airflow worker and scheduler on your machine, create a Docker container

## Access Airflow UI:
Open a web browser and go to http://localhost:8080.
Navigate to the 'ecommerce_etl_pipeline' DAG and trigger it to start the pipeline.


## Time Complexities (Big O Notations)
## SQL Operations:
Joins: O(m * n) where m and n are the number of rows in joined tables.
Aggregations: O(n log n) for group by operations.
Retrievals: O(n log n) for fetching top N records.

## NoSQL Operations:
Insertions: O(1) for inserting documents.
Reads: O(1) for retrieving documents by indexed fields.

## Data Reconciliation Scripts:
Automated scripts to reconcile data between SQL and NoSQL databases.
Scheduled 3 hours jobs to ensure regular updates and consistency checks.

## Performance Optimization:
Database indexing for faster query execution.






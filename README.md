## ETL Pipeline Project README
## Introduction
Welcome to the ETL Pipeline Project README. This document provides an overview of setting up, running, and understanding the ETL pipeline designed for transforming E-commerce data.

## SQL Database (PostgreSQL)

## Create Database and User:
Open a terminal and execute the following commands:
CREATE DATABASE ecommerce_source_db;

## Source Database Connection Details:
Host: localhost
Port: 5432
Username: your_username
Password: your_password

## SQL Database Tables:
customers: Stores customer information.
orders: Contains order details including customer references.
order_items: Lists items in each order with product references.
products: Describes products available with category references.
categories: Categorizes products.
reviews: Holds product reviews by customers.

## NoSQL Database (MongoDB)
## NoSQL Database Collection:
aggregated_data_collection : Stores aggregated customer.
insights_data_collection : Stores insights.

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

## NOTE ##
## Skipping the Staging Step
If the data is small and doesn't need to be staged for further requirements, you can skip the staging step entirely. Instead, you can directly extract, transform, and load (ETL) the data into MongoDB. This approach streamlines the process and reduces the time required for data processing.

This alternative solution is particularly useful for quick, ad-hoc analyses or when you need to load data directly into MongoDB for new requirements without the intermediate step of staging in a database or file. By storing data directly in the destination database, you maintain flexibility to accommodate changing requirements without the extra load of managing a staging environment..

# AdvaRisk-Assignment-Senior-Data-Engineer
AdvaRisk-Assignment-Senior-Data-Engineer


### SQL Database Setup

1. Install PostgreSQL (if not already installed).

2. Create a new database and user:
   ```sql
   CREATE DATABASE ecommerce_db;
   CREATE USER ecommerce_user WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;

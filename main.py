import os
import sys
from dotenv import load_dotenv
import mysql.connector

# Load environment variables
load_dotenv();

# Connect to MySQL database to store collected data in
db_connection = mysql.connector.connect(
    host = os.getenv('DB_HOST'),
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    database = os.getenv('DB_DATABASE')
);

#
if db_connection.is_connected():
    print( 'Successfully connected to the database' )
else:
    sys.exit( 'Could not connecto to database, cannot run script.' )

# Used to execute SQL queries on the database
cursor = db_connection.cursor()

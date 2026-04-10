import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv();

db_connection = mysql.connector.connect(
    host = os.getenv('DB_HOST'),
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    database = os.getenv('DB_DATABASE')
);

if db_connection.is_connected():
    print("Successfully connected to the database")

cursor = db_connection.cursor()

cursor.execute('SHOW TABLES;')
for row in cursor.fetchall():
    print(row)

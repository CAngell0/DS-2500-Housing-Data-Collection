import os
from dotenv import load_dotenv
import requests

from database import MySQLConnection
# Load environment variables
load_dotenv();

database = MySQLConnection()

res = database.send('SHOW TABLES;')


# resp = requests.get('https://api.rentcast.io/v1/listings/sale',
#     params = {
#         'city': 'Austin',
#         'state': 'TX',
#         'status': 'Active'
#     },
#     headers = {
#         'Accept': 'application/json'
#     }
# )

# print(resp.json())

# with open('./response.txt', 'w') as file:
#     file.write(str(resp.json()))


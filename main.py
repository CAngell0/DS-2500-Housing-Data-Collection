import os
import time
import requests
from dotenv import load_dotenv

from database import MySQLConnection
from rentcast import RentCastAPI, APISearchRegion
from utils import *

# Load environment variables
load_dotenv();

# Connect to the MySQL database with environment variable settings
# database = MySQLConnection(
#     host = str( os.getenv('DB_HOST') ),
#     user = str( os.getenv('DB_USER') ),
#     password = str( os.getenv('DB_PASSWORD') ),
#     database = str( os.getenv('DB_DATABASE') )
# )


api = RentCastAPI(
    api_key = str( os.getenv('RENTCASE_API_KEY') ),
    request_limit = 10
)

TARGET_REGIONS = [
    APISearchRegion('UT', 40.634901, -111.917321, 15)
]

# TODO - Test the API class
# TODO - Test to make sure data can be added to the database (and make sure everything is good there)


# data = get_listings('TX', 'Austin', 0)

# with open('./response.txt', 'w') as file:
#     file.write(str(data))


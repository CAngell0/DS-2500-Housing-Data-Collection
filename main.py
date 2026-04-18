import os
import json
from dotenv import load_dotenv


from database import MySQLConnection
from rentcast import RentCastAPI, APISearchRegion
from property import Property

# Load environment variables
load_dotenv();

# Connect to the MySQL database with environment variable settings
database = MySQLConnection(
    host = str( os.getenv('DB_HOST') ),
    user = str( os.getenv('DB_USER') ),
    password = str( os.getenv('DB_PASSWORD') ),
    database = str( os.getenv('DB_DATABASE') )
)


api = RentCastAPI(
    api_key = str( os.getenv('RENTCASE_API_KEY') ),
    request_limit = 10
)

TARGET_REGIONS = [
    APISearchRegion('UT', 40.634901, -111.917321, 15)
]


testdata = ""
with open('./testdata.txt', 'r') as file:
    testdata = file.read()
jsondata = json.loads(testdata)


test = Property(**jsondata[0])

# [print(x) for x in database.send("SHOW tables;")]

# TODO - Test the API class
# TODO - Test to make sure data can be added to the database (and make sure everything is good there)


# for region in TARGET_REGIONS:
#     api.offset = 0
#     api.use_region(region)

#     while not api.region_complete:
#         chunk = api.get_listings_chunk()
#         time.sleep(1)
    
#     print(api.offset)

# with open('./response.txt', 'w') as file:
#     file.write(str(data))


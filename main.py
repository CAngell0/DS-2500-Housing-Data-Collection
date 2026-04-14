import os
import requests
from dotenv import load_dotenv

from database import MySQLConnection
from utils import *

# Load environment variables
load_dotenv();

# Connect to the MySQL database with environment variable settings
database = MySQLConnection(
    host = str( os.getenv('DB_HOST') ),
    user = str( os.getenv('DB_USER') ),
    password = str( os.getenv('DB_PASSWORD') ),
    database = str( os.getenv('DB_DATABASE') )
)

# Method used to make an API call to RentCast
def get_listings(state: str, city: str, offset: int):
    """
    Makes an API call to the RentCast API to retrieve current listing data on a specified region.

    :param state: What state to pull listings from. Must be in 2-character state format (e.g. 'TX' or 'UT')
    :param city: What cit inside the state specified to pull listings from. Needs to be the full name and capitalized
    :param offset: Offset index according to the pagination system outlined by the RentCast docs.
    :return: Either a list or dictionary of the JSON data from the request. See requests.get().json().
    """

    # Makes a request to the RentCast API to retrieve sale listings data based on the location specified
    response = requests.get('https://api.rentcast.io/v1/listings/sale',
        headers = {
            'X-Api-Key': os.getenv('RENTCASE_API_KEY'),
            'Accept': 'application/json'
        },
        params = {
            'state': state,
            'city': city,
            'status': 'Active',
            'limit': 500,
            'offset': offset
        }
    )

    # If the API call failed, throw an exception detailing why
    if (response.status_code != 200): raise Exception(f'API request failed, here is the response data: \n{prettify_json(response.json())}');

    # Return the respons data
    return response.json()


page_offset = 0
requests_made = 0




# data = get_listings('TX', 'Austin', 0)

# with open('./response.txt', 'w') as file:
#     file.write(str(data))


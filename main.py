import os
from dotenv import load_dotenv
import requests

from database import MySQLConnection
from utils import *
# Load environment variables
load_dotenv();

database = MySQLConnection()

page_offset = 0


def get_listings(state: str, city: str):
    """
    Makes an API call to the RentCast API to retrieve current listing data on a specified region. Also increments
    the page_offset variable to that it can keep track of what sale listings it has already pulled during the algorithm.

    :param state: What state to pull listings from. Must be in 2-character state format (e.g. 'TX' or 'UT')
    :param city: What cit inside the state specified to pull listings from. Needs to be the full name and capitalized
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
            'offset': page_offset
        }
    )

    # If the API call failed, throw an exception detailing why
    if (response.status_code != 200): raise Exception(f'API request failed, here is the response data: \n{prettify_json(response.json())}');

    # Return the respons data
    return response.json()



data = get_listings('TX', 'Austin')

with open('./response.txt', 'w') as file:
    file.write(str(data))


# Author: Carson Angell
# Date: 4/10/2026

import os
import time
import json

from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from dataclasses import asdict
from pydantic import ValidationError

from model.database import MySQLConnection
from model.rentcast import RentCastAPI, APISearchRegion
from model.property import Property

error_count = 0

# Create the log folder and log file for the script
log_file_name = datetime.now().strftime('%Y-%m-%d') + '.txt'
log_folder = Path('./logs')

log_folder.mkdir(exist_ok = True)
with open(log_folder / log_file_name, 'w') as file: file.write('-- Start of log file for properties data collection script --\n')

# Load environment variables
load_dotenv();

# Connect to the MySQL database with environment variable settings with a wrapper
database = MySQLConnection(
    host = str( os.getenv('DB_HOST') ),
    user = str( os.getenv('DB_USER') ),
    password = str( os.getenv('DB_PASSWORD') ),
    database = str( os.getenv('DB_DATABASE') )
)

# Set up the rent cast API wrapper
api = RentCastAPI(
    api_key = str( os.getenv('RENTCASE_API_KEY') ),
    request_limit = 10
)

# Configured regions for the script to target
TARGET_REGIONS = [
    APISearchRegion('UT', 40.634901, -111.917321, 15)
]




# Logs a message or a list of messages to the designated log file
def log(message):
    formatted_message = '';

    # If its a list, log each list item as its own line
    if isinstance(message, list):
        for line in message:
            formatted_message += f'\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ->  {line}'

    # If its a string, simply format it with a time stamp
    elif isinstance(message, str):
        formatted_message = f'\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ->  {message}'
    
    # Append the log(s) to the file
    with open(log_folder / log_file_name, 'a') as file:
        file.write(formatted_message)




# Takes the full data of an API call, processes it and sends it to the database
def handle_region_chunk(chunk):
    # Templates and scaffolding for the SQL query that imports the data
    sql_query = 'INSERT INTO properties (rentcast_id, address, state, county, city, zip, sqft, bedrooms, bathrooms, lot_size, year_built, listed_date)\nVALUES'
    row_template = '\n\t("{rentcast_id}", "{address}", "{state}", "{county}", "{city}", {zip}, {sqft}, {bedrooms}, {bathrooms}, {lot_size}, {year_built}, "{listed_date}"),'
    log_messages = [] # Keeps track of errors and successful handlings

    # For every property that was retrieved...
    for property in chunk:
        pojo = None

        # Validate that its JSON matches what is expected
        try: pojo = Property(**property)
        except ValidationError: 
            log_messages.append(f'Invalid property data recieved, could not add.\n\n{json.dumps(property, indent=4)}\n')
            continue
        
        # Convert the date value from unix to a more readable format that SQL understands and can parse into a DATE type
        converted_date = datetime.fromisoformat(pojo.listed_date).strftime("%Y-%m-%d")
        pojo.listed_date = converted_date

        # Use the template above and add the data to the query
        sql_query += row_template.format_map(asdict(pojo))

        # Log that this property was retrieved
        log_messages.append(f'Retrieved property data for RentCase ID :  {pojo.rentcast_id}')
    
    # Final touch on the query to make it syntactically valid
    sql_query = sql_query[:-1] + ';'

    # Send the query to the database and log any errors that may have occurred while doing so
    try: database.send(sql_query)
    except Exception as err: log_messages.append(f'Database error occurred when adding listing chunk:\n\t{err}\n')

    log(log_messages)




# Start making API calls and retrieve data from the configured regions. Both of the loops below will break of the API reaches its request limit or repeated errors are thrown (up to 5)
completed_regions = []
for region in TARGET_REGIONS:
    api.use_region(region)

    while not api.region_is_complete and not error_count >= 5:
        chunk = None

        try: chunk = api.get_listings_chunk()
        except Exception as err: 
            log(f'Retrieval error occurred when getting listing data chunk:\n\t{err}\n')
            error_count += 1
            continue
        
        error_count = 0
        handle_region_chunk(chunk)
        time.sleep(1) # The rate limiting for the API is very low, but this is just to be save
    
    if (error_count < 5): completed_regions.append(str(region))


# Log a small yet descriptive summary of the script.
log(
    'Script has finished executing, the following regions were successfully retrieved:' +
        ''.join([f'\n\t{region}' for region in completed_regions]) +
        ''.join(['\n\n-- End of log file --'])
)


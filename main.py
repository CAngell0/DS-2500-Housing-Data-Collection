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

# Connect to the MySQL database with environment variable settings
database = MySQLConnection(
    host = str( os.getenv('DB_HOST') ),
    user = str( os.getenv('DB_USER') ),
    password = str( os.getenv('DB_PASSWORD') ),
    database = str( os.getenv('DB_DATABASE') )
)

# Set up the rent cast API
api = RentCastAPI(
    api_key = str( os.getenv('RENTCASE_API_KEY') ),
    request_limit = 10
)

# Create constants for what regions to target.
TARGET_REGIONS = [
    APISearchRegion('UT', 40.634901, -111.917321, 15)
]


def log(message):
    formatted_message = '';

    if isinstance(message, list):
        for line in message:
            formatted_message += f'\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ->  {line}'

    elif isinstance(message, str):
        formatted_message = f'\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ->  {message}'
    
    with open(log_folder / log_file_name, 'a') as file:
        file.write(formatted_message)



def handle_region_chunk(chunk):
    sql_query = 'INSERT INTO properties (rentcast_id, address, state, county, city, zip, sqft, bedrooms, bathrooms, lot_size, year_built, listed_date)\nVALUES'
    row_template = '\n\t("{rentcast_id}", "{address}", "{state}", "{county}", "{city}", {zip}, {sqft}, {bedrooms}, {bathrooms}, {lot_size}, {year_built}, "{listed_date}"),'
    log_messages = []

    for property in chunk:
        pojo = None

        try: pojo = Property(**property)
        except ValidationError: 
            log_messages.append(f'Invalid property data recieved, could not add.\n\n{json.dumps(property, indent=4)}\n')
            continue
        
        converted_date = datetime.fromisoformat(pojo.listed_date).strftime("%Y-%m-%d")
        pojo.listed_date = converted_date

        sql_query += row_template.format_map(asdict(pojo))
        log_messages.append(f'Retrieved property data for RentCase ID :  {pojo.rentcast_id}')
    
    sql_query = sql_query[:-1] + ';'
    print(sql_query)

    try: database.send(sql_query)
    except Exception as err: log_messages.append(f'Database error occurred when adding listing chunk:\n\t{err}\n')

    log(log_messages)



completed_regions = []
for region in TARGET_REGIONS:
    api.offset = 0
    api.use_region(region)

    while not api.region_complete and not error_count >= 5:
        chunk = None

        try: chunk = api.get_listings_chunk()
        except Exception as err: 
            log(f'Retrieval error occurred when getting listing data chunk:\n\t{err}\n')
            error_count += 1
            continue
        
        error_count = 0
        handle_region_chunk(chunk)
        time.sleep(1)
    
    if (error_count < 5): completed_regions.append(str(region))

log(
    'Script has finished executing, the following regions were successfully retrieved:' +
        ''.join([f'\n\t{region}' for region in completed_regions]) +
        ''.join(['\n\n-- End of log file --'])
)


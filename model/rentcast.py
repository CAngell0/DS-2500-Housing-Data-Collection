# Author: Carson Angell
# Date: 4/14/2026

import requests
import json

# A simple class to wrap a region and its properties so that it can be used by the API wrapper
class APISearchRegion:
    def __init__(self, state: str, lat: float, lon: float, radius: float) -> None:
        self.state = state
        self.lat = lat
        self.lon = lon
        self.radius = radius
        pass
    
    # Make a readable string from the properties of the region
    def __str__(self) -> str:
        return f'Region(state = \'{self.state}\', lat = {self.lat}, lon = {self.lon}, radius = {self.radius})'


# An API wrapper that calls the RentCast endpoints and manages all the API logic (for the most part)
class RentCastAPI:
    def __init__(self, api_key: str, request_limit: int) -> None:
        """
        Initializes the API wrapper. No special API requests or authentication is called here. It simply sets some local member
        variables.

        :param api_key: API Key that will be used during the HTTP requests to the API
        :param request_limit: How many requests the API is allowed to make before it will refuse further calls from the script.
                              This is here because the free trial of RentCasts only allows free API calls up to 50 requests.
                              And if you go over that limit, it will begin charging your account automatically. This is to prevent that.
        :return:
        """

        self.key = api_key
        self.request_limit = request_limit
        self.region_is_complete = False
        self.request_count = 0
        self.offset = 0
        pass
    
    def reset_offset(self):
        """
        Resets the offset member variable to 0. This makes it ready for a new region entirely. Make sure to call this after a region has successfully been
        received.
        """
        self.offset = 0

    def use_region(self, region: APISearchRegion):
        """
        Set the region that the API will pull from when calling get_listings_chunk(). This method also resets the region_is_complete member variables.
        However it does not reset the offset member variable. This is because the caller may want to set a manual offset to start on a certain page in the requests.
        Make sure to call reset_offset() when the region data is done being collected.
        :param region: The region wrapper object to read from and reference internally
        """
        
        self.region = region
        self.region_is_complete = False
    
    def get_listings_chunk(self):
        """
        Make an HTTP GET request to the /listings/sale RentCase endpoint. It will use the region that was configured with the
        use_region() method. If this method is called before a region is set, an exception will be thrown. Furthermore, if the
        request limit has been reached, it will also throw an exception. Exceptions from the requests.get() method are also 
        propagated up.

        :return: A dictionary that holds the JSON listing data the was retrieved from the API call. If the region is flagged as complete
                 according to the pagination offset, and this method is called. It will return an empty list.
        """

        # Check for invalid settings and limits before executing the call
        if (self.request_count >= self.request_limit): raise Exception('Request limit reached, cannot continue with request')
        if (self.region == None): raise Exception('A region has not be specified to use, cannot perform request')
        if (self.region_is_complete): return []
        
        # Make the API request
        response_data = requests.get('https://api.rentcast.io/v1/listings/sale',
            headers = {
                'X-Api-Key': self.key,
                'Accept': 'application/json'
            },
            params = {
                'state': self.region.state,
                'latitude': self.region.lat,
                'longitude': self.region.lon,
                'radius': self.region.radius,
                'limit': 500,
                'offset': self.offset,
                'status': 'Active',
                'propertyType': 'Single Family'
            }
        ).json()

        # Update internal logic before returning the data
        self.request_count += 1
        self.offset += len(response_data)
        if (len(response_data) < 500): self.region_is_complete = True

        return response_data

import requests

class APISearchRegion:
    def __init__(self, state: str, lat: float, lon: float, radius: float) -> None:
        self.state = state
        self.lat = lat
        self.lon = lon
        self.radius = radius
        pass

class RentCastAPI:
    def __init__(self, api_key: str, request_limit: int) -> None:
        self.key = api_key
        self.request_limit = request_limit
        self.region_complete = False
        self.request_count = 0
        self.offset = 0
        pass

    def use_region(self, region: APISearchRegion):
        self.region = region
        self.region_complete = False
    
    def get_listings_chunk(self):
        if (self.request_count >= self.request_limit): raise Exception('Request limit reached, cannot continue with request')
        if (self.region == None): raise Exception('A region has not be specified to use, cannot perform request')
        if (self.region_complete): return []

        if (self.request_count == 5): response_data = [0] * 300
        else: response_data = [0] * 500
        # response_data = [0] * 300
        

        # response_data = requests.get('https://api.rentcast.io/v1/listings/sale',
        #     headers = {
        #         'X-Api-Key': self.key,
        #         'Accept': 'application/json'
        #     },
        #     params = {
        #         'state': self.region.state,
        #         'latitude': self.region.lat,
        #         'longitude': self.region.lon,
        #         'radius': self.region.radius,
        #         'limit': 500,
        #         'offset': self.offset,
        #         'status': 'Active',
        #         'propertyType': 'Single Family'
        #     }
        # ).json()

        self.request_count += 1
        if (len(response_data) < 500): self.region_complete = True
        else: self.offset += 500

        print('Retrieved chunk');
        # return response_data
        return ""

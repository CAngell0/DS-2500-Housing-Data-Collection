import json
from pydantic import Field
from pydantic import TypeAdapter
from pydantic.dataclasses import dataclass

@dataclass
class Property:
    rentcast_id: str = Field(alias = 'id')

    address: str = Field(alias = 'addressLine1')
    state: str = Field(alias = 'state')
    county: str = Field(alias = 'county')
    city: str = Field(alias = 'city')
    zip: int = Field(alias = 'zipCode')

    sqft: int = Field(alias = 'squareFootage')
    bedrooms: int = Field(alias = 'bedrooms')
    bathrooms: float = Field(alias = 'bathrooms')
    lot_size: int = Field(alias = 'lotSize')

    year_built: int = Field(alias = 'yearBuilt')
    listed_date: str = Field(alias = 'listedDate')

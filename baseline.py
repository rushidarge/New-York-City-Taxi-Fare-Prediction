#baseline.py
from pydantic import BaseModel

class DataForm(BaseModel):
    pickup_lon: float 
    pickup_lat: float 
    dropoff_lon: float 
    dropoff_lat: float
    passenger : int
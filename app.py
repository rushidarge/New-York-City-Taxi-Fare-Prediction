from fastapi import FastAPI
from baseline import DataForm
import pickle
from datetime import datetime
import numpy as np

with open('reg.pkl', 'rb') as f:
    model = pickle.load(f)

def min_bin(min):
    if min >= 46: return 3
    elif min >= 31: return 2
    elif min >= 16: return 1
    elif min >= 0: return 0
    
def cal_dist(pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude):
    dlon = np.deg2rad(dropoff_longitude) - np.deg2rad(pickup_longitude)
    dlat = np.deg2rad(dropoff_latitude) - np.deg2rad(pickup_latitude)
    pre_dist = np.sin(dlat / 2)**2 + np.cos(pickup_latitude) * np.cos(dropoff_latitude) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(pre_dist), np.sqrt(1 - pre_dist))
    distance = 6373.0 * c
    return distance

# datetime object containing current date and time
now = datetime.now()
day = now.day
week = now.isocalendar()[1]
dayofweek = now.isoweekday()
hour = now.hour
month = now.month
min = min_bin(now.minute)

app = FastAPI()

@app.get("/")
async def root():
    return {"Welcome this is New York Taxi Fare Prediction API goto==>": "url/docs"}


@app.post('/predict')
def predict_fare(data:DataForm):
    data = data.dict()
    pickup_lon=data['pickup_lon']
    pickup_lat=data['pickup_lat']
    dropoff_lon=data['dropoff_lon']
    dropoff_lat=data['dropoff_lat']
    passenger=data['passenger']
    distance=cal_dist(pickup_lon,pickup_lat,dropoff_lon,dropoff_lat)
    
   # print(classifier.predict([[variance,skewness,curtosis,entropy]]))
    prediction = model.predict([[passenger, distance, day, dayofweek, week, hour,month, min]])
    return {'fare_price':f'{prediction[0]}'}

# uvicorn app:app
import os
import requests
from dotenv import load_dotenv

load_dotenv()

READ_KEY = os,getenv(PURPLEAIR_READ_KEY)

HEADERS = {
    "X-API-Key": API_KEY
}

def fetch_sensors_from_group(fields=None):
    """
    Fetching sensor data from the specific group of sensors we have put up in La Marina del Prat Vermell
    """

    if fields is None:
        fields = "sensor_index,name,latitude,longitude,pm2.5_atm,humidity,temperature,pressure,last_seen"

        url = f"https://api.purpleair.com/v1/sensors/:sensor_index"




    pass



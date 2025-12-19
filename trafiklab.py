import json
import math
import os
from datetime import datetime

from dotenv import load_dotenv
import requests

DEV = False

def get_station_data(station_id = 740000757):
    """ Get info and departures from station """
    load_dotenv()

    if DEV:
        data = get_example_data()
    else:
        data = get_data(station_id = station_id)
        if 'errorCode' in data:
            return False

    station_data = parse_station_data(data)
    return station_data


def get_data(station_id = 740000757):
    """ Load JSON-data from Trafiklab API """
    api_key = os.getenv("API_KEY")
    api_url = f'https://realtime-api.trafiklab.se/v1/departures/{station_id}?key={api_key}'

    response = requests.get(api_url)
    json_data = response.json()
    return json_data


def get_example_data():
    """ Get example data (for development and testing) """
    with open('example_data2.json', encoding='UTF-8') as json_file:
        json_data = json_file.read()
    return json.loads(json_data) 


def parse_datetime(datetime_str):
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")


def parse_station_data(data):
    """ Parse JSON data and return dict of departures """    
    departures = []

    for d in data['departures']:
        delay_str = ""
        if d['delay'] > 60:
            minutes = math.floor(d['delay'] / 60)
            delay_str = str(minutes) + ' min. sen'

        departure = {
            'direction' : d['route']['direction'],
            'scheduled' : datetime.strftime(parse_datetime(d['scheduled']), "%H:%M"),
            'delay' : delay_str,
            'designation' : d['route']['designation'],
            'realtime' : datetime.strftime(parse_datetime(d['realtime']), "%H:%M"),
            'transportation_mode' : d['route']['transport_mode'].lower(),
            'canceled' : d['canceled']
        }
        departures.append(departure)

    station_data = {
        'station_name' : data['stops'][0]['name'],
        'time' : parse_datetime(data['timestamp']),
        'departures' : departures
    }
    return station_data


def main():
    load_dotenv()
    data = get_station_data()
    print(data)

if __name__ == "__main__":
    main()

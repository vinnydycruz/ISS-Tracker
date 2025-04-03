import requests
import pytz
from datetime import datetime
from geopy.geocoders import Nominatim

def get_response():
  url = 'http://api.open-notify.org/iss-now.json'

  return requests.get(url).json()

def parse_response(response):
  return (response['timestamp'], response['iss_position']['longitude'], response['iss_position']['latitude'])


def get_location():
  def get_CT(timestamp):
    return datetime.fromtimestamp(timestamp, pytz.timezone('America/Chicago')).strftime('%I:%M%p CT').lstrip('0')
  
  def get_city_state(latitude, longitude):
    geolocator = Nominatim(user_agent="ISS_assignment")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    address = {}
    if hasattr(location, 'raw'):
      address = location.raw.get('address', {})

    return f"{address.get('city') or address.get('town') or address.get('village') or 'Unknown City'}, {address.get('state', 'Unknown State')}"


  timestamp, longitude, latitude = parse_response(get_response())

  return (get_CT(timestamp), get_city_state(latitude, longitude))

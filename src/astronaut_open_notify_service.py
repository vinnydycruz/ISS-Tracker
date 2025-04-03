import requests

def get_response():
  url = 'http://api.open-notify.org/astros.json' 
    
  return requests.get(url).json()

def parse_response(response):
  CRAFT = 'ISS'

  return [astronaut["name"] for astronaut in response["people"] if astronaut.get("craft") == CRAFT]

def get_astronauts():
  return (parse_response(get_response()))


from src.astronaut_open_notify_service import get_response, parse_response

def get_location(iss_location_service):
  try:
    return iss_location_service()
  except Exception as error:
    return str(error) 

def get_astronauts(astronaut_service):
  def key_for_sort(name):
    first_name, last_name = name.split()
    
    return (last_name, first_name)

  try:
    return sorted(astronaut_service(), key=key_for_sort)
  except Exception as error:
    return str(error)

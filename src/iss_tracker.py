from astronaut_open_notify_service import get_astronauts
from location_open_notify_service import get_location

def main():
  try:
    location_data = get_location()

    if len(location_data) == 3:
      timestamp, longitude, latitude = location_data
      Location = f"{longitude}, {latitude}"
    else:
      timestamp, location = location_data
 
    astronauts = get_astronauts()
    print(f"******************************")
    print(f"ISS location as {timestamp} flying over {location}\n")
    print(f"There are {len(astronauts)} people on ISS at this time:")
    for astronaut in astronauts:
      first_name, last_name = " ".join(astronaut.split()[:-1]), astronaut.split()[-1]
      print(f"{last_name}, {first_name}")
    print(f"******************************")
  except Exception as e:
    print(f"Error retrieving ISS data: {str(e)}")
    print(f"******************************")

if __name__ == "__main__":
  main()

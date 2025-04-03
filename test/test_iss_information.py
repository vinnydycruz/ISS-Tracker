import unittest
from unittest.mock import patch
from src.iss_information import get_location, get_astronauts
 
class ISSInformationTests(unittest.TestCase):
  def test_canary(self):
    self.assertTrue(True)

  def test_get_location_returns_time_and_location_that_the_service_returns(self):
    iss_location_service = lambda: ('05:17AM', 'Houston, TX') 

    self.assertEqual(get_location(iss_location_service), ('05:17AM', 'Houston, TX'))

  def throw(self, message):
    raise Exception(message)

  def test_get_location_returns_network_error_if_the_service_throws_an_exception(self): 
    iss_location_service = lambda: self.throw('network error: service unreachable')
    
    self.assertEqual(get_location(iss_location_service), 'network error: service unreachable')

  def test_get_location_returns_service_failed_to_respond_if_service_throws_an_exception(self):
    iss_location_service = lambda: self.throw('service failed to respond')

    self.assertEqual(get_location(iss_location_service), 'service failed to respond')

  def test_get_astronauts_returns_empty_list_if_service_returns_empty_list(self):
    iss_astronaut_service = lambda: []

    self.assertEqual(get_astronauts(iss_astronaut_service), [])

  def test_get_astronauts_returns_list_with_one_name_if_services_returns_one_name(self):
    iss_astronaut_service = lambda: ['Sam Khudairi']

    self.assertEqual(get_astronauts(iss_astronaut_service), ['Sam Khudairi'])

  def test_get_astronauts_returns_list_with_two_names_if_services_returns_two_sorted_names(self): 
    iss_astronaut_service = lambda: ['Jade Bui', 'Sam Khudairi']

    self.assertEqual(get_astronauts(iss_astronaut_service), ['Jade Bui', 'Sam Khudairi'])

  def test_get_astronauts_returns_two_sorted_names_if_service_returns_two_unsorted_names(self):
    iss_astronaut_service = lambda: ['Jade Khudairi', 'Sam Bui'] 

    self.assertEqual(get_astronauts(iss_astronaut_service), ['Sam Bui', 'Jade Khudairi']) 

  def test_get_astronauts_return_two_sorted_names_if_service_returns_two_same_last_names_in_unsorted_order(self):
    iss_astronaut_service = lambda: ['Sam Bui', 'Jade Bui']

    self.assertEqual(get_astronauts(iss_astronaut_service), ['Jade Bui', 'Sam Bui'])
  
  def test_get_astronauts_returns_network_error_if_the_service_throws_an_exception(self):
    iss_astronaut_service = lambda: self.throw('network error: service unreachable')

    self.assertEqual(get_astronauts(iss_astronaut_service), 'network error: service unreachable')

if __name__ == '__main__': 
    unittest.main()

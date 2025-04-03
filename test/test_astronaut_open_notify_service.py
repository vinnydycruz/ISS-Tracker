import unittest
from unittest.mock import patch
from src.astronaut_open_notify_service import get_response, parse_response, get_astronauts

class AstronautOpenNotiftyServiceTests(unittest.TestCase):  
  def test_get_response_returns_response_from_webservices_for_astronaut_names(self):
    self.assertEqual(get_response().keys(), {"people", "number", "message"}) 

  def test_parse_response_returns_astronaut_names_from_given_iss_sample_data(self):
    sample_data = {
      "message":"success",
      "number": 5,
      "people": [
        {"name": "Bob Smith", "craft":"ISS"},
        {"name": "Stuart Kennedy", "craft":"Tiangong"},
        {"name": "Kevin Smith", "craft":"Tiangong"},
        {"name": "Shayla Brown", "craft":"ISS"},
        {"name": "Thomas Davis", "craft":"Tiangong"}
      ]
    }

    self.assertEqual(parse_response(sample_data), ["Bob Smith", "Shayla Brown"])

  def test_parse_response_returns_astronaut_names_from_another_iss_sample_data(self):
    sample_data = {
      "message":"success",
      "number": 3,
      "people": [
        {"name": "Jade Bui", "craft":"ISS"},
        {"name": "Tony Stark", "craft":"Tiangong"},
        {"name": "Sam Khudairi", "craft":"ISS"}
      ]
    }

    expected_names = ["Jade Bui", "Sam Khudairi"] 

    self.assertEqual(parse_response(sample_data), expected_names)

  def test_get_astronauts_calls_get_response_and_parse_response(self):
    with patch('src.astronaut_open_notify_service.get_response') as mock_get_response, \
         patch('src.astronaut_open_notify_service.parse_response') as mock_parse_response: 

      mock_get_response.return_value = {
        "message":"success",
        "number": 3,
        "people": [
          {"name": "Jade Bui", "craft":"ISS"},
          {"name": "Tony Stark", "craft":"Tiangong"},
          {"name": "Sam Khudairi", "craft":"ISS"}
        ]
      }
      mock_parse_response.return_value = ['Jade Bui', 'Sam Khudairi']

      self.assertEqual(get_astronauts(), ['Jade Bui','Sam Khudairi'])

      mock_get_response.assert_called_once()
      mock_parse_response.assert_called_once_with(mock_get_response.return_value)

  def test_get_astronauts_throws_exception_if_get_response_fails(self):
    with patch('src.astronaut_open_notify_service.get_response') as mock_get_response:
      mock_get_response.side_effect = Exception("Network error")

      self.assertRaisesRegex(Exception, "Network error", get_astronauts)

  def test_get_astronauts_throws_exception_if_parse_response_fails(self):
    with patch('src.astronaut_open_notify_service.get_response') as mock_get_response, \
         patch('src.astronaut_open_notify_service.parse_response') as mock_parse_response: 

      mock_get_response.return_value = {
        "message":"success",
        "number": 3,
        "people": [
          {"name": "Jade Bui", "craft":"ISS"},
          {"name": "Tony Stark", "craft":"Tiangong"},
          {"name": "Sam Khudairi", "craft":"ISS"}
        ]
      }

      mock_parse_response.side_effect = Exception("Parsing error")

      self.assertRaisesRegex(Exception, "Parsing error", get_astronauts)

      mock_get_response.assert_called_once()
    
if __name__ == '__main__': 
    unittest.main()

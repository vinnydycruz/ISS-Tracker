import unittest
from unittest.mock import patch, MagicMock
from src.location_open_notify_service import get_response, parse_response, get_location
from datetime import datetime
from geopy.geocoders import Nominatim
import pytz

class LocationOpenNotifyServiceTtests(unittest.TestCase):
  def test_get_response_returns_response_from_webservices_for_iss_location_and_time(self):
    self.assertEqual(get_response().keys(), {"iss_position", "timestamp", "message"})

  def test_parse_response_returns_timestamp_and_location_from_the_given_sample_data(self):
    sample_data = {
      "message": "success",
      "timestamp": 1364795862,
      "iss_position": {
        "latitude": -47.36999493,
        "longitude": 151.738540034
      }
    }

    self.assertEqual(parse_response(sample_data), (1364795862, 151.738540034, -47.36999493))

  def test_parse_response_returns_timestamp_and_location_from_another_sample_data(self):
      sample_data = {
        "message": "success",
        "timestamp": 1526893429,
        "iss_position": {
          "latitude": 33.428677212,
          "longitude": -120.12253718
        }
      }

      self.assertEqual(parse_response(sample_data), (1526893429, -120.12253718, 33.428677212))

  def test_get_location_calls_get_response_and_parse_response(self):
    with patch('src.location_open_notify_service.get_response') as mock_get_response, \
         patch('src.location_open_notify_service.parse_response') as mock_parse_response, \
         patch('src.location_open_notify_service.datetime') as mock_datetime, \
         patch('src.location_open_notify_service.Nominatim') as mock_nominatim:

      mock_nominatim.return_value.reverse.return_value = MagicMock(
        latitude='12.345678901',
        longitude='140.22233344',
        raw={'address': {'city': '12.345678901', 'state': '140.22233344'}}
      )

      mock_datetime.fromtimestamp.return_value = MagicMock(strftime=MagicMock(return_value='1234567890'))


      mock_get_response.return_value = {
        "message": "success",
        "timestamp": 1234567890,
        "iss_position": {
          "latitude": 12.345678901,
          "longitude": 140.22233344
        }
      }
      mock_parse_response.return_value = [1234567890, '12.345678901', '140.22233344']

      self.assertEqual(get_location(),('1234567890', '12.345678901, 140.22233344'))

      mock_get_response.assert_called_once()
      mock_parse_response.assert_called_once_with(mock_get_response.return_value)

  def test_get_location_returns_time_in_CT(self):
     with patch('src.location_open_notify_service.get_response') as mock_get_response, \
          patch('src.location_open_notify_service.parse_response') as mock_parse_response, \
          patch('src.location_open_notify_service.datetime') as mock_datetime, \
          patch('src.location_open_notify_service.Nominatim') as mock_nominatim:

       mock_nominatim.return_value.reverse.return_value = MagicMock(
        latitude='30.2672',
        longitude='97.7431',
        raw={'address': {'city': '30.2672', 'state': '97.7431'}}
      )
          
       mock_datetime.fromtimestamp.return_value = datetime(2025, 3, 4, 21, 55, tzinfo=pytz.timezone('America/Chicago'))
 
       mock_get_response.return_value = {
         "message": "success",
         "iss_position": {
           "latitude": "30.2672",
           "longitude": "97.7431"
          },
         "timestamp": 1741146950
       }

       mock_parse_response.return_value = (1741146950, '30.2672', '97.7431')

       self.assertEqual(get_location(), ('9:55PM CT', '30.2672, 97.7431'))

  def test_get_location_returns_city_and_state(self):
     with patch('src.location_open_notify_service.get_response') as mock_get_response, \
          patch('src.location_open_notify_service.parse_response') as mock_parse_response, \
          patch('src.location_open_notify_service.datetime') as mock_datetime, \
          patch('src.location_open_notify_service.Nominatim') as mock_nominatim:
          
       mock_nominatim.return_value.reverse.return_value = MagicMock(raw={'address': {'city': 'Austin', 'state': 'Texas'}})

       mock_datetime.fromtimestamp.return_value = datetime(2025, 3, 4, 21, 55, tzinfo=pytz.timezone('America/Chicago'))
 
       mock_get_response.return_value = {
         "message": "success",
         "iss_position": {
           "latitude": "30.2672",
           "longitude": "97.7431"
          },
         "timestamp": 1741146950
       }

       mock_parse_response.return_value = (1741146950, '97.7431', '30.2672')

       self.assertEqual(get_location(), ('9:55PM CT', 'Austin, Texas'))

  def test_get_location_throws_exception_if_get_response_fails(self):
    with patch('src.location_open_notify_service.get_response') as mock_get_response:
      mock_get_response.side_effect = Exception("Network error")

      self.assertRaisesRegex(Exception, "Network error", get_location)

  def test_get_location_throws_exception_if_parse_response_fails(self):
    with patch('src.location_open_notify_service.get_response') as mock_get_response, \
         patch('src.location_open_notify_service.get_response') as mock_parse_response: 

      mock_get_response.return_value = {
        "message": "success",
        "iss_position": {
           "latitude": "30.2672",
           "longitude": "97.7431"
         },
         "timestamp": 1741146950
       }

      mock_parse_response.side_effect = Exception("Parsing error")

      self.assertRaisesRegex(Exception, "Parsing error", get_location)

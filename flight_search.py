import requests
import os

class FlightSearch:
    def __init__(self):
        self.flight_search_endpoint = "https://api.tequila.kiwi.com/locations/query?"
        self.api_key = os.environ.get("FLIGHT_SEARCH-API")

    def get_destination_code(self, city):
        header = {
            "apikey": self.api_key,
        }
        parameter = {
            "term": city
        }

        response = requests.get(url=self.flight_search_endpoint, params=parameter, headers=header)
        response.raise_for_status()
        return response.json()['locations'][0]["code"]

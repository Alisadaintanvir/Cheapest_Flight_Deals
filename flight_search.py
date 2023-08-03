import requests
import os
from flight_data import FlightData


class FlightSearch:
    def __init__(self):
        self.flight_search_endpoint = "https://api.tequila.kiwi.com"
        self.api_key = os.environ.get("FLIGHT_SEARCH-API")

    def get_destination_code(self, city):
        header = {
            "apikey": self.api_key,
        }
        parameter = {
            "term": city
        }

        response = requests.get(url=f"{self.flight_search_endpoint}/locations/query?", params=parameter, headers=header)
        response.raise_for_status()
        return response.json()['locations'][0]["code"]

    def check_flight(self, origin_city_code, destination_city_code, date_from, date_to):
        header = {
            "apikey": self.api_key,
        }

        parameter = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": date_from.strftime("%d/%m/%Y"),
            "date_to": date_to.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "curr": "GBP",
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
        }

        response = requests.get(url=f"{self.flight_search_endpoint}/v2/search?", params=parameter, headers=header)
        response.raise_for_status()

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        return flight_data

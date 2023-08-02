import requests
import os


class DataManager:
    def __init__(self):
        self.SHEET_ENDPOINT = os.environ.get("SHEET_ENDPOINT")
        self.SHEET_AUTHORIZATION = os.environ.get("SHEET_AUTHORIZATION")
        self.header = {
            "Authorization": self.SHEET_AUTHORIZATION
        }
        self.destination_data = {}

    def get_data(self):
        """Return all data from the spreadsheet in a json format"""
        response = requests.get(url=self.SHEET_ENDPOINT, headers=self.header)
        response.raise_for_status()
        self.destination_data = response.json()["prices"]
        return self.destination_data

    def update_data(self):
        """Update the sheet data"""
        for data in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": data['iataCode']
                }
            }
            response = requests.put(url=f"{self.SHEET_ENDPOINT}/{data['id']}", json=new_data, headers=self.header)
            response.raise_for_status()
            print(response.text)

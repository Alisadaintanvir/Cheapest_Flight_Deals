from dotenv import load_dotenv
from data_manager import DataManager

from pprint import pprint

load_dotenv()
data_manager = DataManager()
sheet_data = data_manager.get_data()
# pprint(sheet_data)

if sheet_data[0]["iataCode"] == "":
    from flight_search import FlightSearch
    flight_search = FlightSearch()

    for data in sheet_data:
        data["iataCode"] = flight_search.get_destination_code(data['city'])
    data_manager.destination_data = sheet_data
    data_manager.update_data()


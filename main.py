from dotenv import load_dotenv
from data_manager import DataManager
from datetime import datetime, timedelta
from flight_search import FlightSearch
from notification_manager import NotificationManager
load_dotenv()
data_manager = DataManager()
sheet_data = data_manager.get_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

if sheet_data[0]["iataCode"] == "":
    for data in sheet_data:
        data["iataCode"] = flight_search.get_destination_code(data['city'])
    data_manager.destination_data = sheet_data
    data_manager.update_data()


current_date = datetime.now() + timedelta(days=1)
six_months_from_now = current_date + timedelta(days=6 * 30)

ORIGIN_CITY_IATA = "LON"

for destination in sheet_data:
    flight = flight_search.check_flight(
        ORIGIN_CITY_IATA,
        destination['iataCode'],
        current_date,
        six_months_from_now
    )
    if flight.price < destination["lowestPrice"]:
        notification_manager.send_sms(
            message=f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} "
                    f"to {flight.destination_city}-{flight.destination_airport}, "
                    f"from {flight.out_date} to {flight.return_date}."
        )

import os
import requests
from twilio.rest import Client

# Twilio
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

# OpenWeather
api_key = os.environ.get("OWN_API_KEY")
API_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"

api_parameters = {
    "lat": 51.519272,
    "lon": 14.007640,
    "exclude": "current,minutely,daily",
    "appid": api_key,
}

response = requests.get(url=API_ENDPOINT, params=api_parameters)
response.raise_for_status()
weather_data = response.json()
hour_slice = weather_data["hourly"]

will_rain = False

for hour_data in hour_slice:
    condition_code = int(hour_data["weather"][0]["id"])
    if condition_code < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☔️!",
        from_=os.environ.get("FROM_NUM"),
        to=os.environ.get("MY_NUM")
    )
    print(message.status)

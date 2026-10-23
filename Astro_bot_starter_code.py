# Commands: /weather <city>, /iss, /help, /quit
# Code uses webex, openweather, openweather geocoding and ISS API

import requests # HTTP request to API
import json # Converts message into JSON
import time # Wating between a check
from datetime import datetime # Converts epoch to human format

# =========================
# CONFIGURATION FUNCTIONS
# =========================

def get_webex_token(): # Function asks for token per runtime
    choice = input("Use hard-coded Webex token? (y/n): ").lower()
    if choice == "n":
        token = input("Enter your Webex Access Token: ")
        return f"Bearer {token}"
    else:
        return "Bearer YOUR_WEBEX_TOKEN"

def get_api_key(prompt, hardcoded_key): # Function asks for API key per runtime
    choice = input(f"use hard coded {prompt}? (y/n): ").lower()
    if choice == "n":
        return input(f"enter your {prompt}: ")
    return hardcoded_key

# ================
# WEBEX FUNCTIONS
# ================

def get_rooms(token): # Function gets the Webex space the account is in
    url = "https://webexapis.com/v1/rooms"
    headers = {"Authorization": token} # The token authorises the use of the API
    response = requests.get(url, headers = headers)

    if response.status_code != 200: # Code 200 = OK. If status code is different, there is error
        print("Error fetching rooms:", response.status_code)
        return []

    return response.json().get("items", [])


def print_rooms(rooms): 
    for room in rooms:
        print(f"Room: {room["title"]}, ID: {room["id"]}")


def select_room(rooms): # Asks the user until room name is given
    while True:
        name = input("Enter name of room to monitor: ")
        for room in rooms:
            if name.lower() in room["title"].lower():
                print(f"Selected room: {room["title"]}")
                return room["id"]
        print("Room not found, try again")


def get_latest_message(token, room_id): # Function gets newest message from Webex room
    url = "https://webexapis.com/v1/messages"
    params = {"roomId": room_id, "max": 1}
    headers = {"Authorization": token}

    response = requests.get(url, headers = headers, params = params)

    if response.status_code != 200:
        return None, None

    data = response.json().get("items", [])

    if not data:
        return None, None

    latest = data[0]
    return latest.get("id"), latest.get("text", "")


def send_message(token, room_id, message): # Function sends output to Webex room
    url = "https://webexapis.com/v1/messages"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {
        "roomId": room_id,
        "text": message
    }
    requests.post(url, headers = headers, data = json.dumps(data)) # json.dumps -> turns data into JSON

# ==================
# WEATHER FUNCTIONS
# ==================
    
def get_city_coordinates(city, api_key): # Function is for geocoding API, which gives lat and long of city
    url = "https://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city, "limit": 1, "appid": api_key}
    response = requests.get(url, params = params)

    if response.status_code != 200:
        return None

    data = response.json()
    return data[0] if data else None # 


def get_weather(city, api_key): # Find the lat, long anc weather for given city
    location = get_city_coordinates(city, api_key)

    if not location:
        return "Could not find " + city

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": location["lat"],
        "lon": location["lon"],
        "units": "metric",
        "appid": api_key
    }

    response = requests.get(url, params = params)

    if response.status_code != 200:
        return "Weather data unobtainable right now"

    weather = response.json()

    return (
        f"Weather for {location["name"]}, {location["country"]}\n"
        f"Conditions: {weather["weather"][0]["description"]}\n"
        f"Temperature: {weather["main"]["temp"]} degrees celsius\n"
        f"Humidity: {weather["main"]["humidity"]} percent\n"
        f"Wind Speed: {weather["wind"]["speed"]} m/s"
    )

# ==============
# ISS FUNCTIONS
# ==============

def reverse_geocode(lat, lon, api_key): # Function for reverse geocode API, which find city with lat and long
    url = "https://api.openweathermap.org/geo/1.0/reverse"
    params = {"lat": lat, "lon": lon, "limit": 1, "appid": api_key}

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    data = response.json()
    return data[0] if data else None


def get_iss_location(api_key): # Function for ISS API, which gets ISS position and area it is above
    url = "http://api.open-notify.org/iss-now.json"

    response = requests.get(url)

    if response.status_code != 200:
        return "ISS location unobtainable right now"

    data = response.json()

    lat = data["iss_position"]["latitude"]
    lon = data["iss_position"]["longitude"]

    location = reverse_geocode(lat, lon, api_key)

    time_text = datetime.fromtimestamp(data["timestamp"]).strftime("%d %b %Y %H:%M:%S") # datetime allows conversion of epoch given by ISS API to readable format

    place = "Over Ocean / No Nearby City"

    if location:
        place = f"{location["Name"]}, {location.get("Country", "Unknown")}"

    return (
        f"ISS current location\n"
        f"Latitude {lat}\n"
        f"Longitude: {lon}\n"
        f"Over: {place}\n"
        f"Position time: {time_text}\n"
    )

# ===============
# MAIN BOT LOGIC
# ===============

def main():

    token = get_webex_token()

    weather_key = get_api_key(
        "Weather API key",
        "YOUR_OPENWEATHER_API_KEY"
    )

    rooms = get_rooms(token)

    if not rooms:
        print("No rooms found. Please check your Webex token?")
        return

    print_rooms(rooms)
    room_id = select_room(rooms)

    last_message_id, _ = get_latest_message(token, room_id) # Latest message used to ignore messages before it

    while True: # Checks for messages during runtime

        message_id, message_text = get_latest_message(token, room_id)

        if message_id and message_id != last_message_id: # Stops multiple responses to old message

            last_message_id = message_id

            print(f"Message: {message_text}")

            if not message_text.startswith("/"): # Ensures bot only responds to commands
                continue

            if message_text.lower() == "/help":
                send_message(
                    token,
                    room_id,
                    "AstroBot commands:\n/weather <city>\n/iss\n/help\n/quit"
                )

            elif message_text.lower().startswith("/weather"):

                parts = message_text.split(maxsplit=1)

                if len(parts) < 2:
                    send_message(token, room_id, "Usage: /weather <city>")
                else:
                    city = parts[1]
                    send_message(token, room_id, get_weather(city, weather_key))

            elif message_text.lower() == "/iss":
                send_message(token, room_id, get_iss_location(weather_key))

            elif message_text.lower() == "/quit":
                send_message(token, room_id, "AstroBot shutting down.")
                break

            else:
                send_message(token, room_id, "Unknown command. Use /help")

        time.sleep(5) # Waits for 5 second which helps with the rate limits


if __name__ == '__main__':
    main()

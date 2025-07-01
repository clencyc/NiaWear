import requests
from typing import Dict

def get_weather(city: str, api_key: str) -> Dict:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Weather API error: {response.json().get('message', 'Unknown error')}")
    data = response.json()
    return {
        "temperature": data["main"]["temp"],
        "condition": data["weather"][0]["main"],
    }
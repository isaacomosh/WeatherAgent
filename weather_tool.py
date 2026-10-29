import os
import requests


from dotenv import load_dotenv

API_KEY=os.getenv("OPENWEATHER_API_KEY")


def get_weather(city: str)->dict:
    """
    Get current weather information for a city

    """

    if not API_KEY:
        return {"error":"OpenWeatherMap API key is missing"}

    url="https://api.openweathermap.org/data/2.5/weather"

    params={
        "q": city,"appid":API_KEY,"units":"metrics"
    }

    try:
        response=requests.get(url,params=params,timeout=10)

        if response.status_code==404:
            return {"error": f"City '{city}' was not found."}

        response.raise_for_status()

        data=response.json()

        return{
              "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }
    except requests.RequestException as error:
        return {"error": f"Could not retrieve weather: {error}"}
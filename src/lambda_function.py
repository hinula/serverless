# src/lambda_function.py
import json
import os
import urllib.parse
import urllib.request

OPENWEATHER_KEY = os.environ.get("fa91e1aef39025a54d3c1e9590846fe3")

def lambda_handler(event, context):
    # HTTP API v2 (API Gateway HTTP) formatına uyumlu
    # event["rawQueryString"] veya event["queryStringParameters"] olabilir.
    qs = event.get("queryStringParameters") or {}
    path = event.get("rawPath", "") or event.get("requestContext", {}).get("http", {}).get("path", "")

    # normalize
    path = path.lower()

    if path.endswith("/hello") or path.endswith("/hello/"):
        name = qs.get("name", "Dünya")
        body = {"message": f"Merhaba {name}, bu fonksiyon bulutta çalışıyor!"}
        return respond(200, body)

    if path.endswith("/weather") or path.endswith("/weather/"):
        city = qs.get("city")
        if not city:
            return respond(400, {"error": "Lütfen ?city=CityName parametresini gönderin."})
        if not OPENWEATHER_KEY:
            return respond(500, {"error": "OpenWeather API anahtarı bulunamadı (env var OPENWEATHER_API_KEY)."})
        try:
            weather = get_weather(city)
            return respond(200, {"city": city, "weather": weather})
        except Exception as e:
            return respond(502, {"error": "OpenWeather çağrısı başarısız", "detail": str(e)})

    return respond(404, {"error": "Endpoint bulunamadı. /hello veya /weather kullanın."})


def respond(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, ensure_ascii=False)
    }

def get_weather(city):
    # OpenWeather current weather API (metric)
    base = "https://api.openweathermap.org/data/2.5/weather"
    params = urllib.parse.urlencode({"q": city, "appid": OPENWEATHER_KEY, "units": "metric", "lang": "tr"})
    url = f"{base}?{params}"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    # basit döküm:
    result = {
        "description": data["weather"][0]["description"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data.get("wind", {}).get("speed")
    }
    return result

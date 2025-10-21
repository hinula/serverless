import json
import os
import requests

def lambda_handler(event, context):
    # API Gateway path
    path = event.get("resource", "/")
    params = event.get("queryStringParameters") or {}
    name = params.get("name", "Dünya")
    
    # Endpoint kontrolü
    if path not in ["/hello", "/weather"]:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Endpoint bulunamadı. /hello veya /weather kullanın."}),
            "headers": {"Content-Type": "application/json"}
        }
    
    # OpenWeather API
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    weather_data = {}
    if api_key:
        url = f"http://api.openweathermap.org/data/2.5/weather?q=Istanbul&appid={api_key}&units=metric"
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            weather_data = {
                "city": "Istanbul",
                "temperature": data.get("main", {}).get("temp")
            }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Merhaba {name}, bu fonksiyon bulutta çalışıyor!",
            "weather": weather_data
        }),
        "headers": {"Content-Type": "application/json"}
    }

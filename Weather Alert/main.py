import requests  # type: ignore

api_key = "0223f28d3bf84a9a769ec72ceab038a3"
url = "https://api.openweathermap.org/data/2.5/forecast"
params = {
    "lat" : 46.829853,
    "lon" : -71.254028,
    "appid" : api_key,
    "cnt" : 4
}

response = requests.get(url, params=params)
response.raise_for_status()
response = response.json()

def get_weather_data(response: dict):
    data = []
    for item in response["list"]:
        date = item["dt_txt"]
        temp = item["main"]["temp"]
        description = item["weather"][0]["description"]
        id = item["weather"][0]["id"]
        data.append((date, temp, description, id))
    return data

data = get_weather_data(response)
for date, temp, description, id in data:
    print(f"{date} - Temp: {temp}K - Description: {description} - ID: {id}")

    if id < 600:
        print("------>Bring an umbrella!")
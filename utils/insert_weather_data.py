import requests
import json


headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Token d8bab2bcb9e990e26f2f545c428a7e321f42f88f'
}
with open('weather_data.json', 'r') as f:
    data = json.loads(f.read())
    count = 0
    print(f'The number of weather stations is {len(data)}')
    for station in data:
        count += len(station['data'])
        r = requests.post('http://localhost:8000/api/weatherstations/', json=station, headers=headers)
    print(f'The total number of observations is: {count}')

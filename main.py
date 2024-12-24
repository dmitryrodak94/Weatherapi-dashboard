import requests

API_KEY = '1ce371f748224092807201919242312'
endpoint = 'current'
query = 'London'
BASE_URL = f'http://api.weatherapi.com/v1/{endpoint}.json?key={API_KEY}&q={query}'

def check_url_status():

    responce = requests.get(BASE_URL)

    if responce.status_code == 200:
        return responce.json()
    

print(check_url_status())
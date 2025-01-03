import requests
from credentials import API_KEY


endpoint = 'current'
query = 'London'
BASE_URL = f'http://api.weatherapi.com/v1/{endpoint}.json?key={API_KEY}&q={query}'

def check_url_status():

    responce = requests.get(BASE_URL)

    if responce.status_code == 200:
        return responce.json()
    



print(check_url_status())

#######

# from airflow import DAG
# from datetime import time
# from airflow.operators.python import PythonOperator
# from airflow.providers.http.sensors.http import HttpSensor
# from airflow.hooks.base import BaseHook
import psycopg2
# from credentials import API_KEY
import requests

API_KEY = '1ce371f748224092807201919242312'
CITIES = ['London', 'Kiev']



default_args = {
    'owner': 'dmytro',
    'email': 'dmitryrodak94@gmail.com',
    'email_on_retry': False,
    'email_on_failure': False,
    'retries': 2,
    'retry_delay': 60,
    'depends_on_past': False,
    # 'start_date': datetime(2021, 01, 1),
	# 'end_date': datetime(2022, 12, 5)
}




class DataInsert:
    def __init__(self, CITIES):
        self.CITIES = CITIES

    def check_url_status(self, endpoint, cities):

        for city in cities:
            BASE_URL = f'http://api.weatherapi.com/v1/{endpoint}.json?key={API_KEY}&q={city}'
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                yield response.json()
    



    def postgres_conn(self):
        try:
            conn = psycopg2.connect(
                host='host.docker.internal',
                dbname='today_day_weather',
                user='root',
                password='root')    
            
            cur = conn.cursor()
            return conn

            
        except Exception as e:
            print(e) 
            return None   


    def insertdata(self, conn):
        for city in self.check_url_status('current', CITIES):
            d = []
            d.append(city)
            return d         

    def main(self):
        conn = self.postgres_conn()
        if conn:
            self.insertdata()
        else:
            print('Error')


ii = DataInsert(CITIES)
print(ii.main())
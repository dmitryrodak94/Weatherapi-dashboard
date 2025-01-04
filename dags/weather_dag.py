#######

# from airflow import DAG
# from datetime import time
# from airflow.operators.python import PythonOperator
# from airflow.providers.http.sensors.http import HttpSensor
# from airflow.hooks.base import BaseHook
import psycopg2
# from credentials import API_KEY
import requests
import json as json
import logging
import inspect

API_KEY = '1ce371f748224092807201919242312'
CITIES = ['London', 'Paris', 'Berlin', 'Moscow', 'Kiev', 'Madrid']
APPROACH = 'current'



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
                dbname='postgres',
                user='root',
                password='root',
                port=54320)    
            
            cur = conn.cursor()
            return cur

            
        except Exception as e:
            print(e) 
            return None   


    def getdata(self, approach):
        d = []
        try:
            for city in self.check_url_status(approach, CITIES):
                d.append(city)
            return d
        except Exception as e:
            print(f'Error: {e}')         

    def main(self):
        conn = self.postgres_conn()
        if conn:
            self.getdata(conn)
        else:
            print('Error')
        

api_connect = DataInsert(CITIES)
data = api_connect.getdata(APPROACH)
postgres_conn = api_connect.postgres_conn()
# cities = api_connect.getdata('current')
# print(cities)

def insert_data_location_weather(data, postgres_conn):
    try:
        for d in data:
            name_region = d['location']['region']
            city = d['location']['name']
            country= d['location']['country']
            
            check_exists_data = """
                SELECT COUNT(*)
                FROM location_weather
                WHERE city = %s 

            """
            postgres_conn.execute(check_exists_data, (city, ))
            result = postgres_conn.fetchone()

            if result[0] == 0:
                insert_location_data = """
                    INSERT INTO location_weather (name_region, city, country)
                    VALUES(%s, %s, %s)
                """
                postgres_conn.execute(insert_location_data, (name_region, city, country))
            else:
                logging.info(f'Location {city} {name_region} is already exist')
        # postgres_conn.connection.commit()

    except Exception as e:
        logging.error(f"Error inserting location weather: {e}")

def insert_data_date_weather(data, postgres_conn):
    try:
        for d in data:
            localtime = d['location']['localtime']
            year, month, day = map(int, localtime.split()[0].split('-'))


            check_exists_data = """
                SELECT date_id
                FROM date_weather
                WHERE day = %s and month = %s and year = %s
            """
            postgres_conn.execute(check_exists_data, (int(day), int(month), int(year)))
            result = postgres_conn.fetchone()

            if result == None:
                insert_date_weather_data = """
                        INSERT INTO date_weather (day, month, year)
                        VALUES(%s, %s, %s)
                    """
                postgres_conn.execute(insert_date_weather_data, (day, month, year))
            else:
                logging.info(f"Date {localtime} already exists in the database.")

        # postgres_conn.connection.commit()
    except Exception as e:
        logging.error(f"Error inserting date weather: {e} in {inspect.currentframe().f_code.co_name}")




def insert_data_today_day_weather(data, postgres_conn):


    try: 
        for d in data:
            get_location_id = """
                SELECT location_id
                FROM location_weather
                WHERE city = %s
            """
            try:
                postgres_conn.execute(get_location_id, (d['location']['name'],))
                location_id_result = postgres_conn.fetchone()
                if location_id_result is None:
                    logging.info(f"City {d['location']['name']} not found, inserting...")
                    insert_data_location_weather(d, postgres_conn)
                    postgres_conn.execute(get_location_id, (d['location']['name']))
                    location_id_result = postgres_conn.fetchone()
                location_id = location_id_result[0]
            except Exception as e:
                 logging.error(f"Error inserting location in today_day_weather: {e} in {inspect.currentframe().f_code.co_name}")

            get_date_id = """
                SELECT date_id
                FROM date_weather
                WHERE day = %s and month = %s and year = %s
            """

            localtime = d['location']['localtime']
            year, month, day = map(int, localtime.split()[0].split('-'))     

            try:
                postgres_conn.execute(get_date_id, (day, month, year))
                date_id_result = postgres_conn.fetchone()
                if date_id_result is None:
                    logging.info(f"City {localtime} not found, inserting...")
                    insert_data_date_weather(d, postgres_conn)
                    postgres_conn.execute(get_date_id, (day, month, year))
                    date_id_result = postgres_conn.fetchone()
                    if date_id_result is None:
                        logging.error(f"Failed to retrieve date_id for {day}-{month}-{year}")
                        continue
                date_id = date_id_result[0]
            except Exception as e:
                 logging.error(f"Error inserting date weather in today_day_weather: {e} in {inspect.currentframe().f_code.co_name}")
      


            # location_id = postgres_conn.fetchone()[0]
            # postgres_conn.execute(get_location_id, (location_id, ))
            temp_avg = d['current']['temp_c']
            temp_min = d['current']['temp_c']
            temp_max = d['current']['temp_c']
            wind_avg = d['current']['wind_kph']
            wind_min = d['current']['wind_kph']
            wind_max = d['current']['wind_kph']
            humidity_avg = d['current']['humidity']
            humidity_min = d['current']['humidity']
            humidity_max = d['current']['humidity']


            

            insert_data_today_day_weather = """
                INSERT INTO today_day_weather (
                    location_id,
                    temp_avg, temp_min, temp_max,
                    wind_avg, wind_min, wind_max, 
                    humidity_avg, humidity_min, humidity_max,
                    date_id
                    )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            postgres_conn.execute(insert_data_today_day_weather, (
                location_id,
                temp_avg, temp_min, temp_max,
                wind_avg, wind_min, wind_max,
                humidity_avg, humidity_min, humidity_max,
                date_id
                ))

    except Exception as e:
        logging.error(f"Error inserting today weather: {e} in {inspect.currentframe().f_code.co_name}")


def main():
    api_connect = DataInsert(CITIES)
    data = api_connect.getdata(APPROACH)
    postgres_conn = api_connect.postgres_conn()

    if postgres_conn:
        try:
            insert_data_location_weather(data, postgres_conn)
            insert_data_date_weather(data, postgres_conn)
            insert_data_today_day_weather(data, postgres_conn)
            postgres_conn.connection.commit()
        except Exception as e:
            logging.error(f"Error during main execution: {e}")
        finally:
            postgres_conn.connection.close()

    else:
        logging.error("Failed to connect to the database.")

main()


# with DAG(
#     dag_id = 'insert_data_in_pg',
#     tags = ['daily', 'pg'],
#     description = 'dag that push data to pg db',
#     schedule_interval = '0 0 * * *',
#     default_arg = default_args

# ) as main_dag:
#     download_data = PythonOperator(
# 		task_id = 'insert_current_data',
# 		python_callable = insert_current_data # функция которую он должен исполнять

#     )
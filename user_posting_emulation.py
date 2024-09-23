import requests
from time import sleep
import random
from multiprocessing import Process
import json
import sqlalchemy
from sqlalchemy import text
from datetime import datetime
import yaml


# Load database credentials from db_creds.yaml
def load_db_credentials():
    with open('db_creds.yaml', 'r') as file:
        return yaml.safe_load(file)

random.seed(100)

class AWSDBConnector:

    def __init__(self):
        creds = load_db_credentials()  # Load credentials from YAML
        self.HOST = creds['HOST']
        self.USER = creds['USER']
        self.PASSWORD = creds['PASSWORD']
        self.DATABASE = creds['DATABASE']
        self.PORT = creds['PORT']

    def create_db_connector(self):
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine

new_connector = AWSDBConnector()
engine = new_connector.create_db_connector()  # Integrated here

# Function to convert datetime objects to string
def handle_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def send_to_kafka(api_url, payload):
    headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps({"records": [{"value": payload}]}, default=handle_datetime))
        if response.status_code != 200:
            print(f"Failed to send data to {api_url}: {response.status_code}, {response.text}")
        else:
            print(f"Data sent successfully to {api_url}")
    except requests.exceptions.RequestException as e:
        print(f"Network error sending data to {api_url}: {e}")

def run_infinite_post_data_loop():  # Start of the loop function
    while True:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)

        with engine.connect() as connection:
            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            for row in pin_selected_row:
                pin_result = dict(row._mapping)

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            for row in geo_selected_row:
                geo_result = dict(row._mapping)

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            for row in user_selected_row:
                user_result = dict(row._mapping)

            print(pin_result)
            print(geo_result)
            print(user_result)

            # Sending the data to the corresponding Kafka topics
            invoke_url_pin = "https://315qr5in54.execute-api.us-east-1.amazonaws.com/Dev/topics/1226d593b7e7.pin"
            invoke_url_geo = "https://315qr5in54.execute-api.us-east-1.amazonaws.com/Dev/topics/1226d593b7e7.geo"
            invoke_url_user = "https://315qr5in54.execute-api.us-east-1.amazonaws.com/Dev/topics/1226d593b7e7.user"

            send_to_kafka(invoke_url_pin, pin_result)
            send_to_kafka(invoke_url_geo, geo_result)
            send_to_kafka(invoke_url_user, user_result)

if __name__ == "__main__":
    run_infinite_post_data_loop()
    print('Working')

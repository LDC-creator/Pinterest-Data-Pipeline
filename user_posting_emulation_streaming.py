import requests
from time import sleep
import random
import sqlalchemy
from sqlalchemy import text
import json
from datetime import datetime

random.seed(100)

class AWSDBConnector:
    '''
    A connector to an AWS database containing Pinterest data.
    '''
    def __init__(self):
        '''
        Constructs all the necessary attributes for the AWSDBConnector object.
        '''
        self.HOST = "pinterestdbreadonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com"
        self.USER = 'project_user'
        self.PASSWORD = ':t%;yCY3Yjg'
        self.DATABASE = 'pinterest_data'
        self.PORT = 3306
        
    def create_db_connector(self):
        '''
        Creates connection to the AWS database containing Pinterest data.
        '''
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine

new_connector = AWSDBConnector()

def run_infinite_post_data_loop():
    '''
    Runs an infinite post data loop to continuously receive and output data into three tables.
    Then sends this data to an API to send the data to three AWS Kinesis streams. 
    '''
    while True:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

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

            # Convert datetime to string if necessary
            if isinstance(geo_result["timestamp"], datetime):
                geo_result["timestamp"] = geo_result["timestamp"].isoformat()  # Convert to ISO format

            if isinstance(user_result["date_joined"], datetime):
                user_result["date_joined"] = user_result["date_joined"].isoformat()  # Convert to ISO format

            # Invoke URLs for Kinesis streams
            invoke_url_pin = "https://315qr5in54.execute-api.us-east-1.amazonaws.com/Dev/streams/streaming-1226d593b7e7-pin/record"
            pin_data = json.dumps({
                "StreamName": "streaming-1226d593b7e7-pin",
                "Data": {
                    "index": pin_result["index"],
                    "unique_id": pin_result["unique_id"],
                    "title": pin_result["title"], 
                    "description": pin_result["description"],
                    "poster_name": pin_result["poster_name"],
                    "follower_count": pin_result["follower_count"],
                    "tag_list": pin_result["tag_list"],
                    "is_image_or_video": pin_result["is_image_or_video"],
                    "image_src": pin_result["image_src"],
                    "downloaded": pin_result["downloaded"],
                    "save_location": pin_result["save_location"],
                    "category": pin_result["category"]
                },
                "PartitionKey": "test"
            })

            headers = {'Content-Type': 'application/json'}
            pin_response = requests.put(invoke_url_pin, headers=headers, data=pin_data)

            invoke_url_geo = "https://315qr5in54.execute-api.us-east-1.amazonaws.com/Dev/streams/streaming-1226d593b7e7-geo/record"
            geo_data = json.dumps({
                "StreamName": "streaming-1226d593b7e7-geo",
                "Data": {
                    "ind": geo_result["ind"],
                    "timestamp": geo_result["timestamp"],  # Now a string
                    "latitude": geo_result["latitude"], 
                    "longitude": geo_result["longitude"],
                    "country": geo_result["country"]
                },
                "PartitionKey": "test"
            })

            geo_response = requests.put(invoke_url_geo, headers=headers, data=geo_data)

            invoke_url_user = "https://315qr5in54.execute-api.us-east-1.amazonaws.com/Dev/streams/streaming-1226d593b7e7-user/record"
            user_data = json.dumps({
                "StreamName": "streaming-1226d593b7e7-user",
                "Data": {
                    "ind": user_result["ind"],
                    "first_name": user_result["first_name"],
                    "last_name": user_result["last_name"], 
                    "age": user_result["age"],
                    "date_joined": user_result["date_joined"]  # Now a string
                },
                "PartitionKey": "test"
            })

            user_response = requests.put(invoke_url_user, headers=headers, data=user_data)

            print(pin_response.status_code)
            print(geo_response.status_code)
            print(user_response.status_code)

if __name__ == "__main__":
    run_infinite_post_data_loop()

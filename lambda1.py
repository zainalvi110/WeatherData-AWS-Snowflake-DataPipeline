import json

# http://api.weatherapi.com/v1/current.json?key=&q=India&aqi=no
from datetime import datetime
import requests  
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("weather")#your dynamodb table name

def get_weather_data(city):  
    api_url = "http://api.weatherapi.com/v1/current.json"
    params = {  
        "q": city,    
        "key": "<your_key>"#api key here
    }  
    response = requests.get(api_url, params=params)  
    data = response.json()  
    return data  
    
    

def lambda_handler(event, context):

    cities = ["Bangalore","Delhi","Mumbai","Chennai","Kashmir","Dehradun","Kochi","Kerela","Hyderabad","Sikkim"] #change the names of cities you want the data to load
    for city in cities:
        data = get_weather_data(city)  
    
        temp = data['current']['temp_c']
        wind_speed = data['current']['wind_mph']
        wind_dir = data['current']['wind_dir']
        pressure_mb = data['current']['pressure_mb']
        humidity = data['current']['humidity']
    
        print(city,temp,wind_speed,wind_dir,pressure_mb,humidity)
        current_timestamp = datetime.utcnow().isoformat()
        
        item = {
                'city': city,
                'time': str(current_timestamp),
                'temp': temp,
                'wind_speed': wind_speed,
                'wind_dir': wind_dir,
                'pressure_mb': pressure_mb,
                'humidity': humidity
            }
        item = json.loads(json.dumps(item), parse_float=Decimal)
        # Insert data into DynamoDB
        table.put_item(
            Item=item
        )
    

 
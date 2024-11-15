import random
import datetime
import time
import threading

heartbeat_data = []  

def generate_heartbeat():
    while True:
        user_id = random.randint(1, 100)
        timestamp = datetime.datetime.now().isoformat()
        heart_rate = random.randint(60, 100)

        heartbeat_data.append({
            'userId': user_id,
            'timestamp': timestamp,
            'heartRate': heart_rate
        })

        time.sleep(60)  


def get_latest_heartbeats(limit=100):
    
    if heartbeat_data:
        return heartbeat_data[-limit:]
    return None  

temperature_data = []

def generate_temperature():
    while True:
        user_id = random.randint(1, 100)
        timestamp = datetime.datetime.now().isoformat()
        temperature = random.randint(30,40)

        temperature_data.append({
            'userId': user_id,
            'timestamp': timestamp,
            'temperature': temperature
        })

        time.sleep(60)  

def get_latest_temperature():
    if temperature_data:
        return temperature_data[-1:]
    return None  

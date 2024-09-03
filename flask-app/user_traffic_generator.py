import requests
import threading
import time
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the target FastAPI app's base URL
TARGET_APP_URL = "http://app-a:8000"

@app.route('/call_url', methods=['GET'])
def call_url():
    url = TARGET_APP_URL
    response = requests.get(url)
    start_time = time.time()
    endpoint = "/"
    frequency = 1
    duration = 100
    while time.time() - start_time < duration:
        try:
            url = f"{TARGET_APP_URL}"
            response = requests.get(url)
            print(f"Request to {url} - Status: {response.status_code}")
        except Exception as e:
            print(f"Error during request: {e}")
    time.sleep(frequency)
    return

def generate_random_data(endpoint):
    if endpoint == "/items/{item_id}":
        item_id = random.randint(1, 100)  # Random item_id between 1 and 100
        q = random.choice(['foo', 'bar', 'baz'])  # Random query parameter
        return f"/items/{item_id}?q={q}"

    elif endpoint == "/random_status":
        status_code = random.choice([200, 300, 400, 500])
        return f"/random_status?status_code={status_code}"
    
    elif endpoint == "/chain":
        return endpoint  # This endpoint doesn't require additional data

    # Add more cases for different endpoints if needed
    return endpoint

def generate_traffic(endpoint, frequency, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            randomized_endpoint = generate_random_data(endpoint)
            url = f"{TARGET_APP_URL}{randomized_endpoint}"
            response = requests.get(url)
            print(f"Request to {url} - Status: {response.status_code}")
        except Exception as e:
            print(f"Error during request: {e}")
        time.sleep(frequency)

@app.route('/')
def home():
    return jsonify({"message": "Traffic generation started"}), 200    

# @app.route('/generate_traffic', methods=['POST'])
# def generate_traffic_route():
#     data = request.json
#     endpoint = data.get('endpoint', '/')
#     frequency = data.get('frequency', 1)
#     duration = data.get('duration', 10)

#     threading.Thread(target=generate_traffic, args=(endpoint, frequency, duration)).start()
#     return jsonify({"message": "Traffic generation started", "endpoint": endpoint}), 200

# @app.route('/generate_bulk_traffic', methods=['POST'])
# def generate_bulk_traffic():
#     data = request.json
#     frequency = data.get('frequency', 1)
#     duration = data.get('duration', 10)
    
#     endpoints = [
#         "/",
#         "/items/{item_id}",
#         "/io_task",
#         "/cpu_task",
#         "/random_status",
#         "/random_sleep",
#         "/error_test",
#         "/chain"
#     ]

#     for endpoint in endpoints:
#         threading.Thread(target=generate_traffic, args=(endpoint, frequency, duration)).start()

#     return jsonify({"message": "Bulk traffic generation started"}), 200

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5123, debug=True)

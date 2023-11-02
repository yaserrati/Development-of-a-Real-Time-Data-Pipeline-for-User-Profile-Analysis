from kafka import KafkaProducer
import json
import requests
import time

topic = "randomuser_data"
kafka_config = {
    "bootstrap_servers": "localhost:9092",  # Change this to your Kafka server address
}

producer = KafkaProducer(bootstrap_servers=kafka_config["bootstrap_servers"])

while True:
    try:
        # Fetch user data from the RandomUser.me API
        response = requests.get('https://randomuser.me/api/')
        response.raise_for_status()  # Raise an exception if the response is not successful

        # Check if the response is not empty
        if response.text.strip():
            # Attempt to parse the response as JSON
            user_data = response.json()

            # Serialize user data to JSON
            user_data_json = json.dumps(user_data)

            # Print the fetched data
            print("Fetched user data:")
            print(user_data_json)

            # Send the data to Kafka
            producer.send(topic, value=user_data_json.encode("utf-8"))
            producer.flush()
        else:
            print("Error: Empty response from the API")

    except requests.exceptions.RequestException as e:
        print(f"Error: An HTTP request error occurred - {e}")

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON response from the API - {e}")

    except Exception as e:
        print(f"An unexpected error occurred - {e}")

    # Add a delay of 6 seconds before the next data collection
    time.sleep(6)

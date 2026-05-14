import time
import json
import random
from kafka import KafkaProducer

def run_edge_scanner():
    print("[EDGE ENGINE] Initializing secure telemetry connection to central cloud...")
    # Connects to the local Kafka broker running in your docker stack
    try:
        producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    except Exception as e:
        print(f"[ERROR] Failed to connect to Kafka: {e}. Ensure docker is running.")
        return

    # Simulated inventory of valid sovereign bills in circulation
    tracked_bills = [f"USD100_SER_{random.randint(10000, 99999)}" for _ in range(5)]
    locations = ["Houston_Airport_Gate4", "New_York_Fed_Vault", "Miami_Port_Container_B"]

    print("[EDGE ENGINE] Systems online. Streaming currency scans asynchronously...")
    while True:
        # Choose a random bill and scanner location
        bill_id = random.choice(tracked_bills)
        location = random.choice(locations)
        
        payload = {
            "serial_number": bill_id,
            "timestamp": time.time(),
            "location_id": location
        }
        
        producer.send('currency-streams', payload)
        print(f"[SCAN EVENT] Banknote {bill_id} swiped at location: {location}")
        
        # Simulating realistic velocity of money
        time.sleep(random.uniform(0.5, 2.0))

if __name__ == "__main__":
    run_edge_scanner()

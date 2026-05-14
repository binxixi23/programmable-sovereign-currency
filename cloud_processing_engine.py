import json
import time
from kafka import KafkaConsumer
from cassandra.cluster import Cluster

def run_cloud_engine():
    print("[CLOUD ENGINE] Initializing ledger runtime...")
    
    # 1. Connect to high-throughput ScyllaDB Cluster
    try:
        cluster = Cluster(['localhost'], port=9042)
        session = cluster.connect()
        # Initialize national table infrastructure if not existing
        session.execute("CREATE KEYSPACE IF NOT EXISTS sovereign_ledger WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};")
        session.execute("USE sovereign_ledger;")
        session.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                serial_number text,
                transaction_time timestamp,
                location_id text,
                status text,
                PRIMARY KEY (serial_number, transaction_time)
            ) WITH CLUSTERING ORDER BY (transaction_time DESC);
        """)
        print("[DATABASE] Connected cleanly to ScyllaDB Ledger.")
    except Exception as e:
        print(f"[DATABASE ERROR] Could not bind to ScyllaDB: {e}")
        return

    # 2. Bind to Kafka transaction stream
    try:
        consumer = KafkaConsumer(
            'currency-streams',
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='latest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        print("[INGESTION] Connected to Kafka stream pipelines.")
    except Exception as e:
        print(f"[INGESTION ERROR] Kafka connection crashed: {e}")
        return

    # Local runtime cache to monitor real-time velocity metrics without heavy queries
    in_memory_state = {}

    print("[SYSTEM READY] Processing sovereign transactions. Watching for security anomalies...")
    for message in consumer:
        tx_data = message.value
        serial = tx_data["serial_number"]
        current_loc = tx_data["location_id"]
        current_time = tx_data["timestamp"]
        
        status = "ACTIVE"
        
        # 3. AI Velocity Engine: Detect mathematical anomalies (cloned currency bills)
        if serial in in_memory_state:
            last_record = in_memory_state[serial]
            time_delta = current_time - last_record["timestamp"]
            
            # If the identical unique bill ID appears at two different locations within 2 seconds
            if current_loc != last_record["location_id"] and time_delta < 2.0:
                status = "VOIDED_CRITICAL"
                print(f"\n[🚨 SECURITY ALERT] COUNTERFEIT CLONE DETECTED FOR {serial}!")
                print(f"-> Last seen: {last_record['location_id']} ({time_delta:.2f}s ago)")
                print(f"-> Threat vector caught at: {current_loc}. Freezing bill assets across global nodes.\n")

        # Update system state
        in_memory_state[serial] = {"location_id": current_loc, "timestamp": current_time}
        
        # 4. Write immutable record back to the ScyllaDB database cluster
        insert_stmt = session.prepare("""
            INSERT INTO transactions (serial_number, transaction_time, location_id, status)
            VALUES (?, toTimestamp(now()), ?, ?)
        """)
        session.execute(insert_stmt, (serial, current_loc, status))

if __name__ == "__main__":
    run_cloud_engine()

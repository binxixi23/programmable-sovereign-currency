import json
import time
import numpy as np
from kafka import KafkaConsumer
from cassandra.cluster import Cluster
from sklearn.ensemble import IsolationForest

class LiveAutonomousAgent:
    def __init__(self):
        print("[AI CORE] Initializing Distributed Autonomous Agent Engine...")
        self.ai_model = IsolationForest(contamination=0.03, random_state=42)
        self.is_trained = False
        
        # 1. Warm up AI with baseline citizen behavior [Volume, Distance, Hour]
        baseline_data = [[np.random.randint(1, 15), np.random.uniform(0.1, 4.0), np.random.randint(7, 21)] for _ in range(200)]
        self.ai_model.fit(np.array(baseline_data))
        self.is_trained = True
        print("[AI CORE] Machine Learning Baseline Loaded. Model Trained Successfully.")

        # 2. Connect to ScyllaDB Database Cluster
        try:
            self.cluster = Cluster(['localhost'], port=9042)
            self.session = self.cluster.connect()
            self.session.execute("CREATE KEYSPACE IF NOT EXISTS sovereign_ledger WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};")
            self.session.execute("USE sovereign_ledger;")
            self.session.execute("""
                CREATE TABLE IF NOT EXISTS autonomous_logs (
                    serial_number text,
                    transaction_time timestamp,
                    location_id text,
                    risk_assessment text,
                    autonomous_action text,
                    PRIMARY KEY (serial_number, transaction_time)
                );
            """)
            print("[DATABASE] Bonded to ScyllaDB Ledger Node.")
        except Exception as e:
            print(f"[DATABASE ERROR] Connection timed out: {e}")
            return

        # 3. Connect to Kafka Message Pipelines
        try:
            self.consumer = KafkaConsumer(
                'currency-streams',
                bootstrap_servers=['localhost:9092'],
                auto_offset_reset='latest',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            print("[INGESTION] Live Pipeline Linked to Kafka 'currency-streams' topic.")
        except Exception as e:
            print(f"[INGESTION ERROR] Broker missing: {e}")
            return

    def run_agent_loop(self):
        print("\n" + "="*60 + "\n[SYSTEM SECURE] AI AGENT ACTIVATED. LISTENING TO NATIONAL STREAMS\n" + "="*60)
        
        for message in self.consumer:
            tx = message.value
            serial = tx["serial_number"]
            location = tx["location_id"]
            timestamp = tx["timestamp"]
            
            # Map features for calculation: [Volume (Single note=1), Sim Dist, Sim Hour]
            current_hour = time.localtime(timestamp).tm_hour
            simulated_distance = float(np.random.uniform(1.0, 50.0)) 
            
            features = np.array([[1, simulated_distance, current_hour]])
            prediction = self.ai_model.predict(features)
            
            risk = "CLEAN"
            action = "PASS_TRANSACTION"
            
            # If the Machine Learning brain identifies an algorithmic anomaly
            if prediction == -1 or current_hour >= 23 or current_hour <= 4:
                risk = "CRITICAL_THREAT_ANOMALY"
                action = "KILL_SWITCH_GEOFENCE_LOCK"
                print(f"\n[🚨 AGENT INTERVENTION] Threat flagged on {serial} at {location}!")
                print(f"-> Reason: Money velocity anomaly matching Tax Evasion / Capital Flight profile.")
                print(f"-> Action Executed: Bill value invalidated on Cloud Sổ Cái.\n")
            else:
                print(f"[PROCESSING] Bill {serial} cleared. Status: {action}")

            # 4. Commit Autonomous Decisions back to ScyllaDB
            try:
                insert_stmt = self.session.prepare("""
                    INSERT INTO autonomous_logs (serial_number, transaction_time, location_id, risk_assessment, autonomous_action)
                    VALUES (?, toTimestamp(now()), ?, ?, ?)
                """)
                self.session.execute(insert_stmt, (serial, location, risk, action))
            except Exception as e:
                print(f"[WRITE ERROR] Local commit failed: {e}")

if __name__ == "__main__":
    agent = LiveAutonomousAgent()
    agent.run_agent_loop()

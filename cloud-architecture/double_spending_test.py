import unittest
import time

class SovereignCloudLedger:
    def __init__(self):
        # Simulated In-Memory High-Speed Database (e.g., Redis/ScyllaDB Shard)
        # Structure: {serial_number: {"last_seen_loc": str, "timestamp": float, "status": str}}
        self.ledger = {
            "USD100_SER_99182": {"last_seen_loc": "Houston_ATM_01", "timestamp": time.time(), "status": "ACTIVE"}
        }

    def process_transaction(self, serial: str, location: str) -> str:
        current_time = time.time()
        
        if serial not in self.ledger:
            return "REJECTED: UNKNOWN_SERIAL"
            
        record = self.ledger[serial]
        
        if record["status"] == "VOIDED":
            return "ALARM: VOIDED_CURRENCY_DETECTED"

        # Double-Spending Velocity Check (Geographical Anomaly Detection)
        time_delta = current_time - record["timestamp"]
        if location != record["last_seen_loc"] and time_delta < 2.0:  # If seen in 2 locations under 2 seconds
            record["status"] = "VOIDED"  # Instantly kill the currency value
            return "CRITICAL_ALARM: DOUBLE_SPENDING_DETECTED_BILL_VOIDED"

        # Update valid tracking log
        record["last_seen_loc"] = location
        record["timestamp"] = current_time
        return "APPROVED"

class TestCloudLedger(unittest.TestCase):
    def test_counterfeit_cloning_detection(self):
        cloud = SovereignCloudLedger()
        
        # Real bill scanned in Houston
        res1 = cloud.process_transaction("USD100_SER_99182", "Houston_ATM_01")
        self.assertEqual(res1, "APPROVED")
        
        # Cloned counterfeit bill instantly scanned in New York 0.5 seconds later
        res2 = cloud.process_transaction("USD100_SER_99182", "New_York_Airport_Gates")
        self.assertEqual(res2, "CRITICAL_ALARM: DOUBLE_SPENDING_DETECTED_BILL_VOIDED")

if __name__ == "__main__":
    unittest.main()

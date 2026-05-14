import time

class CommercialPOSCounter:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.local_cache_blacklist = set(["BAD_SER_001", "STOLEN_SER_772"])
        self.transaction_batch = []

    def scan_banknote(self, scanned_serial: str):
        """
        Processes banknotes instantly at the edge counter.
        Fails fast if the bill matches the local emergency blacklist cached from Cloud.
        """
        if scanned_serial in self.local_cache_blacklist:
            return "ALERT_TILL_LOCKED: FRAUDULENT_BANKNOTE"
            
        # Batching transactions asynchronously to optimize Cloud TPS limit
        self.transaction_batch.append({
            "serial": scanned_serial,
            "timestamp": time.time()
        })
        
        if len(self.transaction_batch) >= 100:
            self.flush_batch_to_kafka_queue()
            
        return "LOCAL_VALIDATION_SUCCESS"

    def flush_batch_to_kafka_queue(self):
        print(f"[EDGE-{self.node_id}] Pushing batch of {len(self.transaction_batch)} transactions to Kafka.")
        self.transaction_batch.clear()

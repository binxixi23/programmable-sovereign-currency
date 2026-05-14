import hashlib
import os

class SovereignRFIDChip:
    def __init__(self, permanent_serial: str, master_key: bytes):
        """
        Simulates the hard-wired, write-once-read-many (WORM) memory layout
        of the ultra-thin sovereign banknote chip.
        """
        self._permanent_serial = permanent_serial
        self._master_key = master_key

    def respond_to_scanner(self, challenge_nonce: bytes) -> dict:
        """
        Challenge-Response Mechanism.
        Does NOT emit the real serial number to prevent illicit tracking.
        Generates a dynamic pseudo-random token instead.
        """
        # Generate dynamic cryptographic token
        hmac_engine = hashlib.sha256()
        hmac_engine.update(self._permanent_serial.encode('utf-8'))
        hmac_engine.update(self._master_key)
        hmac_engine.update(challenge_nonce)
        dynamic_token = hmac_engine.hexdigest()
        
        return {
            "status": "ENCRYPTED_HANDSHAKE",
            "ephemeral_token": dynamic_token
        }

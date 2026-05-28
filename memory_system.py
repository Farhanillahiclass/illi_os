"""
ILLI Local Memory System: Long-term preference and context memory using SQLite.
Persists user preferences, voice profiles, and interaction history.
"""
import json
import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
import threading

logger = logging.getLogger(__name__)

class LocalMemorySystem:
    """
    Long-term preference and context memory using SQLite.
    Persists user preferences, voice profiles, and interaction history.
    """
    
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or Path.home() / ".illi_memory" / "cognition.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()
        
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize SQLite database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    type TEXT,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS voice_profiles (
                    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    voice_type TEXT,
                    pitch REAL,
                    rate REAL,
                    volume REAL,
                    enabled BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS interaction_history (
                    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    input_type TEXT,
                    input_text TEXT,
                    response_text TEXT,
                    status TEXT,
                    metadata TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS mic_calibration (
                    calibration_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ambient_noise_level REAL,
                    calibrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    environment TEXT
                )
            """)
            
            conn.commit()
        
        logger.info(f"Memory system initialized: {self.db_path}")
    
    def set_preference(self, key: str, value: Any, value_type: str = "string") -> bool:
        """Set user preference in memory."""
        try:
            with self.lock:
                with sqlite3.connect(self.db_path) as conn:
                    json_value = json.dumps(value) if not isinstance(value, str) else value
                    conn.execute(
                        "INSERT OR REPLACE INTO preferences (key, value, type) VALUES (?, ?, ?)",
                        (key, json_value, value_type)
                    )
                    conn.commit()
            logger.info(f"Preference set: {key}={value}")
            return True
        except Exception as e:
            logger.error(f"Failed to set preference: {str(e)}")
            return False
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Retrieve user preference from memory."""
        try:
            with self.lock:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.execute(
                        "SELECT value, type FROM preferences WHERE key = ?",
                        (key,)
                    )
                    row = cursor.fetchone()
                    
                    if row:
                        value, value_type = row
                        if value_type != "string": # Attempt to deserialize if not a simple string
                            return json.loads(value)
                        return value
        except Exception as e:
            logger.error(f"Failed to get preference: {str(e)}")
        
        return default
    
    def add_interaction_record(self, input_type: str, input_text: str, 
                               response_text: str, status: str = "success", 
                               metadata: Optional[Dict] = None) -> bool:
        """Log interaction for context learning."""
        try:
            with self.lock:
                with sqlite3.connect(self.db_path) as conn:
                    metadata_json = json.dumps(metadata or {})
                    conn.execute(
                        """INSERT INTO interaction_history 
                           (input_type, input_text, response_text, status, metadata)
                           VALUES (?, ?, ?, ?, ?)""",
                        (input_type, input_text, response_text, status, metadata_json)
                    )
                    conn.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to record interaction: {str(e)}")
            return False
    
    def store_mic_calibration(self, ambient_noise_level: float, environment: str = "unknown"):
        """Store microphone calibration data."""
        # This method is specific to mic calibration, consider moving to mic_calibration.py
        # or keeping a generic 'store_sensor_data'
        try:
            with self.lock:
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute(
                        """INSERT INTO mic_calibration (ambient_noise_level, environment)
                           VALUES (?, ?)""",
                        (ambient_noise_level, environment)
                    )
                    conn.commit()
            logger.info(f"Mic calibration stored: {ambient_noise_level} dB in {environment}.")
            return True
        except Exception as e:
            logger.error(f"Failed to store calibration: {str(e)}")
            return False
    
    def get_latest_mic_calibration(self) -> Optional[float]:
        """Get latest microphone calibration level."""
        # This method is specific to mic calibration, consider moving to mic_calibration.py
        try:
            with self.lock:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.execute(
                        "SELECT ambient_noise_level FROM mic_calibration ORDER BY calibration_id DESC LIMIT 1"
                    )
                    row = cursor.fetchone()
                    return row if row else None
        except Exception as e:
            logger.error(f"Failed to get calibration: {str(e)}")
            return None
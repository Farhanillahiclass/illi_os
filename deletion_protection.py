"""
ILLI Handshake Deletion Protection: Confirmation system for destructive operations.
Voice/text confirmation handshake required before destructive operations.
"""
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

class HandshakeDeleteProtection:
    """
    Deletion confirmation system preventing accidental file/folder destruction.
    Voice/text confirmation handshake required before destructive operations.
    """
    
    def __init__(self, confirmation_callback: Optional[callable] = None):
        self.confirmation_callback = confirmation_callback
        self.pending_confirmations = {}
    
    def request_deletion_confirmation(self, target_path: Path, operation: str = "delete") -> str:
        """
        Request user confirmation before destructive operation.
        Returns confirmation token.
        """
        confirmation_id = f"{int(datetime.now().timestamp() * 1000)}"
        
        self.pending_confirmations[confirmation_id] = {
            "target": str(target_path),
            "operation": operation,
            "status": "PENDING",
            "created_at": datetime.now().isoformat(),
        }
        
        message = f"HANDSHAKE: Confirm {operation} of '{target_path.name}'? Reply 'YES' or 'NO'."
        
        if self.confirmation_callback:
            self.confirmation_callback(message)
        
        logger.warning(f"Deletion handshake initiated: {target_path}.")
        return confirmation_id
    
    def confirm_deletion(self, confirmation_id: str, user_response: str) -> bool:
        """Process user confirmation response."""
        if confirmation_id not in self.pending_confirmations:
            logger.error(f"Unknown confirmation ID: {confirmation_id}.")
            return False
        
        confirmation = self.pending_confirmations[confirmation_id]
        user_response_upper = user_response.strip().upper()
        
        if user_response_upper in ["YES", "Y", "CONFIRM", "PROCEED"]:
            confirmation["status"] = "CONFIRMED"
            logger.info(f"Deletion confirmed: {confirmation['target']}.")
            return True
        else:
            confirmation["status"] = "REJECTED"
            logger.info(f"Deletion rejected: {confirmation['target']}.")
            return False
    
    def get_pending_confirmations(self) -> List[Dict]:
        """Get all pending confirmation requests."""
        return list(self.pending_confirmations.values())
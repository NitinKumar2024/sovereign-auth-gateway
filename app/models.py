from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

class User:
    """
    The core User model for the Sovereign Auth Gateway.
    Handles data structuring and password cryptography.
    """
    def __init__(self, email, password, role="student"):
        self.email = email
        # We NEVER store the raw password. We hash it immediately.
        self.password_hash = generate_password_hash(password)
        self.role = role
        self.created_at = datetime.now(timezone.utc)

    def to_dict(self):
        """
        Converts the Python object into a dictionary so MongoDB can store it.
        """
        return {
            "email": self.email,
            "password_hash": self.password_hash,
            "role": self.role,
            "created_at": self.created_at
        }

    @staticmethod
    def verify_password(stored_hash, provided_password):
        """
        Safely compares a raw password against the database hash during login.
        """
        return check_password_hash(stored_hash, provided_password)
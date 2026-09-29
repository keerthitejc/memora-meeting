import os
import sqlite3
import hashlib
import secrets
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("memora.db_service")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "memora.db")

class DatabaseService:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initialize database tables for users and authentication."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id TEXT PRIMARY KEY,
                        email TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        salt TEXT NOT NULL,
                        name TEXT NOT NULL,
                        role TEXT DEFAULT 'Member',
                        avatar TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                logger.info(f"Database initialized successfully at {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")

    def _hash_password(self, password: str, salt: Optional[str] = None) -> tuple[str, str]:
        if not salt:
            salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return hashed, salt

    def register_user(self, email: str, password: str, name: str, role: str = "User") -> Dict[str, Any]:
        email_clean = email.strip().lower()
        if not email_clean or not password:
            raise ValueError("Email and password are required")

        password_hash, salt = self._hash_password(password)
        user_id = f"user_{secrets.token_hex(8)}"
        avatar = f"https://api.dicebear.com/7.x/avataaars/svg?seed={user_id}"

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (id, email, password_hash, salt, name, role, avatar) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (user_id, email_clean, password_hash, salt, name, role, avatar)
                )
                conn.commit()
                return {
                    "id": user_id,
                    "email": email_clean,
                    "name": name,
                    "role": role,
                    "avatar": avatar
                }
        except sqlite3.IntegrityError:
            raise ValueError("An account with this email already exists.")

    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        email_clean = email.strip().lower()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email_clean,))
            row = cursor.fetchone()
            if not row:
                return None

            user_dict = dict(row)
            computed_hash, _ = self._hash_password(password, user_dict["salt"])
            if secrets.compare_digest(computed_hash, user_dict["password_hash"]):
                return {
                    "id": user_dict["id"],
                    "email": user_dict["email"],
                    "name": user_dict["name"],
                    "role": user_dict["role"],
                    "avatar": user_dict["avatar"] or f"https://api.dicebear.com/7.x/avataaars/svg?seed={user_dict['id']}"
                }
            return None

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        email_clean = email.strip().lower()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, email, name, role, avatar FROM users WHERE email = ?", (email_clean,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

db_service = DatabaseService()

"""
User Model for Authentication
"""
import hashlib
import sqlite3
from datetime import datetime
from database import db


class User:
    """User model for authentication"""
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def create(username, email, password, full_name=None, role='user'):
        """Create a new user"""
        password_hash = User.hash_password(password)
        
        try:
            db.execute('''
                INSERT INTO users (username, email, password_hash, full_name, role)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password_hash, full_name, role))
            
            # Get the created user
            user = User.get_by_username(username)
            return user
        except sqlite3.IntegrityError:
            return None  # Username or email already exists
    
    @staticmethod
    def get_by_username(username):
        """Get user by username"""
        return db.fetch_one('SELECT * FROM users WHERE username = ?', (username,))
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        return db.fetch_one('SELECT * FROM users WHERE email = ?', (email,))
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        return db.fetch_one('SELECT * FROM users WHERE id = ?', (user_id,))
    
    @staticmethod
    def verify_password(user, password):
        """Verify user password"""
        if not user:
            return False
        password_hash = User.hash_password(password)
        return user['password_hash'] == password_hash
    
    @staticmethod
    def update_last_login(user_id):
        """Update last login timestamp"""
        db.execute('''
            UPDATE users SET updated_at = ? WHERE id = ?
        ''', (datetime.now().isoformat(), user_id))


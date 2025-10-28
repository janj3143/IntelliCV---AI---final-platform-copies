"""
Secure Authentication Module for IntelliCV Admin Portal
Provides the missing SecureAuth class referenced in main.py
"""

import sqlite3
import hashlib
import secrets
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple
import streamlit as st

class SecureAuth:
    """Compatible SecureAuth class for existing main.py integration"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or "secure_credentials.db"
        self.max_attempts = 3
        self.lockout_duration = 30 * 60  # 30 minutes in seconds
        self.session_timeout = 60 * 60   # 60 minutes in seconds
        self.inactivity_timeout = 30 * 60  # 30 minutes in seconds
        
        self._init_database()
        
        # Create default admin user if not exists
        if not self._user_exists("admin"):
            self._create_user("admin", "JanJ!3143@?")
    
    def _init_database(self):
        """Initialize SQLite database for authentication"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    failed_attempts INTEGER DEFAULT 0,
                    locked_until INTEGER DEFAULT 0,
                    last_login INTEGER DEFAULT 0,
                    last_activity INTEGER DEFAULT 0,
                    session_token TEXT
                )
            ''')
            
            # Login attempts log
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS login_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    timestamp INTEGER NOT NULL,
                    success INTEGER NOT NULL,
                    ip_address TEXT
                )
            ''')
            
            conn.commit()
    
    def _hash_password(self, password: str, salt: str = None) -> Tuple[str, str]:
        """Hash password with salt"""
        if salt is None:
            salt = secrets.token_hex(32)
        
        password_hash = hashlib.pbkdf2_hmac(
            'sha256', 
            password.encode('utf-8'),
            salt.encode('utf-8'), 
            100000
        ).hex()
        
        return password_hash, salt
    
    def _create_user(self, username: str, password: str):
        """Create a new user"""
        password_hash, salt = self._hash_password(password)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO users 
                (username, password_hash, salt) 
                VALUES (?, ?, ?)
            ''', (username, password_hash, salt))
            conn.commit()
    
    def _user_exists(self, username: str) -> bool:
        """Check if user exists"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM users WHERE username = ?', (username,))
            return cursor.fetchone() is not None
    
    def _log_attempt(self, username: str, success: bool):
        """Log login attempt"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO login_attempts 
                (username, timestamp, success, ip_address) 
                VALUES (?, ?, ?, ?)
            ''', (username, int(time.time()), 1 if success else 0, 'localhost'))
            conn.commit()
    
    def authenticate(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Authenticate user with enhanced security
        Returns: (success, message)
        """
        current_time = int(time.time())
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT password_hash, salt, failed_attempts, locked_until, last_activity
                FROM users WHERE username = ?
            ''', (username,))
            
            result = cursor.fetchone()
            
            if not result:
                self._log_attempt(username, False)
                return False, "Invalid credentials"
            
            password_hash, salt, failed_attempts, locked_until, last_activity = result
            
            # Check if account is locked
            if locked_until > current_time:
                minutes_left = (locked_until - current_time) // 60
                return False, f"Account locked for {minutes_left} more minutes"
            
            # Check if session expired due to inactivity
            if last_activity > 0 and (current_time - last_activity) > self.inactivity_timeout:
                # Clear old session
                cursor.execute('''
                    UPDATE users SET session_token = NULL, last_activity = 0 
                    WHERE username = ?
                ''', (username,))
                conn.commit()
            
            # Verify password
            check_hash, _ = self._hash_password(password, salt)
            
            if check_hash == password_hash:
                # Success - reset failed attempts and update activity
                session_token = secrets.token_urlsafe(32)
                cursor.execute('''
                    UPDATE users 
                    SET failed_attempts = 0, locked_until = 0, 
                        last_login = ?, last_activity = ?, session_token = ?
                    WHERE username = ?
                ''', (current_time, current_time, session_token, username))
                
                # Store session info in Streamlit session state
                st.session_state['session_token'] = session_token
                st.session_state['last_activity'] = current_time
                st.session_state['login_time'] = current_time
                
                conn.commit()
                self._log_attempt(username, True)
                return True, "Authentication successful"
            
            else:
                # Failed - increment attempts
                failed_attempts += 1
                new_locked_until = 0
                
                if failed_attempts >= self.max_attempts:
                    new_locked_until = current_time + self.lockout_duration
                
                cursor.execute('''
                    UPDATE users 
                    SET failed_attempts = ?, locked_until = ?
                    WHERE username = ?
                ''', (failed_attempts, new_locked_until, username))
                
                conn.commit()
                self._log_attempt(username, False)
                
                if new_locked_until > 0:
                    return False, f"Too many failed attempts. Account locked for {self.lockout_duration // 60} minutes."
                else:
                    remaining = self.max_attempts - failed_attempts
                    return False, f"Invalid credentials. {remaining} attempts remaining."
    
    def get_account_status(self, username: str) -> str:
        """Get account status for display"""
        current_time = int(time.time())
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT failed_attempts, locked_until, last_login, last_activity, session_token
                FROM users WHERE username = ?
            ''', (username,))
            
            result = cursor.fetchone()
            
            if not result:
                return "User not found"
            
            failed_attempts, locked_until, last_login, last_activity, session_token = result
            
            if locked_until > current_time:
                minutes_left = (locked_until - current_time) // 60
                return f"🔒 ACCOUNT LOCKED for {minutes_left} more minutes"
            
            # Check inactivity
            if last_activity > 0 and (current_time - last_activity) > self.inactivity_timeout:
                return "🕐 Session expired due to inactivity"
            
            # Check if currently active
            if (session_token and session_token == st.session_state.get('session_token') and
                last_activity > 0 and (current_time - last_activity) < self.inactivity_timeout):
                activity_minutes = (current_time - last_activity) // 60
                return f"✅ Active session (last activity: {activity_minutes} minutes ago)"
            
            if failed_attempts > 0:
                return f"⚠️ {failed_attempts} failed attempts (max: {self.max_attempts})"
            
            if last_login > 0:
                login_time = datetime.fromtimestamp(last_login)
                return f"🔐 Ready for login (last: {login_time.strftime('%Y-%m-%d %H:%M')})"
            
            return "🔐 Ready for login"
    
    def update_activity(self, username: str):
        """Update last activity timestamp"""
        current_time = int(time.time())
        
        # Update in database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET last_activity = ? 
                WHERE username = ?
            ''', (current_time, username))
            conn.commit()
        
        # Update session state
        st.session_state['last_activity'] = current_time
    
    def check_session_timeout(self, username: str) -> bool:
        """
        Check if session has timed out due to inactivity
        Returns True if session is valid, False if timed out
        """
        current_time = int(time.time())
        last_activity = st.session_state.get('last_activity', 0)
        
        if last_activity == 0:
            return False
        
        if (current_time - last_activity) > self.inactivity_timeout:
            # Session timed out - clear session
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users SET session_token = NULL, last_activity = 0 
                    WHERE username = ?
                ''', (username,))
                conn.commit()
            
            # Clear Streamlit session
            for key in ['admin_authenticated', 'session_token', 'last_activity', 'login_time']:
                if key in st.session_state:
                    del st.session_state[key]
            
            return False
        
        # Update activity timestamp
        self.update_activity(username)
        return True
    
    def logout(self, username: str):
        """Logout user and clear session"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET session_token = NULL, last_activity = 0 
                WHERE username = ?
            ''', (username,))
            conn.commit()
        
        # Clear Streamlit session
        for key in ['admin_authenticated', 'session_token', 'last_activity', 'login_time', 'admin_user']:
            if key in st.session_state:
                del st.session_state[key]
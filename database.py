"""
Database setup and connection management
Using SQLite for simplicity and portability
"""
import sqlite3
import os
from datetime import datetime


class Database:
    """Database connection and management"""
    
    def __init__(self, db_path='gearguard.db'):
        self.db_path = db_path
        self.conn = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize database and create tables"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        self._create_tables()
    
    def _create_tables(self):
        """Create all necessary tables"""
        cursor = self.conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                role TEXT DEFAULT 'user',
                is_active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Employees table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                department TEXT,
                is_technician INTEGER DEFAULT 0,
                active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Maintenance Teams table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS maintenance_teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Team Technicians (Many-to-Many)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_technicians (
                team_id INTEGER,
                technician_id INTEGER,
                PRIMARY KEY (team_id, technician_id),
                FOREIGN KEY (team_id) REFERENCES maintenance_teams(id),
                FOREIGN KEY (technician_id) REFERENCES employees(id)
            )
        ''')
        
        # Equipment table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS equipment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                serial_number TEXT,
                department TEXT,
                location TEXT,
                assigned_employee_id INTEGER,
                maintenance_team_id INTEGER,
                purchase_date TEXT,
                warranty_end_date TEXT,
                is_scrapped INTEGER DEFAULT 0,
                active INTEGER DEFAULT 1,
                health_score INTEGER DEFAULT 100,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (assigned_employee_id) REFERENCES employees(id),
                FOREIGN KEY (maintenance_team_id) REFERENCES maintenance_teams(id)
            )
        ''')
        
        # Maintenance Requests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS maintenance_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                equipment_id INTEGER,
                request_type TEXT DEFAULT 'corrective',
                scheduled_date TEXT,
                repaired_date TEXT,
                technician_id INTEGER,
                maintenance_team_id INTEGER,
                duration REAL DEFAULT 0.0,
                description TEXT,
                state TEXT DEFAULT 'new',
                is_overdue INTEGER DEFAULT 0,
                create_date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (equipment_id) REFERENCES equipment(id),
                FOREIGN KEY (technician_id) REFERENCES employees(id),
                FOREIGN KEY (maintenance_team_id) REFERENCES maintenance_teams(id)
            )
        ''')
        
        self.conn.commit()
    
    def get_connection(self):
        """Get database connection"""
        if self.conn is None:
            self._initialize_database()
        return self.conn
    
    def execute(self, query, params=None):
        """Execute a query"""
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.conn.commit()
        return cursor
    
    def fetch_one(self, query, params=None):
        """Fetch one row"""
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def fetch_all(self, query, params=None):
        """Fetch all rows"""
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


# Global database instance
db = Database()


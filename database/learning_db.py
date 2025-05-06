# database/learning_db.py
import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

class LearningDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("stem_learning.db")
        self.create_tables()
        self.load_sample_data()
    
    def create_tables(self):
        """Initialize database schema"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                level INTEGER DEFAULT 1
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS challenges (
                challenge_id TEXT PRIMARY KEY,
                title TEXT,
                description TEXT,
                difficulty TEXT,
                category TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                challenge_id TEXT,
                score REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id),
                FOREIGN KEY(challenge_id) REFERENCES challenges(challenge_id)
            )
        """)
        
        self.conn.commit()
    
    def load_sample_data(self):
        """Insert sample challenges"""
        challenges = [
            ("001", "Hello World", "Print 'Hello World'", "beginner", "python"),
            ("002", "Reverse String", "Reverse a string without built-in functions", "intermediate", "algorithms"),
            ("003", "Robot Movement", "Simulate basic robot kinematics", "advanced", "robotics")
        ]
        
        cursor = self.conn.cursor()
        cursor.executemany(
            "INSERT OR IGNORE INTO challenges VALUES (?, ?, ?, ?, ?)",
            challenges
        )
        self.conn.commit()
    
    def recommend_challenges(self, user_id):
        """Get personalized recommendations"""
        # Get user history
        history = pd.read_sql(
            "SELECT * FROM progress WHERE user_id = ?",
            self.conn,
            params=(user_id,)
        )
        
        if history.empty:
            return self.get_challenges_by_difficulty("beginner")
        
        # Get all challenges
        challenges = pd.read_sql("SELECT * FROM challenges", self.conn)
        
        # Simple recommendation: suggest harder challenges if doing well
        avg_score = history["score"].mean()
        if avg_score > 0.7:
            return self.get_challenges_by_difficulty("advanced")
        elif avg_score > 0.4:
            return self.get_challenges_by_difficulty("intermediate")
        else:
            return self.get_challenges_by_difficulty("beginner")
    
    def get_challenges_by_difficulty(self, difficulty):
        """Get challenges filtered by difficulty"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM challenges WHERE difficulty = ? LIMIT 3",
            (difficulty,)
        )
        return cursor.fetchall()
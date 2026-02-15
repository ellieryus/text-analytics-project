# app/database.py

import sqlite3
import pandas as pd
from datetime import datetime


class ComplaintDatabase:
    # Handle SQLite database operations
    
    def __init__(self, db_path='data/complaints_database.db'):
        self.db_path = db_path
        self.create_table()
    
    def create_table(self):
        # Create complaints table if not exists
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                complaint_text TEXT NOT NULL,
                word_count INTEGER,
                char_count INTEGER,
                caps_words INTEGER,
                exclamations INTEGER,
                questions INTEGER,
                repeated_punct INTEGER,
                urgent_keywords INTEGER,
                emphasis_score REAL,
                sentiment_polarity REAL,
                sentiment_subjectivity REAL,
                sentiment_category TEXT,
                sentiment_aware_score REAL,
                risk_level_original TEXT,
                risk_level_final TEXT,
                product TEXT,
                company TEXT,
                notes TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_complaint(self, analysis_result, metadata=None):
        # Save analyzed complaint to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Extract data
        features = analysis_result['features']
        
        cursor.execute('''
            INSERT INTO complaints (
                timestamp, complaint_text, word_count, char_count,
                caps_words, exclamations, questions, repeated_punct, urgent_keywords,
                emphasis_score, sentiment_polarity, sentiment_subjectivity,
                sentiment_category, sentiment_aware_score,
                risk_level_original, risk_level_final,
                product, company, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            analysis_result['complaint_text'],
            features['word_count'],
            features['char_count'],
            features['caps_words'],
            features['exclamations'],
            features['questions'],
            1 if features['repeated_punct'] else 0,
            features['urgent_keywords'],
            analysis_result['emphasis_score'],
            analysis_result['sentiment_polarity'],
            analysis_result['sentiment_subjectivity'],
            analysis_result['sentiment_category'],
            analysis_result['sentiment_aware_score'],
            analysis_result['risk_level_original'],
            analysis_result['risk_level_final'],
            metadata.get('product', '') if metadata else '',
            metadata.get('company', '') if metadata else '',
            metadata.get('notes', '') if metadata else ''
        ))
        
        conn.commit()
        complaint_id = cursor.lastrowid
        conn.close()
        
        return complaint_id
    
    def get_all_complaints(self):
        # Get all complaints as DataFrame
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM complaints", conn)
        conn.close()
        return df
    
    def get_statistics(self):
        # Get summary statistics
        df = self.get_all_complaints()
        
        if len(df) == 0:
            return None
        
        stats = {
            'total': len(df),
            'high_risk': len(df[df['risk_level_final'] == 'High']),
            'medium_risk': len(df[df['risk_level_final'] == 'Medium']),
            'low_risk': len(df[df['risk_level_final'] == 'Low']),
            'avg_sentiment': df['sentiment_polarity'].mean(),
            'avg_emphasis': df['emphasis_score'].mean()
        }
        
        return stats
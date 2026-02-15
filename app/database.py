# app/database.py

import sqlite3
import pandas as pd
from datetime import datetime
import os


class ComplaintDatabase:
    """Handle SQLite database operations"""
    
    def __init__(self, db_path='data/complaints_database.db'):
        self.db_path = db_path
        
        abs_path = os.path.abspath(self.db_path)
        print(f"Database Initialization:")
        print(f"Relative path: {self.db_path}")
        print(f"Absolute path: {abs_path}")
        print(f"File exists: {os.path.exists(abs_path)}")
        
        # Create directory if doesn't exist
        dir_path = os.path.dirname(abs_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            print(f"Created directory: {dir_path}")
        
        self.create_table()
    
    def create_table(self):
        """Create complaints table if not exists"""
        try:
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
            
            print(f"Table created/verified")
            
        except Exception as e:
            print(f"Error creating table: {e}")
            raise
    
    def save_complaint(self, analysis_result, metadata=None):
        """Save analyzed complaint to database"""
        print(f"\n{'='*60}")
        print(f"SAVING COMPLAINT")
        print(f"{'='*60}")
        
        try:
            # Debug: Show what we're trying to save
            print(f"Risk level original: {analysis_result.get('risk_level_original')}")
            print(f"Risk level final: {analysis_result.get('risk_level_final')}")
            print(f"Sentiment: {analysis_result.get('sentiment_category')}")
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Extract data
            features = analysis_result['features']
            
            # Debug: Show features
            print(f"Features: caps={features['caps_words']}, excl={features['exclamations']}, urgent={features['urgent_keywords']}")
            
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
            
            print(f"Saved, Complaint ID: {complaint_id}")
            print(f"{'='*60}\n")
            
            return complaint_id
            
        except Exception as e:
            print(f"ERROR SAVING: {e}")
            print(f"{'='*60}\n")
            import traceback
            traceback.print_exc()
            return None
    
    def get_all_complaints(self):
        """Get all complaints as DataFrame"""
        try:
            print(f"\nReading from database: {self.db_path}")
            
            if not os.path.exists(self.db_path):
                print(f"Database file doesn't exist yet!")
                return pd.DataFrame()
            
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT * FROM complaints ORDER BY timestamp DESC", conn)
            conn.close()
            
            print(f"Retrieved {len(df)} complaints")
            
            return df
            
        except Exception as e:
            print(f"Error reading database: {e}")
            return pd.DataFrame()
    
    def get_statistics(self):
        """Get summary statistics"""
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
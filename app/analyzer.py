import re
import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 

class ComplaintAnalyzer:
    # Analyze complaint and return risk assessment
    
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        self.urgent_keywords = [
            'fraud', 'stolen', 'unauthorized', 'scam', 'theft',
            'emergency', 'immediately', 'urgent', 'critical',
            'lawyer', 'attorney', 'sue', 'lawsuit', 'legal action',
            'harassment', 'threatening', 'illegal', 'criminal'
        ]
    
    def count_caps_words(self, text):
        # Count ALL-CAPS words
        if not text:
            return 0
        caps_pattern = r'\b[A-Z]{2,}\b'
        return len(re.findall(caps_pattern, text))
    
    def count_exclamations(self, text):
        # Count exclamation marks
        return text.count('!') if text else 0
    
    def count_questions(self, text):
        # Count question marks
        return text.count('?') if text else 0
    
    def has_repeated_punctuation(self, text):
        # Check for repeated punctuation
        if not text:
            return False
        pattern = r'([!?.])\1+'
        return bool(re.search(pattern, text))
    
    def count_urgent_keywords(self, text):
        # Count urgent keywords
        if not text:
            return 0
        text_lower = text.lower()
        return sum(1 for word in self.urgent_keywords if word in text_lower)
    
    def calculate_emphasis_score(self, features):
        # Calculate emphasis score
        caps_score = min(features['caps_words'] / 10, 1.0)
        exclaim_score = min(features['exclamations'] / 5, 1.0)
        question_score = min(features['questions'] / 5, 1.0)
        repeat_score = 1.0 if features['repeated_punct'] else 0.0
        urgent_score = min(features['urgent_keywords'] / 3, 1.0)
        
        emphasis_score = (
            0.25 * caps_score +
            0.20 * exclaim_score +
            0.10 * question_score +
            0.15 * repeat_score +
            0.30 * urgent_score
        )
        
        return round(emphasis_score, 3)
    
    # def get_sentiment(self, text):
    #     # Get sentiment using TextBlob
    #     if not text:
    #         return 0.0, 0.0
        
    #     blob = TextBlob(text)
    #     return blob.sentiment.polarity, blob.sentiment.subjectivity
    
    def get_sentiment(self, text):
        """Hybrid sentiment analysis - VADER primary, TextBlob fallback"""
        if not text:
            return 0.0, 0.0
        
        # Try VADER first (better for complaints)
        try:
            vader_scores = self.vader.polarity_scores(text)
            vader_compound = vader_scores['compound']
            
            # VADER confidence threshold: use if score is meaningful (|score| > 0.05)
            # VADER range: -1 to +1, where -0.05 to +0.05 is neutral
            if abs(vader_compound) > 0.05:
                # Estimate subjectivity from VADER score extremity
                # More extreme = more subjective/opinionated
                subjectivity = min(abs(vader_compound) + 0.3, 1.0)
                return vader_compound, subjectivity
        except Exception as e:
            # VADER not available or error - silently fall back
            print(f"⚠️ VADER failed: {e}, using TextBlob")
            pass
        
        # Fallback to TextBlob
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity, blob.sentiment.subjectivity
        except Exception as e:
            # Both failed - return neutral
            print(f"⚠️ TextBlob also failed: {e}, returning neutral")
            return 0.0, 0.5  # Neutral with moderate subjectivity

    def classify_sentiment(self, polarity):
        """Classify sentiment from polarity score"""
        # Use VADER thresholds (more sensitive than TextBlob)
        if polarity > 0.05:  # VADER positive threshold
            return 'Positive'
        elif polarity < -0.05:  # VADER negative threshold
            return 'Negative'
        else:
            return 'Neutral'
    
    def calculate_sentiment_aware_score(self, emphasis_score, sentiment):
        # Adjust emphasis by sentiment
        if sentiment > 0.3:
            multiplier = 0.3
        elif sentiment > 0:
            multiplier = 0.7
        else:
            multiplier = 1.0
        
        return round(emphasis_score * multiplier, 3)
    
    def classify_risk(self, score):
        # Classify risk level
        if score >= 0.6:
            return 'High'
        elif score >= 0.3:
            return 'Medium'
        else:
            return 'Low'
    
    def analyze(self, complaint_text):
        # Complete analysis of complaint
        
        # Returns dict with all analysis results
        # Extract features
        features = {
            'caps_words': self.count_caps_words(complaint_text),
            'exclamations': self.count_exclamations(complaint_text),
            'questions': self.count_questions(complaint_text),
            'repeated_punct': self.has_repeated_punctuation(complaint_text),
            'urgent_keywords': self.count_urgent_keywords(complaint_text),
            'word_count': len(complaint_text.split()) if complaint_text else 0,
            'char_count': len(complaint_text) if complaint_text else 0
        }
        
        # Calculate scores
        emphasis_score = self.calculate_emphasis_score(features)
        sentiment_polarity, sentiment_subjectivity = self.get_sentiment(complaint_text)
        sentiment_category = self.classify_sentiment(sentiment_polarity)
        sentiment_aware_score = self.calculate_sentiment_aware_score(
            emphasis_score, sentiment_polarity
        )
        
        # Classify
        risk_level_original = self.classify_risk(emphasis_score)
        risk_level_final = self.classify_risk(sentiment_aware_score)
        
        return {
            'complaint_text': complaint_text,
            'features': features,
            'emphasis_score': emphasis_score,
            'sentiment_polarity': sentiment_polarity,
            'sentiment_subjectivity': sentiment_subjectivity,
            'sentiment_category': sentiment_category,
            'sentiment_aware_score': sentiment_aware_score,
            'risk_level_original': risk_level_original,
            'risk_level_final': risk_level_final,
        }
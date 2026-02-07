"""
Signal Analysis Module
Detects urgency, emphasis, and escalation patterns in text
"""

import pandas as pd
import numpy as np
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmphasisDetector:
    """Detect emphasis and urgency signals in text"""
    
    def __init__(self, config=None):
        """
        Initialize emphasis detector
        
        Parameters:
        -----------
        config : dict, optional
            Configuration dictionary
        """
        self.config = config or {}
        
    def count_caps_words(self, text):
        """
        Count words in ALL CAPS (excluding single letters)
        
        Parameters:
        -----------
        text : str
            Input text
            
        Returns:
        --------
        int : number of ALL CAPS words
        """
        if pd.isna(text):
            return 0
        
        # Find words that are all uppercase and longer than 1 character
        caps_pattern = r'\b[A-Z]{2,}\b'
        caps_words = re.findall(caps_pattern, text)
        
        return len(caps_words)
    
    def count_exclamations(self, text):
        """
        Count exclamation marks
        
        Parameters:
        -----------
        text : str
            Input text
            
        Returns:
        --------
        int : number of exclamation marks
        """
        if pd.isna(text):
            return 0
        
        return text.count('!')
    
    def count_questions(self, text):
        """
        Count question marks
        
        Parameters:
        -----------
        text : str
            Input text
            
        Returns:
        --------
        int : number of question marks
        """
        if pd.isna(text):
            return 0
        
        return text.count('?')
    
    def has_repeated_punctuation(self, text):
        """
        Check for repeated punctuation (!!!, ???, etc.)
        
        Parameters:
        -----------
        text : str
            Input text
            
        Returns:
        --------
        bool : True if repeated punctuation found
        """
        if pd.isna(text):
            return False
        
        # Pattern for 2+ repeated punctuation
        pattern = r'([!?.])\1+'
        return bool(re.search(pattern, text))
    
    def count_urgent_words(self, text, urgent_words=None):
        """
        Count urgent/escalation keywords
        
        Parameters:
        -----------
        text : str
            Input text
        urgent_words : list, optional
            List of urgent keywords
            
        Returns:
        --------
        int : count of urgent words
        """
        if pd.isna(text):
            return 0
        
        if urgent_words is None:
            urgent_words = [
                'urgent', 'immediately', 'asap', 'emergency', 'critical',
                'fraud', 'stolen', 'unauthorized', 'lawyer', 'attorney',
                'sue', 'lawsuit', 'legal action', 'complaint', 'scam'
            ]
        
        text_lower = text.lower()
        count = sum(1 for word in urgent_words if word in text_lower)
        
        return count
    
    def calculate_emphasis_score(self, text):
        """
        Calculate overall emphasis score
        
        Parameters:
        -----------
        text : str
            Input text
            
        Returns:
        --------
        float : emphasis score (0-1 normalized)
        """
        if pd.isna(text):
            return 0.0
        
        # Component scores
        caps_score = min(self.count_caps_words(text) / 10, 1.0)  # normalize to max 10
        exclaim_score = min(self.count_exclamations(text) / 5, 1.0)  # normalize to max 5
        urgent_score = min(self.count_urgent_words(text) / 3, 1.0)  # normalize to max 3
        repeat_score = 1.0 if self.has_repeated_punctuation(text) else 0.0
        
        # Weighted combination
        emphasis_score = (
            0.3 * caps_score +
            0.25 * exclaim_score +
            0.3 * urgent_score +
            0.15 * repeat_score
        )
        
        return emphasis_score
    
    def extract_all_features(self, text):
        """
        Extract all emphasis features
        
        Parameters:
        -----------
        text : str
            Input text
            
        Returns:
        --------
        dict : all emphasis features
        """
        features = {
            'caps_words': self.count_caps_words(text),
            'exclamations': self.count_exclamations(text),
            'questions': self.count_questions(text),
            'repeated_punct': self.has_repeated_punctuation(text),
            'urgent_words': self.count_urgent_words(text),
            'emphasis_score': self.calculate_emphasis_score(text)
        }
        
        return features


class RiskClassifier:
    """Classify complaints by risk level"""
    
    def __init__(self, thresholds=None):
        """
        Initialize risk classifier
        
        Parameters:
        -----------
        thresholds : dict, optional
            Threshold values for risk levels
        """
        self.thresholds = thresholds or {
            'high': 0.6,
            'medium': 0.3,
            'low': 0.0
        }
    
    def classify_risk(self, emphasis_score):
        """
        Classify risk level based on emphasis score
        
        Parameters:
        -----------
        emphasis_score : float
            Emphasis score (0-1)
            
        Returns:
        --------
        str : risk level ('high', 'medium', 'low')
        """
        if emphasis_score >= self.thresholds['high']:
            return 'high'
        elif emphasis_score >= self.thresholds['medium']:
            return 'medium'
        else:
            return 'low'
    
    def flag_high_risk(self, df, score_column='emphasis_score'):
        """
        Flag high-risk complaints
        
        Parameters:
        -----------
        df : pandas.DataFrame
            Dataframe with emphasis scores
        score_column : str
            Name of score column
            
        Returns:
        --------
        pandas.DataFrame : dataframe with risk labels
        """
        df['risk_level'] = df[score_column].apply(self.classify_risk)
        df['is_high_risk'] = df['risk_level'] == 'high'
        
        logger.info(f"Flagged {df['is_high_risk'].sum()} high-risk complaints")
        
        return df


def extract_emphasis_features_batch(texts):
    """
    Extract emphasis features for multiple texts
    
    Parameters:
    -----------
    texts : pandas.Series or list
        Collection of texts
        
    Returns:
    --------
    pandas.DataFrame : features for all texts
    """
    detector = EmphasisDetector()
    
    features_list = []
    for text in texts:
        features = detector.extract_all_features(text)
        features_list.append(features)
    
    df_features = pd.DataFrame(features_list)
    
    return df_features

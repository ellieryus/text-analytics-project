"""
Content Analysis Module
Handles keyword extraction, TF-IDF analysis, and phrase extraction
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KeywordExtractor:
    """Extract keywords and phrases using TF-IDF"""
    
    def __init__(self, config=None):
        """
        Initialize keyword extractor
        
        Parameters:
        -----------
        config : dict, optional
            Configuration dictionary
        """
        self.config = config or {}
        self.vectorizer = None
        self.feature_names = None
        
    def fit_tfidf(self, texts, ngram_range=(1, 3), max_features=1000, 
                  min_df=5, max_df=0.8, stop_words='english'):
        """
        Fit TF-IDF vectorizer on texts
        
        Parameters:
        -----------
        texts : list or pandas.Series
            Collection of text documents
        ngram_range : tuple
            Range of n-grams to extract
        max_features : int
            Maximum number of features
        min_df : int or float
            Minimum document frequency
        max_df : float
            Maximum document frequency
        stop_words : str or list
            Stop words to remove
            
        Returns:
        --------
        scipy.sparse matrix : TF-IDF matrix
        """
        logger.info("Fitting TF-IDF vectorizer...")
        
        self.vectorizer = TfidfVectorizer(
            ngram_range=ngram_range,
            max_features=max_features,
            min_df=min_df,
            max_df=max_df,
            stop_words=stop_words,
            lowercase=True
        )
        
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        self.feature_names = self.vectorizer.get_feature_names_out()
        
        logger.info(f"Extracted {len(self.feature_names)} features")
        return tfidf_matrix
    
    def get_top_keywords(self, tfidf_matrix, n=20):
        """
        Get top keywords across entire corpus
        
        Parameters:
        -----------
        tfidf_matrix : scipy.sparse matrix
            TF-IDF matrix
        n : int
            Number of top keywords to return
            
        Returns:
        --------
        pandas.DataFrame : top keywords with scores
        """
        # Calculate mean TF-IDF score for each term
        mean_tfidf = np.asarray(tfidf_matrix.mean(axis=0)).flatten()
        
        # Create dataframe of terms and scores
        df_keywords = pd.DataFrame({
            'keyword': self.feature_names,
            'tfidf_score': mean_tfidf
        })
        
        # Sort by score
        df_keywords = df_keywords.sort_values('tfidf_score', ascending=False)
        
        return df_keywords.head(n)
    
    def get_document_keywords(self, tfidf_matrix, doc_idx, n=10):
        """
        Get top keywords for a specific document
        
        Parameters:
        -----------
        tfidf_matrix : scipy.sparse matrix
        doc_idx : int
            Document index
        n : int
            Number of keywords
            
        Returns:
        --------
        list : top keywords for document
        """
        # Get TF-IDF scores for document
        doc_scores = tfidf_matrix[doc_idx].toarray().flatten()
        
        # Get top n indices
        top_indices = doc_scores.argsort()[-n:][::-1]
        
        # Get corresponding keywords
        top_keywords = [(self.feature_names[i], doc_scores[i]) 
                       for i in top_indices if doc_scores[i] > 0]
        
        return top_keywords


class PhraseExtractor:
    """Extract meaningful phrases and collocations"""
    
    def __init__(self):
        """Initialize phrase extractor"""
        pass
    
    def extract_bigrams(self, texts, min_freq=5):
        """
        Extract common bigrams (2-word phrases)
        
        Parameters:
        -----------
        texts : list
            List of text documents
        min_freq : int
            Minimum frequency threshold
            
        Returns:
        --------
        list : common bigrams
        """
        from nltk import bigrams
        from collections import Counter
        
        all_bigrams = []
        
        for text in texts:
            tokens = word_tokenize(text.lower())
            all_bigrams.extend(list(bigrams(tokens)))
        
        bigram_freq = Counter(all_bigrams)
        common_bigrams = [(bg, freq) for bg, freq in bigram_freq.most_common() 
                         if freq >= min_freq]
        
        return common_bigrams
    
    def extract_trigrams(self, texts, min_freq=5):
        """
        Extract common trigrams (3-word phrases)
        
        Parameters:
        -----------
        texts : list
            List of text documents
        min_freq : int
            Minimum frequency threshold
            
        Returns:
        --------
        list : common trigrams
        """
        from nltk import trigrams
        from collections import Counter
        
        all_trigrams = []
        
        for text in texts:
            tokens = word_tokenize(text.lower())
            all_trigrams.extend(list(trigrams(tokens)))
        
        trigram_freq = Counter(all_trigrams)
        common_trigrams = [(tg, freq) for tg, freq in trigram_freq.most_common() 
                          if freq >= min_freq]
        
        return common_trigrams


def tokenize_text(text, remove_stopwords=True):
    """
    Tokenize text with optional stopword removal
    
    Parameters:
    -----------
    text : str
        Input text
    remove_stopwords : bool
        Whether to remove stopwords
        
    Returns:
    --------
    list : tokens
    """
    # Tokenize
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords if requested
    if remove_stopwords:
        stop_words = set(stopwords.words('english'))
        tokens = [t for t in tokens if t not in stop_words and t.isalnum()]
    
    return tokens

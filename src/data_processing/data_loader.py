"""
Data Processing Module
Handles data loading, cleaning, and initial preprocessing
"""

import pandas as pd
import numpy as np
import yaml
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Load and perform initial data validation"""
    
    def __init__(self, config_path='config.yaml'):
        """Initialize with configuration file"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
    def load_raw_data(self, filepath=None):
        """
        Load raw complaint data from CSV
        
        Parameters:
        -----------
        filepath : str, optional
            Path to CSV file. If None, uses path from config
            
        Returns:
        --------
        pandas.DataFrame
        """
        if filepath is None:
            filepath = self.config['data']['raw_data_path']
        
        logger.info(f"Loading data from {filepath}")
        
        try:
            df = pd.read_csv(filepath, low_memory=False)
            logger.info(f"Successfully loaded {len(df)} records")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def validate_data(self, df):
        """
        Perform basic data validation
        
        Parameters:
        -----------
        df : pandas.DataFrame
            Input dataframe
            
        Returns:
        --------
        dict : validation results
        """
        validation = {
            'total_records': len(df),
            'columns': list(df.columns),
            'missing_values': df.isnull().sum().to_dict(),
            'data_types': df.dtypes.to_dict()
        }
        
        logger.info("Data validation complete")
        return validation
    
    def get_text_column(self, df, text_col='Consumer complaint narrative'):
        """
        Extract and validate text column
        
        Parameters:
        -----------
        df : pandas.DataFrame
        text_col : str
            Name of text column
            
        Returns:
        --------
        pandas.Series
        """
        if text_col not in df.columns:
            raise ValueError(f"Column '{text_col}' not found in dataframe")
        
        # Remove null values
        text_data = df[text_col].dropna()
        logger.info(f"Extracted {len(text_data)} non-null text records")
        
        return text_data


class DataCleaner:
    """Clean and preprocess text data"""
    
    def __init__(self, config_path='config.yaml'):
        """Initialize with configuration"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
    
    def light_clean(self, text):
        """
        Perform light cleaning while preserving emphasis signals
        
        Parameters:
        -----------
        text : str
            Input text
            
        Returns:
        --------
        str : cleaned text
        """
        if pd.isna(text):
            return ""
        
        # Convert to string
        text = str(text)
        
        # Remove excessive whitespace but keep single spaces
        text = ' '.join(text.split())
        
        return text
    
    def remove_masked_data(self, text):
        """
        Remove masked/redacted data patterns (XX, XXXX, etc.)
        
        Parameters:
        -----------
        text : str
            Input text
            
        Returns:
        --------
        str : text with masked data removed
        """
        import re
        
        # Remove patterns like XX, XXXX, {XX}
        text = re.sub(r'\b[X]{2,}\b', '', text)
        text = re.sub(r'\{[X]{2,}\}', '', text)
        
        return text


def save_processed_data(df, filename, output_dir='data/processed/'):
    """
    Save processed dataframe
    
    Parameters:
    -----------
    df : pandas.DataFrame
    filename : str
    output_dir : str
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filepath = Path(output_dir) / filename
    
    df.to_csv(filepath, index=False)
    logger.info(f"Saved processed data to {filepath}")

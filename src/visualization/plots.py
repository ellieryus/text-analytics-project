"""
Visualization Module
Functions for creating plots and visualizations
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from wordcloud import WordCloud
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def plot_keyword_frequency(keywords_df, n=20, title="Top Keywords by TF-IDF Score", 
                          save_path=None):
    """
    Plot top keywords as horizontal bar chart
    
    Parameters:
    -----------
    keywords_df : pandas.DataFrame
        DataFrame with 'keyword' and 'tfidf_score' columns
    n : int
        Number of top keywords to plot
    title : str
        Plot title
    save_path : str, optional
        Path to save figure
    """
    plt.figure(figsize=(10, 8))
    
    # Get top n keywords
    top_keywords = keywords_df.head(n)
    
    # Create horizontal bar plot
    plt.barh(range(len(top_keywords)), top_keywords['tfidf_score'])
    plt.yticks(range(len(top_keywords)), top_keywords['keyword'])
    plt.xlabel('TF-IDF Score')
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved figure to {save_path}")
    
    plt.show()


def create_wordcloud(text_or_freq, title="Word Cloud", save_path=None):
    """
    Create word cloud visualization
    
    Parameters:
    -----------
    text_or_freq : str or dict
        Either concatenated text or frequency dictionary
    title : str
        Plot title
    save_path : str, optional
        Path to save figure
    """
    plt.figure(figsize=(14, 8))
    
    # Create word cloud
    wordcloud = WordCloud(
        width=1200, 
        height=600,
        background_color='white',
        colormap='viridis',
        max_words=100
    ).generate(text_or_freq) if isinstance(text_or_freq, str) else \
      WordCloud(
        width=1200, 
        height=600,
        background_color='white',
        colormap='viridis'
    ).generate_from_frequencies(text_or_freq)
    
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=16, pad=20)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved figure to {save_path}")
    
    plt.show()


def plot_emphasis_distribution(df, score_column='emphasis_score', 
                               title="Distribution of Emphasis Scores", 
                               save_path=None):
    """
    Plot distribution of emphasis scores
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with emphasis scores
    score_column : str
        Name of score column
    title : str
        Plot title
    save_path : str, optional
        Path to save figure
    """
    plt.figure(figsize=(12, 6))
    
    # Histogram
    plt.subplot(1, 2, 1)
    plt.hist(df[score_column], bins=50, edgecolor='black', alpha=0.7)
    plt.xlabel('Emphasis Score')
    plt.ylabel('Frequency')
    plt.title('Histogram of Emphasis Scores')
    
    # Box plot
    plt.subplot(1, 2, 2)
    plt.boxplot(df[score_column], vert=True)
    plt.ylabel('Emphasis Score')
    plt.title('Box Plot of Emphasis Scores')
    
    plt.suptitle(title, fontsize=14, y=1.02)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved figure to {save_path}")
    
    plt.show()


def plot_risk_categories(df, risk_column='risk_level', 
                        title="Complaint Risk Level Distribution", 
                        save_path=None):
    """
    Plot distribution of risk categories
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with risk levels
    risk_column : str
        Name of risk column
    title : str
        Plot title
    save_path : str, optional
        Path to save figure
    """
    plt.figure(figsize=(10, 6))
    
    # Count risk levels
    risk_counts = df[risk_column].value_counts()
    
    # Create bar plot
    colors = {'high': '#d62728', 'medium': '#ff7f0e', 'low': '#2ca02c'}
    risk_colors = [colors.get(level, 'gray') for level in risk_counts.index]
    
    plt.bar(risk_counts.index, risk_counts.values, color=risk_colors, alpha=0.8)
    plt.xlabel('Risk Level')
    plt.ylabel('Number of Complaints')
    plt.title(title)
    
    # Add value labels on bars
    for i, (level, count) in enumerate(risk_counts.items()):
        plt.text(i, count, str(count), ha='center', va='bottom')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved figure to {save_path}")
    
    plt.show()


def plot_feature_correlation(df, features, title="Feature Correlation Matrix", 
                            save_path=None):
    """
    Plot correlation matrix of features
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with features
    features : list
        List of feature column names
    title : str
        Plot title
    save_path : str, optional
        Path to save figure
    """
    plt.figure(figsize=(10, 8))
    
    # Calculate correlation matrix
    corr_matrix = df[features].corr()
    
    # Create heatmap
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title(title)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved figure to {save_path}")
    
    plt.show()


def plot_ngram_frequency(ngram_list, n=20, title="Top N-grams", save_path=None):
    """
    Plot top n-grams
    
    Parameters:
    -----------
    ngram_list : list of tuples
        List of (ngram, frequency) tuples
    n : int
        Number of top n-grams to plot
    title : str
        Plot title
    save_path : str, optional
        Path to save figure
    """
    plt.figure(figsize=(12, 8))
    
    # Get top n
    top_ngrams = ngram_list[:n]
    
    # Extract labels and values
    labels = [' '.join(ng[0]) if isinstance(ng[0], tuple) else ng[0] 
              for ng in top_ngrams]
    values = [ng[1] for ng in top_ngrams]
    
    # Create horizontal bar plot
    plt.barh(range(len(labels)), values, color='steelblue')
    plt.yticks(range(len(labels)), labels)
    plt.xlabel('Frequency')
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved figure to {save_path}")
    
    plt.show()


def save_figure(fig, filename, output_dir='outputs/figures/'):
    """
    Save matplotlib figure
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        Figure to save
    filename : str
        Output filename
    output_dir : str
        Output directory
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filepath = Path(output_dir) / filename
    
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"Saved figure to {filepath}")

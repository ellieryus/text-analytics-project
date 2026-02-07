# Quick Start Guide
## Consumer Complaint Text Analytics Project

---

## Setup Instructions

### 1. Environment Setup

```bash
# Navigate to project directory
cd text_analytics_project

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Download NLTK Data

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
```

### 3. Prepare Your Data

Place your consumer complaints CSV file in:
```
data/raw/consumer_complaints.csv
```

Update the file path in `config.yaml` if using a different filename.

---

## Running the Analysis

### Step-by-Step Workflow

**Notebook 1: Data Exploration** (`01_data_exploration.ipynb`)
- Load and inspect raw data
- Check data quality
- Understand text characteristics
- Explore structured fields

**Notebook 2: Data Preprocessing** (`02_data_preprocessing.ipynb`)
- Clean complaint narratives
- Handle missing values
- Remove masked data patterns
- Create processed dataset

**Notebook 3: Content Analysis** (`03_content_analysis.ipynb`)
- Extract keywords using TF-IDF
- Identify key phrases
- Analyze n-grams (bigrams, trigrams)
- Generate word clouds

**Notebook 4: Signal Analysis** (`04_signal_analysis.ipynb`)
- Detect emphasis patterns
- Calculate urgency scores
- Flag high-risk complaints
- Analyze feature correlations

**Notebook 5: Final Analysis** (`05_final_analysis.ipynb`)
- Combine content and signal insights
- Generate final reports
- Create visualizations
- Summarize findings

---

## Using the Python Modules

### Data Loading

```python
from src.data_processing import DataLoader

# Initialize loader
loader = DataLoader(config_path='config.yaml')

# Load data
df = loader.load_raw_data()

# Get text column
complaints = loader.get_text_column(df)
```

### Content Analysis

```python
from src.content_analysis.keyword_extraction import KeywordExtractor

# Initialize extractor
extractor = KeywordExtractor()

# Fit TF-IDF
tfidf_matrix = extractor.fit_tfidf(complaints)

# Get top keywords
top_keywords = extractor.get_top_keywords(tfidf_matrix, n=20)
```

### Signal Analysis

```python
from src.signal_analysis.emphasis_detection import EmphasisDetector

# Initialize detector
detector = EmphasisDetector()

# Extract features for a single text
features = detector.extract_all_features(complaint_text)

# Calculate emphasis score
score = detector.calculate_emphasis_score(complaint_text)
```

### Visualization

```python
from src.visualization.plots import plot_keyword_frequency

# Plot top keywords
plot_keyword_frequency(
    top_keywords, 
    n=20, 
    save_path='outputs/figures/top_keywords.png'
)
```

---

## Configuration

Edit `config.yaml` to customize:

- **Data paths:** Where to find raw/processed data
- **TF-IDF parameters:** max_features, min_df, max_df
- **Signal thresholds:** For risk classification
- **Output settings:** Figure format, DPI

Example:
```yaml
tfidf:
  max_features: 1000
  min_df: 5
  max_df: 0.8

signal_analysis:
  caps_threshold: 3
  exclamation_threshold: 2
```

---

## Common Tasks

### Generate Top Keywords Report

```python
from src.content_analysis.keyword_extraction import KeywordExtractor
from src.visualization.plots import plot_keyword_frequency

extractor = KeywordExtractor()
tfidf_matrix = extractor.fit_tfidf(complaints)
keywords_df = extractor.get_top_keywords(tfidf_matrix, n=50)

# Save to CSV
keywords_df.to_csv('outputs/tables/top_keywords.csv', index=False)

# Create visualization
plot_keyword_frequency(keywords_df, n=20, 
                      save_path='outputs/figures/keywords.png')
```

### Identify High-Risk Complaints

```python
from src.signal_analysis.emphasis_detection import (
    extract_emphasis_features_batch, 
    RiskClassifier
)

# Extract features
features_df = extract_emphasis_features_batch(complaints)

# Classify risk
classifier = RiskClassifier()
features_df = classifier.flag_high_risk(features_df)

# Get high-risk complaints
high_risk = df[features_df['is_high_risk']]

# Save results
high_risk.to_csv('outputs/tables/high_risk_complaints.csv', index=False)
```

### Create Word Cloud

```python
from src.visualization.plots import create_wordcloud

# Combine all complaint text
all_text = ' '.join(complaints.astype(str))

# Generate word cloud
create_wordcloud(
    all_text, 
    title='Consumer Complaint Word Cloud',
    save_path='outputs/figures/wordcloud.png'
)
```

---

## Troubleshooting

### Issue: Module not found
```bash
# Make sure src is in Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/text_analytics_project"
```

Or in notebook:
```python
import sys
sys.path.append('../src')
```

### Issue: NLTK data not found
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### Issue: File path errors
- Use relative paths from project root
- Check config.yaml for correct paths
- Ensure data files are in correct directories

### Issue: Memory errors with large datasets
- Process data in chunks
- Reduce max_features in TF-IDF
- Use sparse matrices where possible

---

## Output Files

After running the analysis, you should have:

**Figures** (`outputs/figures/`)
- Top keyword bar charts
- Word clouds
- Emphasis score distributions
- Risk category plots
- Feature correlation heatmaps

**Tables** (`outputs/tables/`)
- Top keywords CSV
- High-risk complaints CSV
- Summary statistics
- N-gram frequencies

**Reports** (`outputs/reports/`)
- Final analysis report
- Presentation slides

---

## Tips for Success

1. **Start with small samples** to test your code before processing all data
2. **Document your findings** in notebooks as you go
3. **Save intermediate results** to avoid re-running expensive computations
4. **Use version control** to track changes
5. **Collaborate effectively** by dividing tasks among team members

---

## Next Steps After Setup

1. Run `01_data_exploration.ipynb` to understand your data
2. Review the config.yaml and adjust parameters as needed
3. Proceed through notebooks 02-05 sequentially
4. Generate final visualizations and reports
5. Prepare presentation materials

---

## Getting Help

- Review the `docs/PROJECT_DOCUMENTATION.md` for detailed information
- Check function docstrings for parameter details
- Consult the README.md for project overview
- Ask team members for clarification

---

## Contact

For questions or issues, contact team members:
- Yanxin Li (261010919)
- Yasmine Zhao (261268871)
- Ellie Ha (261266871)
- Maral Vahedi (261231293)

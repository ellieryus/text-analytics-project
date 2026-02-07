# Text Analytics Project Structure
## Complete Directory Layout

```
text_analytics_project/
│
├── 📄 README.md                          # Project overview and introduction
├── 📄 requirements.txt                   # Python package dependencies
├── 📄 config.yaml                        # Configuration parameters
├── 📄 .gitignore                         # Git ignore rules
│
├── 📂 data/                              # All data files (gitignored)
│   ├── 📂 raw/                           # Original, immutable data
│   │   └── .gitkeep                      # (Place your consumer_complaints.csv here)
│   ├── 📂 interim/                       # Intermediate transformed data
│   │   └── .gitkeep
│   └── 📂 processed/                     # Final, analysis-ready data
│       └── .gitkeep
│
├── 📂 notebooks/                         # Jupyter notebooks for analysis
│   ├── 01_data_exploration.ipynb         # ✅ Initial data exploration
│   ├── 02_data_preprocessing.ipynb       # ⏳ Data cleaning (to be created)
│   ├── 03_content_analysis.ipynb         # ⏳ Keyword extraction (to be created)
│   ├── 04_signal_analysis.ipynb          # ⏳ Emphasis detection (to be created)
│   └── 05_final_analysis.ipynb           # ⏳ Final report (to be created)
│
├── 📂 src/                               # Source code modules
│   ├── __init__.py                       # Package initializer
│   │
│   ├── 📂 data_processing/               # Data loading and cleaning
│   │   ├── __init__.py
│   │   └── data_loader.py                # ✅ DataLoader, DataCleaner classes
│   │
│   ├── 📂 content_analysis/              # Keyword extraction and TF-IDF
│   │   ├── __init__.py
│   │   └── keyword_extraction.py         # ✅ KeywordExtractor, PhraseExtractor
│   │
│   ├── 📂 signal_analysis/               # Urgency and emphasis detection
│   │   ├── __init__.py
│   │   └── emphasis_detection.py         # ✅ EmphasisDetector, RiskClassifier
│   │
│   └── 📂 visualization/                 # Plotting and reporting
│       ├── __init__.py
│       └── plots.py                      # ✅ Visualization functions
│
├── 📂 models/                            # Trained models and vectorizers
│   └── .gitkeep                          # (Will store fitted TF-IDF models)
│
├── 📂 outputs/                           # Generated outputs
│   ├── 📂 figures/                       # Plots and visualizations
│   │   └── .gitkeep
│   ├── 📂 tables/                        # CSV exports and summary tables
│   │   └── .gitkeep
│   └── 📂 reports/                       # Final reports and presentations
│       └── .gitkeep
│
├── 📂 docs/                              # Documentation
│   ├── PROJECT_DOCUMENTATION.md          # ✅ Detailed project documentation
│   └── QUICK_START.md                    # ✅ Setup and usage guide
│
└── 📂 references/                        # Reference materials
    └── (Data dictionaries, papers, manuals)

```

## Key Components

### 📊 Data Flow
```
Raw Data (CSV) 
    ↓
Data Loading (data_loader.py)
    ↓
Data Cleaning (light_clean, remove_masked_data)
    ↓
    ├─→ Content Analysis (keyword_extraction.py)
    │       ├── Tokenization
    │       ├── TF-IDF Vectorization
    │       ├── Keyword Extraction
    │       └── N-gram Analysis
    │
    └─→ Signal Analysis (emphasis_detection.py)
            ├── Emphasis Detection (CAPS, punctuation)
            ├── Urgency Scoring
            └── Risk Classification
    ↓
Visualization & Reporting (plots.py)
    ↓
Outputs (figures, tables, reports)
```

### 🔧 Core Modules

**1. Data Processing** (`src/data_processing/`)
- `DataLoader`: Load and validate CSV data
- `DataCleaner`: Clean text while preserving signals
- Functions for saving processed data

**2. Content Analysis** (`src/content_analysis/`)
- `KeywordExtractor`: TF-IDF based keyword extraction
- `PhraseExtractor`: Bigram and trigram extraction
- Tokenization utilities

**3. Signal Analysis** (`src/signal_analysis/`)
- `EmphasisDetector`: Detect urgency patterns
  - ALL-CAPS words
  - Exclamation marks
  - Repeated punctuation
  - Urgent keywords
- `RiskClassifier`: Classify complaints by risk level

**4. Visualization** (`src/visualization/`)
- Keyword frequency plots
- Word clouds
- Emphasis distribution plots
- Risk category charts
- Correlation heatmaps

### 📓 Notebook Workflow

1. **01_data_exploration.ipynb** ✅
   - Load data
   - Inspect structure
   - Analyze text characteristics
   - Explore distributions

2. **02_data_preprocessing.ipynb** (To be created)
   - Clean narratives
   - Handle missing values
   - Create processed dataset

3. **03_content_analysis.ipynb** (To be created)
   - Extract keywords
   - Generate word clouds
   - Analyze n-grams

4. **04_signal_analysis.ipynb** (To be created)
   - Calculate emphasis scores
   - Flag high-risk complaints
   - Visualize patterns

5. **05_final_analysis.ipynb** (To be created)
   - Combine insights
   - Generate final report
   - Create presentation materials

### ⚙️ Configuration

**config.yaml** contains:
- Data file paths
- TF-IDF parameters (max_features, min_df, max_df)
- Signal detection thresholds
- Output settings

### 📦 Dependencies

**Core Libraries:**
- pandas, numpy (data manipulation)
- scikit-learn (TF-IDF, vectorization)
- nltk (tokenization, stopwords)
- matplotlib, seaborn (visualization)
- wordcloud (word cloud generation)

### 🎯 Expected Outputs

After running the analysis:

**outputs/figures/**
- `top_keywords.png` - Bar chart of top keywords
- `wordcloud.png` - Visual word cloud
- `emphasis_distribution.png` - Score distribution
- `risk_categories.png` - Risk level breakdown
- `feature_correlation.png` - Feature heatmap

**outputs/tables/**
- `top_keywords.csv` - Keyword rankings
- `high_risk_complaints.csv` - Flagged complaints
- `summary_statistics.csv` - Descriptive stats
- `ngram_frequencies.csv` - Common phrases

**outputs/reports/**
- Final analysis report (PDF/Word)
- Presentation slides (PPTX)

## Getting Started

1. **Place your data:** Copy CSV to `data/raw/`
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Download NLTK data:** Run setup code in notebook
4. **Run notebooks:** Execute 01-05 in sequence
5. **Review outputs:** Check `outputs/` directory

## Legend

- ✅ = Created and ready to use
- ⏳ = Template ready, awaiting implementation
- 📄 = Documentation file
- 📂 = Directory
- 📊 = Data/Analysis component
- 🔧 = Code module

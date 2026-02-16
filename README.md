# Consumer Complaint Text Analytics Project

## INSY 669 - Text Analytics

**Team Members:**

- Ellie Ha
- Yanxin Li
- Yasmine Zhao
- Maral Vahedi

**Date:** January 23, 2026

---

## Project Overview

This project applies text analytics techniques to analyze consumer complaints from the Consumer Financial Protection Bureau (CFPB) database. The goal is to extract insights from unstructured complaint narratives and identify high-risk complaints requiring immediate attention.

### Objectives

1. **Content Analysis**: Extract keywords and key phrases to understand what consumers complain about
2. **Signal Analysis**: Identify urgency and escalation patterns to flag high-risk complaints
3. **Pattern Discovery**: Reveal recurring themes through co-occurring terms

---

## Dataset

- **Source**: Consumer Financial Protection Bureau (CFPB) Consumer Complaint Database
- **Size**: 1058741 consumer complaints
- **Key Fields**:
  - Consumer complaint narrative (free text)
  - Product category
  - Issue type
  - Company name
  - Response status

---

## Project Structure

```
text_analytics_project/
│
├── data/
│   ├── raw/                    # Original, immutable data
│   ├── interim/                # Intermediate transformed data
│   └── processed/              # Final, analysis-ready data
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_content_analysis.ipynb
│   ├── 04_signal_analysis.ipynb
│   └── 05_final_analysis.ipynb
│
├── src/
│   ├── data_processing/        # Data loading and cleaning scripts
│   ├── content_analysis/       # Keyword extraction, TF-IDF
│   ├── signal_analysis/        # Urgency detection features
│   └── visualization/          # Plotting and reporting functions
│
├── models/                     # Trained models and vectorizers
│
├── outputs/
│   ├── figures/                # Generated plots and visualizations
│   ├── tables/                 # Summary tables and statistics
│   └── reports/                # Final reports and presentations
│
├── docs/                       # Project documentation
│
├── references/                 # Data dictionaries, papers, manuals
│
├── requirements.txt            # Python dependencies
├── config.yaml                 # Configuration parameters
└── README.md                   # This file
```

---

## Methodology

### 1. Content Perspective (What consumers complain about)

- Light text cleaning (formatting, whitespace)
- Tokenization (unigrams, bigrams, trigrams)
- TF-IDF weighting for keyword extraction
- Phrase extraction for meaningful expressions

### 2. Signal Perspective (How consumers complain)

- Preserve stylistic elements (caps, punctuation)
- Extract emphasis features:
  - ALL-CAPS words frequency
  - Exclamation points
  - Repeated punctuation
  - Urgency indicators
- Combine with keywords to identify high-risk complaints

---

## Getting Started

### Prerequisites

```bash
python >= 3.8
pip
```

### Installation

```bash
# Clone or navigate to project directory
cd text_analytics_project

# Install dependencies
pip install -r requirements.txt
```

### Usage

1. Place raw data in `data/raw/`
2. Run notebooks in sequence (01 → 05)
3. Review outputs in `outputs/` directory

---

## Expected Outcomes

1. **Keyword Summaries**: Concise extraction of key terms representing common issues
2. **Theme Identification**: Frequently co-occurring terms revealing complaint patterns
3. **Risk Flagging**: Highlighted narratives with emphasis/escalation signals
4. **Actionable Insights**: Surface high-risk complaints from unstructured text

---

## Timeline

- **Week 1-2**: Data exploration and preprocessing
- **Week 3-4**: Content analysis (TF-IDF, keyword extraction)
- **Week 5-6**: Signal analysis (emphasis features)
- **Week 7-8**: Integration and final analysis
- **Week 9**: Report writing and presentation preparation

---

## License

This project is for academic purposes as part of INSY 669 coursework.

---

## Contact

For questions or collaboration, please contact any team member listed above.

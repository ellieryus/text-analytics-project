# 🚀 Project Setup Instructions
## INSY 669 - Consumer Complaint Text Analytics

---

## ✅ What Has Been Created

Your complete project structure is ready with:

### 📁 Directory Structure
- **data/** - Raw, interim, and processed data folders
- **notebooks/** - 5 Jupyter notebooks for sequential analysis
- **src/** - 4 Python modules with reusable functions
- **outputs/** - Folders for figures, tables, and reports
- **docs/** - Complete documentation
- **models/** - Storage for trained models

### 📄 Key Files Created
1. **README.md** - Project overview
2. **requirements.txt** - All Python dependencies
3. **config.yaml** - Configurable parameters
4. **.gitignore** - Version control setup
5. **01_data_exploration.ipynb** - First analysis notebook (ready to run)

### 🔧 Python Modules
1. **data_processing/** - DataLoader, DataCleaner classes
2. **content_analysis/** - KeywordExtractor, PhraseExtractor
3. **signal_analysis/** - EmphasisDetector, RiskClassifier
4. **visualization/** - All plotting functions

### 📚 Documentation
1. **PROJECT_DOCUMENTATION.md** - Complete methodology guide
2. **QUICK_START.md** - Step-by-step usage instructions
3. **PROJECT_STRUCTURE.md** - Visual directory layout

---

## 🎯 Next Steps (What YOU Need to Do)

### Step 1: Move Your Dataset ⏰ (5 minutes)

You mentioned you already downloaded the dataset. You need to:

1. **Locate your downloaded CSV file** (probably named something like `consumer_complaints.csv`)

2. **Move it to the correct location:**
   ```
   text_analytics_project/data/raw/consumer_complaints.csv
   ```

3. **If your file has a different name**, update the path in `config.yaml`:
   ```yaml
   data:
     raw_data_path: "data/raw/YOUR_FILENAME.csv"
   ```

### Step 2: Set Up Python Environment ⏰ (10 minutes)

```bash
# Navigate to project directory
cd text_analytics_project

# Create virtual environment (recommended)
python -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

### Step 3: Download NLTK Data ⏰ (2 minutes)

Open Python and run:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
```

Or run this in the first cell of your notebook.

### Step 4: Start Jupyter ⏰ (1 minute)

```bash
# From project root
jupyter notebook
```

This will open Jupyter in your browser.

### Step 5: Run First Notebook ⏰ (15 minutes)

1. Navigate to `notebooks/`
2. Open `01_data_exploration.ipynb`
3. Run all cells (Cell → Run All)
4. Review the outputs and understand your data

---

## 📝 Recommended Workflow

### Week 1-2: Data Understanding
- ✅ **Already done:** Project setup
- 🔲 **To do:** Run 01_data_exploration.ipynb
- 🔲 **To do:** Create 02_data_preprocessing.ipynb
- 🔲 **Deliverable:** Clean dataset + exploration report

### Week 3-4: Content Analysis
- 🔲 **To do:** Create 03_content_analysis.ipynb
- 🔲 **To do:** Extract top keywords using TF-IDF
- 🔲 **To do:** Generate word clouds
- 🔲 **To do:** Analyze bigrams and trigrams
- 🔲 **Deliverable:** Keyword summary tables + visualizations

### Week 5-6: Signal Analysis
- 🔲 **To do:** Create 04_signal_analysis.ipynb
- 🔲 **To do:** Calculate emphasis scores
- 🔲 **To do:** Classify risk levels
- 🔲 **To do:** Identify high-risk complaints
- 🔲 **Deliverable:** Risk classification report

### Week 7-8: Integration & Reporting
- 🔲 **To do:** Create 05_final_analysis.ipynb
- 🔲 **To do:** Combine content + signal insights
- 🔲 **To do:** Generate comprehensive visualizations
- 🔲 **To do:** Prepare final presentation
- 🔲 **Deliverable:** Final report + presentation

---

## 🛠️ How to Use the Python Modules

The modules in `src/` are ready to use. Here are examples:

### Load Data
```python
from src.data_processing import DataLoader

loader = DataLoader('config.yaml')
df = loader.load_raw_data()
complaints = loader.get_text_column(df)
```

### Extract Keywords
```python
from src.content_analysis.keyword_extraction import KeywordExtractor

extractor = KeywordExtractor()
tfidf_matrix = extractor.fit_tfidf(complaints, ngram_range=(1,3))
keywords = extractor.get_top_keywords(tfidf_matrix, n=50)
```

### Detect Emphasis
```python
from src.signal_analysis.emphasis_detection import EmphasisDetector

detector = EmphasisDetector()
score = detector.calculate_emphasis_score(complaint_text)
features = detector.extract_all_features(complaint_text)
```

### Create Visualizations
```python
from src.visualization.plots import plot_keyword_frequency

plot_keyword_frequency(
    keywords, 
    n=20,
    save_path='outputs/figures/top_keywords.png'
)
```

---

## 📊 Expected Project Outputs

By the end, you should have:

### Figures (outputs/figures/)
1. Top keyword bar charts
2. Word clouds (overall + by category)
3. Emphasis score distributions
4. Risk level breakdowns
5. N-gram frequency plots
6. Feature correlation heatmaps

### Tables (outputs/tables/)
1. Top 50-100 keywords (CSV)
2. High-risk complaints list (CSV)
3. Bigram/trigram frequencies (CSV)
4. Summary statistics (CSV)

### Reports (outputs/reports/)
1. Final analysis report (PDF/DOCX)
2. Presentation slides (PPTX)
3. Executive summary

---

## 🎓 Tips for Success

### Collaboration
- **Divide the work:** Each team member takes 1-2 notebooks
- **Share findings:** Regular check-ins on progress
- **Code review:** Review each other's code before merging
- **Document everything:** Add markdown cells explaining your work

### Code Quality
- Use the provided modules - they're tested and ready
- Add comments to explain complex logic
- Use descriptive variable names
- Save your work frequently

### Analysis Tips
- Start with small data samples to test code
- Validate results manually (spot-check keywords)
- Create visualizations to understand patterns
- Don't just report results - interpret them

### Time Management
- Week 1-2 are critical for setup and understanding
- Don't skip data exploration - it informs everything else
- Leave time for report writing and presentation prep
- Build in buffer time for unexpected issues

---

## 🆘 Troubleshooting

### "Module not found" error
```python
# Add this at the top of notebooks
import sys
sys.path.append('../src')
```

### "File not found" error
- Check your file paths in config.yaml
- Make sure data is in data/raw/
- Use relative paths, not absolute

### "NLTK data not found"
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### Out of memory
- Process data in smaller chunks
- Reduce max_features in TF-IDF
- Close other applications

### Jupyter won't start
```bash
# Reinstall Jupyter
pip install --upgrade jupyter
```

---

## 📖 Documentation Guide

### Where to Find Information

**General Overview:**
- `README.md` - Start here

**Setup Instructions:**
- `docs/QUICK_START.md` - Detailed setup guide

**Methodology:**
- `docs/PROJECT_DOCUMENTATION.md` - Theory and approach

**Project Structure:**
- `PROJECT_STRUCTURE.md` - Visual directory map

**Code Documentation:**
- Check docstrings in Python modules
- Example: `help(DataLoader)`

---

## ✉️ Team Communication

### Recommended Tools
- **GitHub** - Version control (push notebooks regularly)
- **Slack/Teams** - Daily communication
- **Google Docs** - Collaborative report writing
- **Zoom** - Weekly sync meetings

### What to Share
1. Completed notebooks
2. Generated outputs (figures, tables)
3. Findings and insights
4. Issues and blockers
5. Updated code in src/

---

## 🎯 Deliverables Checklist

### Technical Deliverables
- [ ] Clean, documented code
- [ ] 5 completed Jupyter notebooks
- [ ] All visualizations saved
- [ ] Summary tables exported
- [ ] Working Python modules

### Analysis Deliverables
- [ ] Top keywords by category
- [ ] Key phrase extraction
- [ ] High-risk complaint identification
- [ ] Emphasis pattern analysis
- [ ] Thematic clustering

### Presentation Deliverables
- [ ] Final report (10-15 pages)
- [ ] Presentation slides (15-20 slides)
- [ ] Executive summary (1-2 pages)
- [ ] Code repository (GitHub)

---

## 🚀 You're Ready to Start!

Everything is set up and ready to go. Your next immediate actions:

1. ✅ **Place your data file** in `data/raw/`
2. ✅ **Install dependencies** with `pip install -r requirements.txt`
3. ✅ **Download NLTK data**
4. ✅ **Open and run** `01_data_exploration.ipynb`
5. ✅ **Review outputs** and understand your data

Good luck with your project! 🎉

---

**Questions?** Check the documentation files or ask your team members.

**Team:** Yanxin Li, Yasmine Zhao, Ellie Ha, Maral Vahedi

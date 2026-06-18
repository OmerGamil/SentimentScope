# 🎯 SentimentScope

**Turn text into insight.** A multi-page Streamlit dashboard for real-time sentiment analysis using VADER and TextBlob.

![SentimentScope](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)

---

## Features

| Page | Description |
|------|-------------|
| **📊 Demo** | Preloaded Twitter data covering 8 tech brands — instant analysis with charts and word clouds |
| **✍️ Analyze Text** | Paste any text, get a compound score gauge, breakdown bars, and sentence-level analysis |
| **📁 Upload CSV** | Upload your own dataset, select the text column, download enriched results |
| **ℹ️ About** | Methodology, score ranges, business use cases, and dataset credits |

---

## Screenshots

> _Add screenshots here after first run_

---

## Setup — Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/OmerGamil/SentimentScope.git
cd SentimentScope/sentimentscope
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download NLTK data (one-time, automatic on first run)

The app downloads `punkt` and `punkt_tab` automatically on first launch.

### 5. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Deploy to Streamlit Cloud

1. Push the repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in.
3. Click **New app**.
4. Select your repo, set **Main file path** to `sentimentscope/app.py`.
5. Click **Deploy** — Streamlit Cloud installs `requirements.txt` automatically.

> **Note:** The `data/sample_tweets.csv` file must be committed to the repo for the Demo page to work.

---

## Sentiment Logic

| Compound Score | Label |
|---------------|-------|
| ≥ 0.05 | **Positive** |
| −0.05 to 0.05 | **Neutral** |
| ≤ −0.05 | **Negative** |

- **Primary:** VADER (Valence Aware Dictionary and sEntiment Reasoner) — optimized for social media text
- **Secondary:** TextBlob polarity — used as a cross-validation score

---

## Dataset Credit

**Twitter Entity Sentiment Analysis**
Source: [Kaggle — jp797498e](https://www.kaggle.com/datasets/jp797498e/twitter-entity-sentiment-analysis)
License: CC0 Public Domain

The `data/sample_tweets.csv` file used in Demo mode is a representative synthetic sample
inspired by this dataset, covering 8 major tech brands across Positive, Negative, Neutral,
and Irrelevant sentiment categories.

---

## Project Structure

```
sentimentscope/
├── app.py                  # Main entry point (home page)
├── pages/
│   ├── 1_Demo.py           # Demo with preloaded dataset
│   ├── 2_Analyze_Text.py   # Single text analysis
│   ├── 3_Upload_CSV.py     # CSV upload and batch analysis
│   └── 4_About.py          # Methodology and credits
├── data/
│   └── sample_tweets.csv   # 108-row sample dataset
├── utils/
│   ├── __init__.py
│   ├── sentiment.py        # VADER + TextBlob logic
│   └── charts.py           # Plotly chart functions
├── requirements.txt
├── README.md
└── .streamlit/
    └── config.toml         # Dark theme configuration
```

---

## License

MIT

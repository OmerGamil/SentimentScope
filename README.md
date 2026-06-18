# SentimentScope

**Turn any text into actionable insight — powered by VADER, RoBERTa, and TextBlob.**

SentimentScope is a production-ready, multi-model sentiment analysis dashboard built with Streamlit. It combines a fast lexicon-based classifier (VADER) with a state-of-the-art transformer (RoBERTa fine-tuned on 58 million tweets) to give businesses reliable, explainable sentiment scores on any text — from a single customer review to a 10,000-row CSV export.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![HuggingFace](https://img.shields.io/badge/🤗%20RoBERTa-twitter--roberta--base--sentiment-FFD21E?style=flat-square)](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest)
[![License](https://img.shields.io/badge/License-MIT-7C3AED?style=flat-square)](LICENSE)

---

## Why This Exists

Customer sentiment is the most underutilised signal in most businesses. Reviews, support tickets, survey responses, social mentions — companies collect mountains of text but rarely have the tooling to process it at scale without paying for enterprise NLP APIs.

SentimentScope solves that:

| Problem | SentimentScope answer |
|---|---|
| Manual review tagging takes hours | Classify thousands of rows in seconds |
| Single-model results are unreliable | Three independent models with a disagreement flag |
| "Positive/Negative" isn't enough | Confidence scores, subjectivity, and compound floats |
| No visibility into trends | Time-series chart auto-grouped by day / week / month / quarter |
| Hard to share results | One-click CSV download of enriched data |

---

## Features

### 📊 Demo — Instant Brand Sentiment
Explore a preloaded dataset of tweets across 8 major tech brands. Charts, word clouds, and per-entity breakdowns load instantly — no setup needed. Great for demos and presentations.

### ✍️ Analyse Text — Deep Single-Text Analysis
Paste any text and get:
- **Dual model badges** — VADER compound score + RoBERTa confidence probabilities side by side
- **Model disagreement alert** — flagged automatically when VADER says Positive and RoBERTa says Negative (or vice versa), a strong signal of sarcasm, irony, or domain-specific language
- **Sentence-level breakdown** — each sentence scored individually so you can pinpoint exactly where sentiment shifts
- **TextBlob cross-check** — polarity and subjectivity scores for additional context
- **Downloadable breakdown table** — export sentence scores as CSV

### 📁 Upload CSV — Bulk Analysis
Upload any CSV with a text column and get the full suite:
- Runs VADER + TextBlob on every row (RoBERTa reserved for single texts to keep bulk analysis fast)
- Auto-detects date columns and renders a **sentiment trend chart** grouped by the right time period
- Category/entity grouping bar chart
- Word clouds by sentiment class
- VADER vs TextBlob scatter plot for model agreement overview
- Full enriched CSV download

### ⚡ Batch Analysis — Multi-Text Comparison
Paste one text per line and analyse them all in a single run. Useful for comparing product variants, A/B message testing, or quickly scoring a list of headlines.

### ℹ️ About — Methodology & Use Cases
Score interpretation guide, model cards, and business use cases with a full tech stack table.

---

## Business Use Cases

**Brand & Reputation Monitoring** — Track customer sentiment across social media and review platforms in real time. Spot PR crises before they escalate by detecting negative sentiment spikes.

**E-commerce Review Intelligence** — Automatically classify product reviews to surface quality issues, rank SKUs by sentiment, and identify high-value testimonials for marketing.

**Customer Support Triage** — Score incoming messages by sentiment and urgency. Route high-negativity tickets to senior agents, auto-tag positives for the CSAT report.

**Market Research & Surveys** — Replace manual coding of open-ended survey responses with automated scoring across thousands of submissions in seconds.

**Financial Sentiment Signals** — Analyse earnings call transcripts, analyst notes, or social mentions to identify directional market sentiment alongside quantitative signals.

**Media & News Monitoring** — Gauge public sentiment toward events, political figures, or organisations from news headlines and social commentary at scale.

**Gaming & Community Management** — Monitor player feedback on forums, Steam, Discord, and Reddit after each game patch or update to prioritise response.

**Healthcare & Patient Feedback** — Classify patient experience responses to identify service improvement areas while maintaining compliance with data handling requirements.

---

## How It Works — The Three-Model Stack

```
Input text
    │
    ├── VADER ──────────────────► Compound score (−1 to +1) + P/N/Neu breakdown
    │   Fast, lexicon-based                  Always runs — used for all bulk analysis
    │   Handles emojis, CAPS, slang
    │
    ├── RoBERTa ─────────────────► Label + confidence probabilities
    │   Transformer, 58M tweets              Optional (Analyse Text + Batch pages)
    │   Context-aware, handles negation      ~500 MB download, cached after first use
    │
    └── TextBlob ────────────────► Polarity (−1 to +1) + Subjectivity (0 to 1)
        Linguistic approach                  Always runs — good for formal prose
        Better for objective writing
```

**Disagreement signal:** when VADER and RoBERTa produce opposite verdicts (one Positive, one Negative), the app flags it with a warning. This disagreement is often the most valuable output — it surfaces ambiguous language that deserves a human second look.

### Compound Score Ranges

| Score | Label |
|---|---|
| ≥ 0.05 | **Positive** |
| −0.05 to 0.05 | **Neutral** |
| ≤ −0.05 | **Negative** |

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/OmerGamil/SentimentScope.git
cd SentimentScope
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

> **Note:** PyTorch (~800 MB) downloads on first install. The RoBERTa model (~500 MB) downloads from Hugging Face on first use of the Analyse Text page and is then cached locally.

### 4. Run

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501).

---

## Deploy to Heroku

### Prerequisites
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed and logged in
- A Heroku account

### Steps

```bash
# 1. Create a new Heroku app
heroku create your-app-name

# 2. Set the Python buildpack
heroku buildpacks:set heroku/python

# 3. Deploy
git push heroku main
```

The `Procfile` and `runtime.txt` are already included. Heroku will install all dependencies automatically.

> **Memory note:** The RoBERTa model requires at least **1 GB of RAM** at inference time. Use a Standard-2X dyno or higher (`heroku ps:scale web=1:standard-2x`) for reliable transformer inference. The Demo and CSV pages use VADER only and run fine on a Basic dyno.

### Environment variables (optional)

| Variable | Purpose |
|---|---|
| `TRANSFORMERS_CACHE` | Override Hugging Face model cache path |

---

## Project Structure

```
sentimentscope/
├── app.py                    # Home page — hero, feature cards, how-it-works
├── pages/
│   ├── 1_Demo.py             # Preloaded Twitter dataset — brand sentiment
│   ├── 2_Analyze_Text.py     # Single text — dual models, sentence breakdown
│   ├── 3_Upload_CSV.py       # CSV upload — bulk analysis, time series
│   ├── 4_Batch.py            # One text per line — batch comparison
│   └── 5_About.py            # Methodology, model cards, use cases
├── utils/
│   ├── __init__.py
│   ├── sentiment.py          # VADER + RoBERTa + TextBlob engine
│   ├── charts.py             # Plotly chart functions
│   ├── sidebar.py            # Shared sidebar + CSS injection
│   └── styles.py             # Design system — CSS + HTML helpers
├── data/
│   └── sample_tweets.csv     # 108-row demo dataset (CC0)
├── .streamlit/
│   └── config.toml           # Light violet theme
├── Procfile                  # Heroku process definition
├── runtime.txt               # Python version pin
└── requirements.txt          # Python dependencies
```

---

## Tech Stack

| Layer | Library | Purpose |
|---|---|---|
| UI | [Streamlit](https://streamlit.io) | Multi-page dashboard framework |
| Fast NLP | [vaderSentiment](https://github.com/cjhutto/vaderSentiment) | Lexicon-based compound scoring |
| Transformer NLP | [transformers](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest) · RoBERTa | High-accuracy deep learning sentiment |
| Cross-check NLP | [TextBlob](https://textblob.readthedocs.io) | Polarity & subjectivity |
| Data | [Pandas](https://pandas.pydata.org) | DataFrame processing |
| Charts | [Plotly Express](https://plotly.com/python/) | Interactive visualisations |
| Word Clouds | [wordcloud](https://github.com/amueller/word_cloud) | Text frequency art |
| Deep Learning | [PyTorch](https://pytorch.org) | Transformer inference backend |

---

## Dataset Credit

**Twitter Entity Sentiment Analysis**
Source: [Kaggle — jp797498e](https://www.kaggle.com/datasets/jp797498e/twitter-entity-sentiment-analysis) · CC0 Public Domain

The `data/sample_tweets.csv` file is a representative sample covering 8 major tech brands across Positive, Negative, Neutral, and Irrelevant sentiment categories.

---

## License

MIT — see [LICENSE](LICENSE) for details.

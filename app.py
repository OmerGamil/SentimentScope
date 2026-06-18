import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

import streamlit as st
from utils.sidebar import render_sidebar
from utils.styles import hero, feature_cards, step_cards, section, divider

st.set_page_config(
    page_title="SentimentScope",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar("""
**Navigate:**

📊 **Demo** — Preloaded Twitter data
✍️ **Analyze Text** — Instant single-text analysis
📦 **Batch** — Multiple texts at once
📁 **Upload CSV** — Analyze your dataset
ℹ️ **About** — Methodology & use cases
""")

st.markdown(hero(
    "NLP · Sentiment Analysis · Data Science",
    "Sentiment",
    "Scope",
    "Turn any text into actionable insight. Powered by VADER, RoBERTa, and TextBlob.",
), unsafe_allow_html=True)

st.markdown(feature_cards(
    ("📊", "Demo Mode",
     "Explore live sentiment analysis on a preloaded Twitter dataset covering 8 major tech brands."),
    ("✍️", "Analyze Text",
     "Paste any text and get instant VADER + RoBERTa scores, a confidence badge, and sentence-level breakdown."),
    ("📦", "Batch Analysis",
     "Paste multiple texts — one per line — for rapid bulk scoring with downloadable results."),
    ("📁", "Upload CSV",
     "Upload your own dataset, select any text column, and analyze thousands of rows in seconds."),
), unsafe_allow_html=True)

st.markdown(section("How It Works"), unsafe_allow_html=True)

st.markdown(step_cards(
    ("VADER Analysis",
     "Lexicon-based model optimized for social media. Returns a compound score from −1 to +1. Fast enough for bulk CSV analysis."),
    ("RoBERTa (optional)",
     "Transformer fine-tuned on 58M tweets. More accurate for sarcasm, negation, and ambiguous language. Used on Analyze Text."),
    ("TextBlob Cross-check",
     "Provides a secondary polarity score and a subjectivity score — useful for filtering out factual, objective content."),
    ("Disagreement Signal",
     "When VADER and RoBERTa give opposite labels the app surfaces a warning banner, flagging potential sarcasm or irony."),
    ("Classification",
     "Compound ≥ 0.05 → Positive. Between −0.05 and 0.05 → Neutral. ≤ −0.05 → Negative."),
    ("Time Series",
     "If your CSV has a date column, the Upload CSV page renders an average-compound trend chart over time."),
), unsafe_allow_html=True)

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from utils.sentiment import analyze_dataframe
from utils.charts import (
    pie_chart,
    bar_by_entity,
    generate_wordcloud,
    scatter_vader_textblob,
    compound_histogram,
)
from utils.sidebar import render_sidebar
from utils.styles import page_header, stats, section, divider

st.set_page_config(
    page_title="Demo | SentimentScope",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar()

st.markdown(page_header(
    "📊 Demo — Twitter Entity Sentiment",
    "Preloaded sample from the Twitter Entity Sentiment Analysis dataset (Kaggle) · 108 tweets · 8 brands",
), unsafe_allow_html=True)


@st.cache_data(show_spinner="Running VADER & TextBlob analysis...")
def load_and_analyze():
    data_path = ROOT / "data" / "sample_tweets.csv"
    df = pd.read_csv(data_path)
    return analyze_dataframe(df, "tweet_content")


df = load_and_analyze()

counts = df["vader_label"].value_counts()
total = len(df)
pos = counts.get("Positive", 0)
neu = counts.get("Neutral", 0)
neg = counts.get("Negative", 0)

st.markdown(stats(total, pos, neu, neg), unsafe_allow_html=True)

# ── Distribution charts ───────────────────────────────────────────────────────
st.markdown(section("Sentiment Distribution"), unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(pie_chart(df), use_container_width=True)
with c2:
    st.plotly_chart(compound_histogram(df), use_container_width=True)

# ── Entity bar chart ─────────────────────────────────────────────────────────
if "entity" in df.columns:
    st.markdown(section("Sentiment by Brand"), unsafe_allow_html=True)
    st.plotly_chart(bar_by_entity(df, "entity"), use_container_width=True)

# ── Word clouds ───────────────────────────────────────────────────────────────
st.markdown(section("Word Clouds by Sentiment"), unsafe_allow_html=True)
wc1, wc2, wc3 = st.columns(3)

for col, sentiment in zip([wc1, wc2, wc3], ["Positive", "Neutral", "Negative"]):
    with col:
        texts = df[df["vader_label"] == sentiment]["tweet_content"].astype(str).tolist()
        fig = generate_wordcloud(texts, sentiment)
        if fig:
            st.pyplot(fig)
        else:
            st.info(f"Not enough {sentiment} text for a word cloud.")

# ── Top tweets tables ─────────────────────────────────────────────────────────
st.markdown(divider(), unsafe_allow_html=True)
cols_show = [c for c in ["tweet_content", "entity", "vader_compound"] if c in df.columns]

col_a, col_b = st.columns(2)
with col_a:
    st.markdown(section("Top Positive Tweets"), unsafe_allow_html=True)
    top_pos = df[df["vader_label"] == "Positive"].nlargest(5, "vader_compound")[cols_show]
    st.dataframe(top_pos, use_container_width=True, hide_index=True)

with col_b:
    st.markdown(section("Top Negative Tweets"), unsafe_allow_html=True)
    top_neg = df[df["vader_label"] == "Negative"].nsmallest(5, "vader_compound")[cols_show]
    st.dataframe(top_neg, use_container_width=True, hide_index=True)

# ── VADER vs TextBlob ─────────────────────────────────────────────────────────
st.markdown(section("VADER vs TextBlob Comparison"), unsafe_allow_html=True)
st.plotly_chart(scatter_vader_textblob(df), use_container_width=True)

# ── Raw data expander ─────────────────────────────────────────────────────────
with st.expander("View full dataset"):
    display_cols = [c for c in [
        "tweet_content", "entity", "sentiment",
        "vader_label", "vader_compound", "textblob_polarity"
    ] if c in df.columns]
    st.dataframe(df[display_cols], use_container_width=True, hide_index=True)

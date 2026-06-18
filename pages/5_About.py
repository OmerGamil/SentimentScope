import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import streamlit as st
from utils.sidebar import render_sidebar
from utils.styles import page_header, section, divider

st.set_page_config(
    page_title="About | SentimentScope",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar()

st.markdown(page_header(
    "ℹ️ About SentimentScope",
    "Methodology, scoring guide, model details, and business use cases.",
), unsafe_allow_html=True)

# ── Score ranges ──────────────────────────────────────────────────────────────
st.markdown(section("Compound Score Ranges"), unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
<div style="background:#ECFDF5;border:1px solid #059669;border-left:3px solid #059669;border-radius:14px;padding:22px 20px;">
  <div style="color:#059669;font-size:0.72rem;text-transform:uppercase;letter-spacing:.1em;font-weight:700;margin-bottom:8px;">Positive</div>
  <div style="color:#059669;font-size:2.2rem;font-weight:900;letter-spacing:-.02em;margin-bottom:8px;">≥ 0.05</div>
  <div style="color:#065F46;font-size:.85rem;line-height:1.6;">Text expresses net positive sentiment. Stronger positivity as score approaches +1.</div>
</div>""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div style="background:#FFFBEB;border:1px solid #D97706;border-left:3px solid #D97706;border-radius:14px;padding:22px 20px;">
  <div style="color:#D97706;font-size:0.72rem;text-transform:uppercase;letter-spacing:.1em;font-weight:700;margin-bottom:8px;">Neutral</div>
  <div style="color:#D97706;font-size:2.2rem;font-weight:900;letter-spacing:-.02em;margin-bottom:8px;">−0.05 → 0.05</div>
  <div style="color:#78350F;font-size:.85rem;line-height:1.6;">Text does not lean either way. Factual or objective statements typically land here.</div>
</div>""", unsafe_allow_html=True)

with col3:
    st.markdown("""
<div style="background:#FEF2F2;border:1px solid #DC2626;border-left:3px solid #DC2626;border-radius:14px;padding:22px 20px;">
  <div style="color:#DC2626;font-size:0.72rem;text-transform:uppercase;letter-spacing:.1em;font-weight:700;margin-bottom:8px;">Negative</div>
  <div style="color:#DC2626;font-size:2.2rem;font-weight:900;letter-spacing:-.02em;margin-bottom:8px;">≤ −0.05</div>
  <div style="color:#7F1D1D;font-size:.85rem;line-height:1.6;">Text expresses net negative sentiment. Stronger negativity as score approaches −1.</div>
</div>""", unsafe_allow_html=True)

st.markdown(divider(), unsafe_allow_html=True)

# ── Models ────────────────────────────────────────────────────────────────────
st.markdown(section("Models"), unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)

with m1:
    st.markdown("""
<div style="background:#fff;border:1px solid rgba(124,58,237,0.1);border-radius:14px;padding:22px 20px;
            box-shadow:0 2px 8px rgba(124,58,237,0.07);">
  <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:.1em;color:#7C3AED;font-weight:700;margin-bottom:10px;">VADER</div>
  <div style="font-size:1rem;font-weight:700;color:#1E1433;margin-bottom:10px;">Lexicon-Based (Fast)</div>
  <div style="font-size:.82rem;color:#6B5FA0;line-height:1.65;">
    Rule-based model optimized for social media. Handles emojis, ALL-CAPS, slang, and punctuation like !!!.
    No training required — used for all bulk analysis.
  </div>
</div>""", unsafe_allow_html=True)

with m2:
    st.markdown("""
<div style="background:#fff;border:1px solid rgba(124,58,237,0.1);border-radius:14px;padding:22px 20px;
            box-shadow:0 2px 8px rgba(124,58,237,0.07);">
  <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:.1em;color:#7C3AED;font-weight:700;margin-bottom:10px;">RoBERTa</div>
  <div style="font-size:1rem;font-weight:700;color:#1E1433;margin-bottom:10px;">Transformer (Accurate)</div>
  <div style="font-size:.82rem;color:#6B5FA0;line-height:1.65;">
    Fine-tuned on 58M tweets. Understands context, sarcasm, and complex negation.
    ~500 MB download on first use, then cached. Used on the Analyze Text page.
  </div>
</div>""", unsafe_allow_html=True)

with m3:
    st.markdown("""
<div style="background:#fff;border:1px solid rgba(124,58,237,0.1);border-radius:14px;padding:22px 20px;
            box-shadow:0 2px 8px rgba(124,58,237,0.07);">
  <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:.1em;color:#9B8FC0;font-weight:700;margin-bottom:10px;">TextBlob</div>
  <div style="font-size:1rem;font-weight:700;color:#1E1433;margin-bottom:10px;">Cross-Check</div>
  <div style="font-size:.82rem;color:#6B5FA0;line-height:1.65;">
    Provides polarity (−1 to +1) and subjectivity (0 to 1) scores.
    Better for formal prose. Useful for filtering out objective statements.
  </div>
</div>""", unsafe_allow_html=True)

st.markdown(divider(), unsafe_allow_html=True)

# ── Business use cases ────────────────────────────────────────────────────────
st.markdown(section("Business Use Cases"), unsafe_allow_html=True)
uc1, uc2 = st.columns(2)

with uc1:
    st.markdown("""
**📣 Brand Monitoring** — Track customer sentiment across social media. Detect PR crises early by monitoring negative sentiment spikes.

**🛒 E-commerce Reviews** — Automatically classify product reviews to surface quality issues, identify top-rated SKUs, and prioritize support tickets.

**📞 Customer Support Triage** — Route incoming messages by sentiment. Urgent negative tickets get escalated; positive feedback gets logged for testimonials.

**📰 News & Media** — Gauge public sentiment toward events, politicians, or brands in real time.
""")

with uc2:
    st.markdown("""
**📋 Survey Analysis** — Analyze open-ended responses at scale. Replace manual coding of thousands of free-text answers with automated scoring.

**📈 Financial Sentiment** — Analyze earnings transcripts, analyst reports, or social mentions to identify market sentiment signals.

**🎮 Gaming & Community** — Monitor player feedback on forums, Steam, and Discord after each game update.

**🏥 Healthcare Feedback** — Classify patient reviews to identify service improvements while maintaining privacy compliance.
""")

# ── Tech stack ────────────────────────────────────────────────────────────────
st.markdown(divider(), unsafe_allow_html=True)
st.markdown(section("Tech Stack"), unsafe_allow_html=True)
st.markdown("""
| Component | Library | Purpose |
|-----------|---------|---------|
| UI | [Streamlit](https://streamlit.io) | Multi-page dashboard |
| Fast NLP | [vaderSentiment](https://github.com/cjhutto/vaderSentiment) | Compound scoring — bulk & demo |
| Deep Learning NLP | [transformers](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest) · RoBERTa | High-accuracy transformer model |
| Secondary NLP | [TextBlob](https://textblob.readthedocs.io) | Polarity & subjectivity |
| Data | [Pandas](https://pandas.pydata.org) | DataFrame manipulation |
| Charts | [Plotly Express](https://plotly.com/python/plotly-express/) | Interactive visualizations |
| Word Clouds | [wordcloud](https://github.com/amueller/word_cloud) | Text frequency art |
| Demo Data | [Twitter Entity Sentiment Analysis](https://www.kaggle.com/datasets/jp797498e/twitter-entity-sentiment-analysis) | Kaggle · CC0 |
""")

# ── Source ────────────────────────────────────────────────────────────────────
st.markdown(divider(), unsafe_allow_html=True)
st.markdown("""
**GitHub:** [github.com/OmerGamil/SentimentScope](https://github.com/OmerGamil/SentimentScope)

Built as part of the Code Institute Data Science curriculum.
""")

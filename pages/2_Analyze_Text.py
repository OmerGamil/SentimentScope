import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st
from utils.sentiment import analyze_text, analyze_sentences, load_transformer_pipeline, ROBERTA_ENABLED
from utils.charts import compound_gauge, score_bars
from utils.sidebar import render_sidebar
from utils.styles import page_header, section, divider, badges, disagree_banner

st.set_page_config(
    page_title="Analyze Text | SentimentScope",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar("""
**Tips**

- Paste multiple sentences for a sentence-level breakdown
- Toggle RoBERTa for transformer-based scoring
- Use the examples dropdown to explore
""")

st.markdown(page_header(
    "✍️ Analyze Text",
    "Paste any text and get instant sentiment scores with model-level and sentence-level breakdown.",
), unsafe_allow_html=True)

EXAMPLES = {
    "Positive review": "This product is absolutely amazing! I couldn't be happier with the quality and fast shipping. Highly recommend to everyone.",
    "Negative complaint": "Terrible experience. The product arrived broken, customer service was useless, and I still haven't received my refund after two weeks.",
    "Mixed feedback": "The food was delicious but the service was painfully slow. The ambiance was great though I wouldn't mind going back just for the atmosphere.",
    "Neutral statement": "The company released its annual report showing revenue of $4.2 billion. The board meeting is scheduled for next Tuesday.",
}

with st.expander("Try an example"):
    example_choice = st.selectbox("Choose an example:", list(EXAMPLES.keys()))
    if st.button("Load example"):
        st.session_state["input_text"] = EXAMPLES[example_choice]
        st.rerun()

user_text = st.text_area(
    "Enter text to analyze",
    value=st.session_state.get("input_text", ""),
    height=160,
    placeholder="Paste a tweet, review, comment, or any text here…",
    label_visibility="collapsed",
)

ctrl_left, ctrl_right = st.columns([3, 2])
with ctrl_left:
    if ROBERTA_ENABLED:
        use_roberta = st.checkbox(
            "Use RoBERTa  ·  more accurate, ~500 MB first-run download",
            value=False,
        )
    else:
        use_roberta = False
        st.caption("RoBERTa is disabled on this deployment — VADER + TextBlob active.")
with ctrl_right:
    analyze_btn = st.button("Analyze Sentiment", type="primary", use_container_width=True)

COLORS = {"Positive": "#2ECC71", "Neutral": "#F39C12", "Negative": "#E74C3C"}


@st.cache_resource(show_spinner="Loading RoBERTa — this only happens once…")
def _get_pipe():
    return load_transformer_pipeline()


if analyze_btn and user_text.strip():
    pipe = _get_pipe() if use_roberta else None
    result = analyze_text(user_text, pipe)
    sentences = analyze_sentences(user_text, pipe)

    label = result["label"]
    confidence = result["confidence"]
    roberta_label = result.get("roberta_label")
    roberta_compound = result.get("roberta_compound")
    has_roberta = roberta_label and roberta_label != "N/A"

    # ── Disagreement banner ───────────────────────────────────────────────────
    if result.get("disagreement"):
        st.markdown(disagree_banner(label, roberta_label), unsafe_allow_html=True)

    # ── Badges ────────────────────────────────────────────────────────────────
    st.markdown(badges(
        label, confidence, result["compound"],
        roberta_label if has_roberta else None,
        roberta_compound if has_roberta else None,
    ), unsafe_allow_html=True)

    # ── Gauge + score bars ────────────────────────────────────────────────────
    g_col, b_col = st.columns(2)
    with g_col:
        st.plotly_chart(compound_gauge(result["compound"], label), use_container_width=True)
    with b_col:
        st.plotly_chart(score_bars(result), use_container_width=True)

    # ── Metrics row ───────────────────────────────────────────────────────────
    st.markdown(divider(), unsafe_allow_html=True)
    if has_roberta:
        t1, t2, t3, t4, t5 = st.columns(5)
        t1.metric("VADER Compound", f"{result['compound']:+.4f}")
        t2.metric("VADER Label", label)
        t3.metric("RoBERTa Label", roberta_label)
        t4.metric("TextBlob Polarity", f"{result['textblob_polarity']:+.4f}")
        t5.metric("TextBlob Subjectivity", f"{result['textblob_subjectivity']:.4f}")
    else:
        t1, t2, t3, t4 = st.columns(4)
        t1.metric("VADER Compound", f"{result['compound']:+.4f}")
        t2.metric("TextBlob Polarity", f"{result['textblob_polarity']:+.4f}")
        t3.metric("TextBlob Subjectivity", f"{result['textblob_subjectivity']:.4f}")
        t4.metric("VADER Label", label)

    # ── Sentence breakdown ────────────────────────────────────────────────────
    if len(sentences) > 1:
        st.markdown(section(f"Sentence Breakdown — {len(sentences)} sentences"), unsafe_allow_html=True)
        rows = []
        for i, s in enumerate(sentences, 1):
            row = {
                "#": i,
                "Sentence": s["sentence"],
                "VADER Label": s["label"],
                "Compound": s["compound"],
                "Pos": s["positive"],
                "Neu": s["neutral"],
                "Neg": s["negative"],
            }
            if s.get("roberta_label") and s["roberta_label"] != "N/A":
                row["RoBERTa"] = s["roberta_label"]
            rows.append(row)
        sent_df = pd.DataFrame(rows)

        def color_label(val):
            c = COLORS.get(val, "")
            return f"color: {c}; font-weight: bold" if c else ""

        label_cols = [c for c in ["VADER Label", "RoBERTa"] if c in sent_df.columns]
        styled = sent_df.style.map(color_label, subset=label_cols)
        st.dataframe(styled, use_container_width=True, hide_index=True)

        st.download_button(
            label="⬇️ Download Sentence Breakdown",
            data=sent_df.to_csv(index=False).encode("utf-8"),
            file_name="sentence_breakdown.csv",
            mime="text/csv",
        )
    else:
        st.caption("Enter multiple sentences to see a sentence-by-sentence breakdown.")

elif analyze_btn:
    st.warning("Please enter some text to analyze.")

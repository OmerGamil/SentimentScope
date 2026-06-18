import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st
from utils.sentiment import analyze_text
from utils.charts import pie_chart, compound_histogram
from utils.sidebar import render_sidebar
from utils.styles import page_header, stats, section, divider

st.set_page_config(
    page_title="Batch | SentimentScope",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar("""
**Tips**

- One text per line
- Blank lines are skipped
- Results include VADER + TextBlob scores
- Download results as CSV
""")

st.markdown(page_header(
    "📦 Batch Analysis",
    "Analyze multiple texts at once — one per line — with downloadable results.",
), unsafe_allow_html=True)

EXAMPLE = """\
I absolutely love this product, it exceeded all my expectations!
The delivery was late and the item arrived damaged. Very disappointed.
The meeting is scheduled for Thursday at 3pm in conference room B.
This is hands down the best coffee I've ever had in my life.
Not great, not terrible. Does what it says on the tin.
Can't believe how bad the customer service was — never buying again.
Revenue figures for Q3 remain consistent with prior quarters.
Surprisingly good for the price point. Would recommend to a friend."""

hdr_left, hdr_right = st.columns([5, 1])
with hdr_right:
    if st.button("Load Example", use_container_width=True):
        st.session_state["batch_text"] = EXAMPLE
        st.rerun()

user_input = st.text_area(
    "Texts",
    value=st.session_state.get("batch_text", ""),
    height=220,
    placeholder="Paste one text per line…",
    label_visibility="collapsed",
)

analyze_btn = st.button("Analyze All", type="primary")

COLORS = {"Positive": "#2ECC71", "Neutral": "#F39C12", "Negative": "#E74C3C"}

if analyze_btn and user_input.strip():
    lines = [line.strip() for line in user_input.splitlines() if line.strip()]
    if not lines:
        st.warning("No valid lines found.")
        st.stop()

    with st.spinner(f"Analyzing {len(lines)} texts…"):
        raw = [analyze_text(line) for line in lines]

    results_df = pd.DataFrame([
        {
            "#": i + 1,
            "Text": lines[i],
            "Label": r["label"],
            "VADER Compound": r["compound"],
            "Confidence": r["confidence"],
            "TextBlob Polarity": r["textblob_polarity"],
            "Subjectivity": r["textblob_subjectivity"],
        }
        for i, r in enumerate(raw)
    ])

    total = len(results_df)
    lc = results_df["Label"].value_counts()
    pos, neu, neg = lc.get("Positive", 0), lc.get("Neutral", 0), lc.get("Negative", 0)

    st.markdown(stats(total, pos, neu, neg), unsafe_allow_html=True)

    # ── Charts ────────────────────────────────────────────────────────────────
    st.markdown(section("Distribution"), unsafe_allow_html=True)
    chart_df = results_df.rename(
        columns={"Label": "vader_label", "VADER Compound": "vader_compound"}
    )
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(pie_chart(chart_df), use_container_width=True)
    with c2:
        st.plotly_chart(compound_histogram(chart_df), use_container_width=True)

    # ── Results table ─────────────────────────────────────────────────────────
    st.markdown(section("Results"), unsafe_allow_html=True)

    def color_label(val):
        c = COLORS.get(val, "")
        return f"color: {c}; font-weight: bold" if c else ""

    styled = results_df.style.map(color_label, subset=["Label"])
    st.dataframe(styled, use_container_width=True, hide_index=True)

    st.download_button(
        label="⬇️ Download Results CSV",
        data=results_df.to_csv(index=False).encode("utf-8"),
        file_name="batch_results.csv",
        mime="text/csv",
    )

elif analyze_btn:
    st.warning("Please enter at least one line of text.")

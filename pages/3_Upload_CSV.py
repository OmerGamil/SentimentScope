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
    scatter_vader_textblob,
    compound_histogram,
    generate_wordcloud,
    time_series_chart,
)
from utils.sidebar import render_sidebar
from utils.styles import page_header, stats, section, divider

st.set_page_config(
    page_title="Upload CSV | SentimentScope",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar("""
**CSV Requirements**

- At least one text column (string)
- UTF-8 or latin-1 encoding
- Any number of rows

**Output columns added:**
`vader_compound`, `vader_label`, `vader_positive`, `vader_neutral`, `vader_negative`, `textblob_polarity`, `textblob_subjectivity`
""")

st.markdown(page_header(
    "📁 Upload CSV",
    "Upload any CSV with a text column and analyze thousands of rows in seconds.",
), unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drop your CSV here or click to browse",
    type=["csv"],
    help="Must contain at least one string column.",
)

if uploaded_file is not None:
    try:
        try:
            raw_df = pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            raw_df = pd.read_csv(uploaded_file, encoding="latin-1")
    except Exception as e:
        st.error(f"Could not read file: {e}")
        st.stop()

    st.success(f"Loaded **{len(raw_df):,} rows** × **{len(raw_df.columns)} columns**")

    text_candidates = [
        c for c in raw_df.columns
        if raw_df[c].dtype == object and raw_df[c].notna().sum() > 0
    ]
    if not text_candidates:
        st.error("No text columns found. Please upload a CSV with at least one string column.")
        st.stop()

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        text_col = st.selectbox("Text column to analyze:", text_candidates)
    with col_b:
        other_cols = [c for c in raw_df.columns if c != text_col]
        object_cols = [c for c in other_cols if raw_df[c].dtype == object]
        entity_col = st.selectbox(
            "Category column (optional):",
            ["(none)"] + object_cols,
        )
        if entity_col == "(none)":
            entity_col = None
    with col_c:
        date_col = st.selectbox(
            "Date column for trend (optional):",
            ["(none)"] + other_cols,
        )
        if date_col == "(none)":
            date_col = None

    preview_rows = min(5, len(raw_df))
    with st.expander(f"Preview — first {preview_rows} rows"):
        st.dataframe(raw_df.head(preview_rows), use_container_width=True, hide_index=True)

    if st.button("Run Sentiment Analysis", type="primary"):
        with st.spinner(f"Analyzing {len(raw_df):,} rows…"):
            results_df = analyze_dataframe(raw_df, text_col)

        st.success("Analysis complete!")

        counts = results_df["vader_label"].value_counts()
        total = len(results_df)
        pos = counts.get("Positive", 0)
        neu = counts.get("Neutral", 0)
        neg = counts.get("Negative", 0)

        st.markdown(stats(total, pos, neu, neg), unsafe_allow_html=True)

        # ── Distribution charts ───────────────────────────────────────────────
        st.markdown(section("Distribution"), unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(pie_chart(results_df), use_container_width=True)
        with c2:
            st.plotly_chart(compound_histogram(results_df), use_container_width=True)

        if entity_col:
            st.markdown(section(f"Sentiment by {entity_col.replace('_', ' ').title()}"), unsafe_allow_html=True)
            st.plotly_chart(bar_by_entity(results_df, entity_col), use_container_width=True)

        # ── Time series ───────────────────────────────────────────────────────
        if date_col:
            ts_fig = time_series_chart(results_df, date_col)
            if ts_fig:
                st.markdown(section("Sentiment Over Time"), unsafe_allow_html=True)
                st.plotly_chart(ts_fig, use_container_width=True)
            else:
                st.info(f"Could not parse '{date_col}' as dates — skipping trend chart.")

        # ── Word clouds ───────────────────────────────────────────────────────
        st.markdown(section("Word Clouds by Sentiment"), unsafe_allow_html=True)
        wc1, wc2, wc3 = st.columns(3)
        for col, sentiment in zip([wc1, wc2, wc3], ["Positive", "Neutral", "Negative"]):
            with col:
                texts = (
                    results_df[results_df["vader_label"] == sentiment][text_col]
                    .astype(str).tolist()
                )
                fig = generate_wordcloud(texts, sentiment)
                if fig:
                    st.pyplot(fig)
                else:
                    st.info(f"Not enough {sentiment} text.")

        # ── VADER vs TextBlob scatter ─────────────────────────────────────────
        st.markdown(section("VADER vs TextBlob"), unsafe_allow_html=True)
        st.plotly_chart(scatter_vader_textblob(results_df), use_container_width=True)

        # ── Results preview ───────────────────────────────────────────────────
        st.markdown(section("Results Preview"), unsafe_allow_html=True)
        result_cols = (
            [text_col]
            + ([entity_col] if entity_col else [])
            + ([date_col] if date_col else [])
            + ["vader_label", "vader_compound", "textblob_polarity", "textblob_subjectivity"]
        )
        result_cols = [c for c in result_cols if c in results_df.columns]
        st.dataframe(results_df[result_cols].head(50), use_container_width=True, hide_index=True)

        # ── Download ──────────────────────────────────────────────────────────
        st.markdown(divider(), unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download Full Results CSV",
            data=results_df.to_csv(index=False).encode("utf-8"),
            file_name="sentiment_results.csv",
            mime="text/csv",
        )
        st.caption(
            "Download includes all original columns plus: `vader_compound`, `vader_label`, "
            "`vader_positive`, `vader_neutral`, `vader_negative`, `textblob_polarity`, `textblob_subjectivity`"
        )
else:
    st.markdown("""
<div style="background:#FFFFFF;border:1.5px dashed rgba(124,58,237,0.2);border-radius:14px;padding:36px;text-align:center;margin-top:8px;box-shadow:0 2px 8px rgba(124,58,237,0.06);">
  <div style="font-size:2rem;margin-bottom:12px;">📂</div>
  <div style="font-size:1rem;font-weight:600;color:#1E1433;margin-bottom:8px;">Upload a CSV to get started</div>
  <div style="font-size:0.83rem;color:#6B5FA0;line-height:1.7;">
    Works with product reviews · social media posts · support tickets · survey responses · news headlines
  </div>
</div>
""", unsafe_allow_html=True)

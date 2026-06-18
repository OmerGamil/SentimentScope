import streamlit as st
from utils.styles import inject_css


def render_sidebar(tip: str | None = None) -> None:
    st.markdown(inject_css(), unsafe_allow_html=True)
    with st.sidebar:
        st.markdown(
            """
<div style="padding:8px 0 4px;">
  <span style="font-size:1.3rem;font-weight:900;color:#7C3AED;letter-spacing:-0.02em;">
    🎯 SentimentScope
  </span>
  <div style="font-size:0.75rem;color:#9B8FC0;margin-top:4px;letter-spacing:0.03em;">
    Turn text into insight.
  </div>
</div>""",
            unsafe_allow_html=True,
        )
        st.divider()
        if tip:
            st.markdown(tip)
            st.divider()
        st.markdown(
            '<div style="font-size:0.72rem;color:#C4B8E8;letter-spacing:0.05em;">'
            "VADER · TextBlob · RoBERTa</div>",
            unsafe_allow_html=True,
        )

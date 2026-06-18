import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from wordcloud import WordCloud

COLORS = {
    "Positive": "#059669",
    "Neutral":  "#D97706",
    "Negative": "#DC2626",
}
TEMPLATE = "plotly_white"
_LAYOUT = dict(
    template=TEMPLATE,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#1E1433", family="sans-serif"),
)


def pie_chart(df: pd.DataFrame, label_col: str = "vader_label") -> go.Figure:
    counts = df[label_col].value_counts().reset_index()
    counts.columns = ["Sentiment", "Count"]
    fig = px.pie(
        counts,
        values="Count",
        names="Sentiment",
        color="Sentiment",
        color_discrete_map=COLORS,
        title="Sentiment Distribution",
        hole=0.4,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(**_LAYOUT, legend_title="Sentiment")
    return fig


def bar_by_entity(
    df: pd.DataFrame, entity_col: str, label_col: str = "vader_label"
) -> go.Figure:
    top = df[entity_col].value_counts().nlargest(10).index
    filtered = df[df[entity_col].isin(top)]
    grouped = (
        filtered.groupby([entity_col, label_col]).size().reset_index(name="Count")
    )
    fig = px.bar(
        grouped,
        x=entity_col,
        y="Count",
        color=label_col,
        color_discrete_map=COLORS,
        title=f"Sentiment by {entity_col.replace('_', ' ').title()}",
        barmode="group",
        text_auto=True,
    )
    fig.update_layout(**_LAYOUT, xaxis_tickangle=-30)
    return fig


def compound_gauge(compound: float, label: str) -> go.Figure:
    color = COLORS.get(label, "#7C3AED")
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=compound,
            delta={"reference": 0},
            title={"text": f"Compound Score — <b>{label}</b>", "font": {"size": 16, "color": "#1E1433"}},
            number={"font": {"size": 40, "color": "#1E1433"}},
            gauge={
                "axis": {"range": [-1, 1], "tickwidth": 1, "tickcolor": "#9B8FC0"},
                "bar": {"color": color, "thickness": 0.3},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [-1, -0.05], "color": "rgba(220,38,38,0.1)"},
                    {"range": [-0.05, 0.05], "color": "rgba(217,119,6,0.1)"},
                    {"range": [0.05, 1], "color": "rgba(5,150,105,0.1)"},
                ],
                "threshold": {
                    "line": {"color": color, "width": 4},
                    "thickness": 0.75,
                    "value": compound,
                },
            },
        )
    )
    fig.update_layout(**_LAYOUT, height=310, margin=dict(t=90, b=20, l=30, r=30))
    return fig


def score_bars(scores: dict) -> go.Figure:
    categories = ["Positive", "Neutral", "Negative"]
    values = [scores.get("positive", 0), scores.get("neutral", 0), scores.get("negative", 0)]
    fig = go.Figure(
        go.Bar(
            x=categories,
            y=values,
            marker_color=[COLORS[c] for c in categories],
            text=[f"{v:.1%}" for v in values],
            textposition="outside",
        )
    )
    fig.update_layout(
        **_LAYOUT,
        title="Positive / Neutral / Negative Breakdown",
        yaxis=dict(range=[0, 1.15], tickformat=".0%"),
        showlegend=False,
        height=350,
    )
    return fig


def compound_histogram(df: pd.DataFrame) -> go.Figure:
    fig = px.histogram(
        df,
        x="vader_compound",
        color="vader_label",
        color_discrete_map=COLORS,
        nbins=40,
        title="Distribution of Compound Scores",
        labels={"vader_compound": "VADER Compound Score"},
    )
    fig.update_layout(**_LAYOUT, barmode="overlay")
    fig.update_traces(opacity=0.75)
    return fig


def scatter_vader_textblob(df: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        df,
        x="vader_compound",
        y="textblob_polarity",
        color="vader_label",
        color_discrete_map=COLORS,
        opacity=0.65,
        title="VADER Compound vs TextBlob Polarity",
        labels={
            "vader_compound": "VADER Compound Score",
            "textblob_polarity": "TextBlob Polarity",
        },
    )
    fig.add_hline(y=0, line_dash="dash", line_color="#9B8FC0", opacity=0.5)
    fig.add_vline(x=0, line_dash="dash", line_color="#9B8FC0", opacity=0.5)
    fig.update_layout(**_LAYOUT)
    return fig


def time_series_chart(
    df: pd.DataFrame,
    date_col: str,
    compound_col: str = "vader_compound",
) -> "go.Figure | None":
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col]).sort_values(date_col)
    if df.empty:
        return None

    date_range = (df[date_col].max() - df[date_col].min()).days
    if date_range <= 14:
        period, period_label = "D", "Day"
    elif date_range <= 90:
        period, period_label = "W", "Week"
    elif date_range <= 730:
        period, period_label = "ME", "Month"
    else:
        period, period_label = "QE", "Quarter"

    df["_period"] = df[date_col].dt.to_period(period).dt.start_time
    trend = df.groupby("_period")[compound_col].agg(["mean", "count"]).reset_index()
    trend.columns = ["Date", "Avg Compound", "Count"]

    fig = go.Figure()
    fig.add_hrect(y0=0.05, y1=1, fillcolor="#059669", opacity=0.05, line_width=0)
    fig.add_hrect(y0=-1, y1=-0.05, fillcolor="#DC2626", opacity=0.05, line_width=0)
    fig.add_trace(
        go.Scatter(
            x=trend["Date"],
            y=trend["Avg Compound"],
            mode="lines+markers",
            name="Avg VADER Compound",
            line=dict(color="#7C3AED", width=2.5),
            marker=dict(size=7, color="#7C3AED"),
            hovertemplate=(
                "<b>%{x|%b %d, %Y}</b><br>"
                "Avg Compound: %{y:.3f}<br>"
                "Rows: %{customdata}<extra></extra>"
            ),
            customdata=trend["Count"],
        )
    )
    fig.add_hline(y=0.05, line_dash="dot", line_color="#059669", opacity=0.6)
    fig.add_hline(y=-0.05, line_dash="dot", line_color="#DC2626", opacity=0.6)
    fig.add_hline(y=0, line_dash="solid", line_color="#9B8FC0", opacity=0.3)
    fig.update_layout(
        **_LAYOUT,
        title=f"Sentiment Trend Over Time (by {period_label})",
        xaxis_title="Date",
        yaxis_title="Avg VADER Compound Score",
        yaxis=dict(range=[-1, 1]),
        height=400,
    )
    return fig


def generate_wordcloud(texts: list, sentiment: str):
    combined = " ".join([str(t) for t in texts if str(t).strip()])
    if len(combined.split()) < 5:
        return None
    cmap = {"Positive": "Greens", "Neutral": "Oranges", "Negative": "Reds"}.get(
        sentiment, "Purples"
    )
    wc = WordCloud(
        width=800,
        height=380,
        background_color="white",
        colormap=cmap,
        max_words=80,
        collocations=False,
    ).generate(combined)
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    ax.set_title(f"{sentiment}", color="#1E1433", fontsize=13, pad=6)
    fig.patch.set_facecolor("white")
    plt.tight_layout(pad=0.2)
    return fig

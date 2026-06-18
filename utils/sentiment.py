from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import pandas as pd
import nltk

for _resource in ["punkt", "punkt_tab"]:
    try:
        nltk.data.find(f"tokenizers/{_resource}")
    except LookupError:
        nltk.download(_resource, quiet=True)

_analyzer = SentimentIntensityAnalyzer()
_TRANSFORMER_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"


def load_transformer_pipeline():
    from transformers import pipeline as hf_pipeline
    return hf_pipeline(
        "text-classification",
        model=_TRANSFORMER_MODEL,
        top_k=None,
        truncation=True,
        max_length=512,
    )


def _get_label(compound: float) -> str:
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    return "Neutral"


def _get_confidence(compound: float) -> str:
    abs_c = abs(compound)
    if abs_c >= 0.5:
        strength = "Strong"
    elif abs_c >= 0.05:
        strength = "Moderate"
    else:
        return "Neutral"
    return f"{strength} {_get_label(compound)}"


def analyze_transformer(text: str, pipe) -> dict:
    try:
        raw = pipe(str(text)[:512])[0]
        scores = {item["label"].lower(): item["score"] for item in raw}
        neg = scores.get("negative", 0.0)
        neu = scores.get("neutral", 0.0)
        pos = scores.get("positive", 0.0)
        max_score = max(neg, neu, pos)
        if pos == max_score:
            label = "Positive"
        elif neg == max_score:
            label = "Negative"
        else:
            label = "Neutral"
        return {
            "roberta_label": label,
            "roberta_positive": round(pos, 4),
            "roberta_neutral": round(neu, 4),
            "roberta_negative": round(neg, 4),
            "roberta_compound": round(pos - neg, 4),
        }
    except Exception:
        return {
            "roberta_label": "N/A",
            "roberta_positive": None,
            "roberta_neutral": None,
            "roberta_negative": None,
            "roberta_compound": None,
        }


def models_disagree(vader_label: str, roberta_label: str) -> bool:
    """True when VADER and RoBERTa give opposite positive/negative labels."""
    opposites = {("Positive", "Negative"), ("Negative", "Positive")}
    return (vader_label, roberta_label) in opposites


def analyze_text(text: str, pipe=None) -> dict:
    text = str(text)
    scores = _analyzer.polarity_scores(text)
    compound = scores["compound"]
    blob = TextBlob(text)
    result = {
        "compound": round(compound, 4),
        "positive": round(scores["pos"], 4),
        "neutral": round(scores["neu"], 4),
        "negative": round(scores["neg"], 4),
        "label": _get_label(compound),
        "confidence": _get_confidence(compound),
        "textblob_polarity": round(blob.sentiment.polarity, 4),
        "textblob_subjectivity": round(blob.sentiment.subjectivity, 4),
    }
    if pipe is not None:
        roberta = analyze_transformer(text, pipe)
        result.update(roberta)
        result["disagreement"] = models_disagree(result["label"], roberta["roberta_label"])
    return result


def analyze_sentences(text: str, pipe=None) -> list:
    try:
        sentences = nltk.sent_tokenize(str(text))
    except Exception:
        sentences = [s.strip() for s in str(text).split(".") if s.strip()]
    return [{"sentence": s, **analyze_text(s, pipe)} for s in sentences if s.strip()]


def analyze_dataframe(df: pd.DataFrame, text_col: str) -> pd.DataFrame:
    df = df.copy()
    series = df[text_col].fillna("").astype(str)
    results = pd.DataFrame(list(series.apply(analyze_text)))
    df["vader_compound"] = results["compound"].values
    df["vader_positive"] = results["positive"].values
    df["vader_neutral"] = results["neutral"].values
    df["vader_negative"] = results["negative"].values
    df["vader_label"] = results["label"].values
    df["textblob_polarity"] = results["textblob_polarity"].values
    df["textblob_subjectivity"] = results["textblob_subjectivity"].values
    return df

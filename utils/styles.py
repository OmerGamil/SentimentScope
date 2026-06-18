CSS = """
<style>
/* ── Streamlit chrome ──────────────────────────────────────── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 4rem !important;
    max-width: 1100px !important;
}

/* ── Sidebar ────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #EDE9FE !important;
    border-right: 1px solid rgba(124,58,237,0.12) !important;
}

[data-testid="stSidebarNav"] a {
    border-radius: 8px !important;
    font-size: 0.88rem !important;
    padding: 6px 12px !important;
    color: #4B3A7A !important;
    transition: background 0.15s ease !important;
}

[data-testid="stSidebarNav"] a:hover {
    background: rgba(124,58,237,0.1) !important;
    color: #7C3AED !important;
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(124,58,237,0.12) !important;
    border-left: 2px solid #7C3AED !important;
    color: #7C3AED !important;
    font-weight: 600 !important;
}

/* ── Hero ────────────────────────────────────────────────────── */
.ss-hero {
    position: relative;
    background: linear-gradient(160deg, #F0EBFF 0%, #FFFFFF 55%, #F9F7FF 100%);
    border: 1px solid rgba(124,58,237,0.14);
    border-radius: 22px;
    padding: 64px 56px 56px;
    text-align: center;
    overflow: hidden;
    margin-bottom: 36px;
    box-shadow:
        0 4px 24px rgba(124,58,237,0.08),
        0 1px 4px rgba(124,58,237,0.04);
}

.ss-hero::before {
    content: '';
    position: absolute;
    top: -80px; left: 50%;
    transform: translateX(-50%);
    width: 620px; height: 280px;
    background: radial-gradient(ellipse, rgba(124,58,237,0.14) 0%, transparent 70%);
    pointer-events: none;
}

.ss-hero > * { position: relative; z-index: 1; }

.ss-eyebrow {
    display: inline-block;
    background: rgba(124,58,237,0.08);
    border: 1px solid rgba(124,58,237,0.22);
    border-radius: 999px;
    padding: 5px 20px;
    font-size: 0.72rem;
    color: #7C3AED;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 24px;
}

.ss-hero-title {
    font-size: 3.4rem;
    font-weight: 900;
    color: #1E1433;
    margin: 0 0 16px;
    line-height: 1.07;
    letter-spacing: -0.025em;
}

.ss-hero-title .hi {
    background: linear-gradient(130deg, #7C3AED 0%, #A78BFA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.ss-hero-sub {
    display: block;
    font-size: 1.1rem;
    color: #6B5FA0;
    margin: 0 auto;
    max-width: 500px;
    line-height: 1.7;
    text-align: center;
}

/* ── Feature cards ──────────────────────────────────────────── */
.ss-grid-4 {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 40px;
}

.ss-card {
    background: #FFFFFF;
    border: 1px solid rgba(124,58,237,0.1);
    border-radius: 16px;
    padding: 26px 22px;
    box-shadow: 0 2px 10px rgba(124,58,237,0.07), 0 1px 2px rgba(124,58,237,0.04);
}

.ss-card-icon {
    font-size: 1.8rem;
    display: block;
    margin-bottom: 14px;
}

.ss-card-title {
    font-size: 0.98rem;
    font-weight: 700;
    color: #1E1433;
    margin: 0 0 8px;
}

.ss-card-body {
    font-size: 0.83rem;
    color: #6B5FA0;
    line-height: 1.65;
    margin: 0;
}

/* ── Stat cards ─────────────────────────────────────────────── */
.ss-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 32px;
}

.ss-stat {
    background: #FFFFFF;
    border: 1px solid rgba(124,58,237,0.1);
    border-radius: 14px;
    padding: 24px 16px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(124,58,237,0.06);
}

.ss-stat-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.11em;
    color: #9B8FC0;
    margin: 0 0 10px;
}

.ss-stat-value {
    font-size: 2.6rem;
    font-weight: 900;
    line-height: 1;
    margin: 0 0 6px;
    letter-spacing: -0.03em;
}

.ss-stat-pct {
    font-size: 0.8rem;
    font-weight: 700;
    opacity: 0.75;
}

/* ── Steps ─────────────────────────────────────────────────── */
.ss-steps {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin-top: 8px;
}

.ss-step {
    background: #FFFFFF;
    border: 1px solid rgba(124,58,237,0.09);
    border-radius: 12px;
    padding: 18px;
    display: flex;
    align-items: flex-start;
    gap: 14px;
    box-shadow: 0 1px 4px rgba(124,58,237,0.05);
}

.ss-step-num {
    min-width: 28px;
    height: 28px;
    background: rgba(124,58,237,0.08);
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 7px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.78rem;
    font-weight: 800;
    color: #7C3AED;
    flex-shrink: 0;
}

.ss-step h4 {
    font-size: 0.87rem;
    font-weight: 700;
    color: #1E1433;
    margin: 0 0 4px;
}

.ss-step p {
    font-size: 0.79rem;
    color: #6B5FA0;
    line-height: 1.55;
    margin: 0;
}

/* ── Section header ─────────────────────────────────────────── */
.ss-sec {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 40px 0 18px;
}

.ss-sec h3 {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1E1433;
    margin: 0;
    white-space: nowrap;
}

.ss-sec-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(124,58,237,0.22) 0%, transparent 100%);
}

/* ── Page header ────────────────────────────────────────────── */
.ss-page-head {
    margin-bottom: 32px;
    padding-bottom: 22px;
    border-bottom: 1px solid rgba(124,58,237,0.1);
}

.ss-page-head h1 {
    font-size: 2rem;
    font-weight: 800;
    color: #1E1433;
    margin: 0 0 6px;
    letter-spacing: -0.015em;
}

.ss-page-head p {
    font-size: 0.9rem;
    color: #6B5FA0;
    margin: 0;
}

/* ── Divider ────────────────────────────────────────────────── */
.ss-divider {
    height: 1px;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(124,58,237,0.14) 25%,
        rgba(124,58,237,0.14) 75%,
        transparent 100%);
    margin: 38px 0;
}

/* ── Sentiment badges ───────────────────────────────────────── */
.ss-badges {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin: 14px 0 26px;
}

.ss-badge {
    display: flex;
    flex-direction: column;
    border-radius: 14px;
    padding: 16px 28px;
    border-width: 1px;
    border-style: solid;
    min-width: 150px;
    background: #FFFFFF;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.ss-badge-model {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    opacity: 0.6;
    font-weight: 700;
    margin-bottom: 5px;
}

.ss-badge-label { font-size: 1.2rem; font-weight: 800; }
.ss-badge-score { font-size: 0.78rem; opacity: 0.65; margin-top: 3px; font-weight: 600; }

/* ── Disagree banner ────────────────────────────────────────── */
.ss-disagree {
    background: #FFFBEB;
    border: 1px solid rgba(217,119,6,0.22);
    border-left: 3px solid #D97706;
    border-radius: 10px;
    padding: 14px 18px 14px 16px;
    margin: 8px 0 20px;
    font-size: 0.88rem;
    line-height: 1.6;
    color: #78350F;
}

.ss-disagree strong { color: #B45309; }

/* ── Native Streamlit overrides ─────────────────────────────── */

[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 14px rgba(124,58,237,0.32) !important;
    transition: box-shadow 0.2s ease, transform 0.15s ease !important;
}

[data-testid="baseButton-primary"]:hover {
    box-shadow: 0 6px 22px rgba(124,58,237,0.48) !important;
    transform: translateY(-1px) !important;
}

[data-testid="baseButton-secondary"] {
    background: #FFFFFF !important;
    border: 1px solid rgba(124,58,237,0.22) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    color: #7C3AED !important;
    transition: background 0.15s ease, border-color 0.15s ease !important;
}

[data-testid="baseButton-secondary"]:hover {
    background: rgba(124,58,237,0.04) !important;
    border-color: rgba(124,58,237,0.38) !important;
}

[data-testid="stTextArea"] textarea {
    background: #FFFFFF !important;
    border: 1px solid rgba(124,58,237,0.16) !important;
    border-radius: 12px !important;
    color: #1E1433 !important;
}

[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(124,58,237,0.42) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.08) !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 1px solid rgba(124,58,237,0.16) !important;
    border-radius: 10px !important;
}

[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid rgba(124,58,237,0.1) !important;
    border-radius: 12px !important;
    padding: 18px 20px !important;
    box-shadow: 0 2px 8px rgba(124,58,237,0.05) !important;
}

[data-testid="stMetricValue"] {
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
    color: #1E1433 !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: #9B8FC0 !important;
}

[data-testid="stFileUploadDropzone"] {
    background: rgba(124,58,237,0.03) !important;
    border: 1.5px dashed rgba(124,58,237,0.22) !important;
    border-radius: 14px !important;
    transition: border-color 0.2s ease, background 0.2s ease !important;
}

[data-testid="stFileUploadDropzone"]:hover {
    background: rgba(124,58,237,0.06) !important;
    border-color: rgba(124,58,237,0.38) !important;
}

[data-testid="stExpander"] details {
    background: rgba(255,255,255,0.85) !important;
    border: 1px solid rgba(124,58,237,0.1) !important;
    border-radius: 10px !important;
}

[data-testid="stDataFrame"] > div {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid rgba(124,58,237,0.1) !important;
}

[data-testid="stCheckbox"] {
    background: rgba(124,58,237,0.04) !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    border: 1px solid rgba(124,58,237,0.08) !important;
}

[data-testid="stAlert"] { border-radius: 10px !important; }
</style>
"""


def inject_css() -> str:
    return CSS


def hero(eyebrow: str, title: str, accent: str, subtitle: str) -> str:
    return f"""
<div style="position:relative;background:linear-gradient(160deg,#F0EBFF 0%,#FFFFFF 55%,#F9F7FF 100%);border:1px solid rgba(124,58,237,0.14);border-radius:22px;padding:64px 56px 56px;text-align:center;overflow:hidden;margin-bottom:36px;box-shadow:0 4px 24px rgba(124,58,237,0.08),0 1px 4px rgba(124,58,237,0.04);">
  <div style="position:absolute;top:-80px;left:50%;transform:translateX(-50%);width:620px;height:280px;background:radial-gradient(ellipse,rgba(124,58,237,0.14) 0%,transparent 70%);pointer-events:none;"></div>
  <div style="position:relative;z-index:1;">
    <div style="display:inline-block;background:rgba(124,58,237,0.08);border:1px solid rgba(124,58,237,0.22);border-radius:999px;padding:5px 20px;font-size:0.72rem;color:#7C3AED;letter-spacing:0.14em;text-transform:uppercase;font-weight:700;margin-bottom:24px;">{eyebrow}</div>
    <h1 style="font-size:3.4rem;font-weight:900;color:#1E1433;margin:0 0 16px;line-height:1.07;letter-spacing:-0.025em;">{title} <span style="background:linear-gradient(130deg,#7C3AED 0%,#A78BFA 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{accent}</span></h1>
    <div style="font-size:1.1rem;color:#6B5FA0;line-height:1.7;margin:0 !important;text-align:center !important;">{subtitle}</div>
  </div>
</div>"""


def feature_cards(*cards) -> str:
    inner = "".join(
        f"""<div class="ss-card">
  <span class="ss-card-icon">{icon}</span>
  <p class="ss-card-title">{title}</p>
  <p class="ss-card-body">{body}</p>
</div>"""
        for icon, title, body in cards
    )
    return f'<div class="ss-grid-4">{inner}</div>'


def step_cards(*steps) -> str:
    inner = "".join(
        f"""<div class="ss-step">
  <div class="ss-step-num">{i + 1}</div>
  <div><h4>{title}</h4><p>{desc}</p></div>
</div>"""
        for i, (title, desc) in enumerate(steps)
    )
    return f'<div class="ss-steps">{inner}</div>'


def stats(total: int, pos: int, neu: int, neg: int) -> str:
    pct = lambda n: f"{n / total:.0%}" if total else "—"
    C = {"total": "#7C3AED", "pos": "#059669", "neu": "#D97706", "neg": "#DC2626"}
    return f"""
<div class="ss-stats">
  <div class="ss-stat">
    <div class="ss-stat-label">Total</div>
    <div class="ss-stat-value" style="color:{C['total']}">{total:,}</div>
  </div>
  <div class="ss-stat">
    <div class="ss-stat-label">Positive</div>
    <div class="ss-stat-value" style="color:{C['pos']}">{pos:,}</div>
    <div class="ss-stat-pct" style="color:{C['pos']}">{pct(pos)}</div>
  </div>
  <div class="ss-stat">
    <div class="ss-stat-label">Neutral</div>
    <div class="ss-stat-value" style="color:{C['neu']}">{neu:,}</div>
    <div class="ss-stat-pct" style="color:{C['neu']}">{pct(neu)}</div>
  </div>
  <div class="ss-stat">
    <div class="ss-stat-label">Negative</div>
    <div class="ss-stat-value" style="color:{C['neg']}">{neg:,}</div>
    <div class="ss-stat-pct" style="color:{C['neg']}">{pct(neg)}</div>
  </div>
</div>"""


def section(title: str) -> str:
    return f"""
<div class="ss-sec">
  <h3>{title}</h3>
  <div class="ss-sec-line"></div>
</div>"""


def page_header(title: str, caption: str) -> str:
    return f"""
<div class="ss-page-head">
  <h1>{title}</h1>
  <p>{caption}</p>
</div>"""


def divider() -> str:
    return '<div class="ss-divider"></div>'


def badges(
    label: str, confidence: str, compound: float,
    roberta_label: str | None = None,
    roberta_compound: float | None = None,
) -> str:
    C = {"Positive": "#059669", "Neutral": "#D97706", "Negative": "#DC2626"}
    c = C.get(label, "#7C3AED")
    b1 = f"""
<div class="ss-badge" style="border-color:{c}40;color:{c}">
  <span class="ss-badge-model">VADER</span>
  <span class="ss-badge-label">{confidence}</span>
  <span class="ss-badge-score">{compound:+.4f}</span>
</div>"""
    b2 = ""
    if roberta_label and roberta_label != "N/A":
        rc = C.get(roberta_label, "#7C3AED")
        b2 = f"""
<div class="ss-badge" style="border-color:{rc}40;color:{rc}">
  <span class="ss-badge-model">RoBERTa</span>
  <span class="ss-badge-label">{roberta_label}</span>
  <span class="ss-badge-score">{roberta_compound:+.4f}</span>
</div>"""
    return f'<div class="ss-badges">{b1}{b2}</div>'


def disagree_banner(vader: str, roberta: str) -> str:
    return f"""
<div class="ss-disagree">
  ⚠️ <strong>Models disagree</strong> — VADER reads this as <strong>{vader}</strong>
  but RoBERTa reads it as <strong>{roberta}</strong>.
  The text may contain sarcasm, irony, or domain-specific language — RoBERTa is generally more reliable here.
</div>"""

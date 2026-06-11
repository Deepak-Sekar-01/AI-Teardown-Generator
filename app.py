import streamlit as st
import time
from search import get_research
from teardown import generate_teardown

st.set_page_config(
    page_title="AI Product Teardown Generator",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* ── Base ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: #0A0A0A;
        color: #F0F0F0;
    }

    /* ── Hide Streamlit chrome ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 60px !important;
        padding-left: 10% !important;
        padding-right: 10% !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
    }
    /* ── Layout wrapper ── */
    .wrapper {
        max-width: 1100px;
        margin: 0 auto;
        padding: 60px 40px 80px 40px;
    }

    /* ── Header ── */
    .header-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 3px;
        color: #00C896;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .header-title {
        font-size: 36px;
        font-weight: 700;
        color: #F0F0F0;
        margin: 0 0 8px 0;
        line-height: 1.2;
    }

    .header-sub {
        font-size: 15px;
        color: #666666;
        margin: 0 0 48px 0;
        font-weight: 400;
    }

    /* ── Divider ── */
    .divider {
        height: 1px;
        background: #1E1E1E;
        margin: 40px 0;
    }

    /* ── Pipeline tracker ── */
    .pipeline {
        display: flex;
        gap: 8px;
        align-items: center;
        margin: 32px 0;
        flex-wrap: wrap;
    }

    .stage {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        padding: 6px 14px;
        border-radius: 2px;
        color: #444444;
        background: #111111;
        border: 1px solid #1E1E1E;
        transition: all 0.3s ease;
    }

    .stage.active {
        color: #00C896;
        border-color: #00C896;
        background: #00C89610;
    }

    .stage.done {
        color: #F0F0F0;
        border-color: #333333;
        background: #141414;
    }

    .stage-arrow {
        color: #333333;
        font-size: 12px;
    }

    /* ── Cards grid ── */
    .cards-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-bottom: 16px;
    }

    .card {
        background: #141414;
        border: 1px solid #1E1E1E;
        border-radius: 4px;
        padding: 24px 24px 24px 20px;
        border-left-width: 3px;
    }

    .card-label {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .card-body {
        font-size: 14px;
        line-height: 1.7;
        color: #CCCCCC;
        font-weight: 400;
    }

    /* ── Card accent colors ── */
    .card-problem    { border-left-color: #FF6B6B; }
    .card-problem    .card-label { color: #FF6B6B; }

    .card-rootcause  { border-left-color: #FFB347; }
    .card-rootcause  .card-label { color: #FFB347; }

    .card-userimpact { border-left-color: #5B9BD5; }
    .card-userimpact .card-label { color: #5B9BD5; }

    .card-bizcost    { border-left-color: #C084FC; }
    .card-bizcost    .card-label { color: #C084FC; }

    /* ── Recommendation card (full width) ── */
    .card-rec {
        background: #141414;
        border: 1px solid #1E1E1E;
        border-left: 3px solid #00C896;
        border-radius: 4px;
        padding: 24px 24px 24px 20px;
        margin-bottom: 16px;
    }

    .card-rec .card-label { color: #00C896; }

    /* ── Confidence note ── */
    .confidence {
        font-size: 12px;
        color: #555555;
        margin-top: 16px;
        padding-top: 16px;
        border-top: 1px solid #1E1E1E;
        font-style: italic;
    }

    /* ── Sources ── */
    .sources-header {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #444444;
        margin-bottom: 12px;
    }

    .source-item {
        font-size: 13px;
        color: #555555;
        padding: 8px 0;
        border-bottom: 1px solid #1A1A1A;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .source-item a {
        color: #00C896;
        text-decoration: none;
        font-size: 11px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    /* ── Input overrides ── */
    .stTextInput input {
        background: #111111 !important;
        border: 1px solid #2A2A2A !important;
        border-radius: 4px !important;
        color: #F0F0F0 !important;
        font-size: 15px !important;
        padding: 14px 16px !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stTextInput input:focus {
        border-color: #00C896 !important;
        box-shadow: none !important;
    }

    .stTextInput input::placeholder {
        color: #444444 !important;
    }

    /* ── Button override ── */
    .stButton button {
        background: #00C896 !important;
        color: #0A0A0A !important;
        border: none !important;
        border-radius: 4px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        padding: 14px 32px !important;
        font-family: 'Inter', sans-serif !important;
        width: 100% !important;
        cursor: pointer !important;
    }

    .stButton button:hover {
        background: #00B384 !important;
    }

    /* ── App name display ── */
    .app-name-tag {
        display: inline-block;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #0A0A0A;
        background: #00C896;
        padding: 4px 12px;
        border-radius: 2px;
        margin-bottom: 24px;
    }
</style>
""", unsafe_allow_html=True)


def render_pipeline(stage):
    stages = ["Searching", "Compiling", "Analyzing", "Complete"]
    html = '<div class="pipeline">'
    for i, s in enumerate(stages):
        if s == stage:
            css = "stage active"
        elif stages.index(stage) > i:
            css = "stage done"
        else:
            css = "stage"
        html += f'<span class="{css}">{s}</span>'
        if i < len(stages) - 1:
            html += '<span class="stage-arrow">›</span>'
    html += '</div>'
    return html


def render_results(teardown, sources):
    app = teardown.get("app_name", "")
    st.markdown(f'<div class="app-name-tag">{app}</div>', unsafe_allow_html=True)

    # ADD THIS BLOCK:
    st.markdown(f"""
    <div style="background:#141414; border:1px solid #1E1E1E; border-radius:4px; 
        padding:24px; margin-bottom:16px;">
        <div class="card-label" style="color:#A0A0A0; margin-bottom:12px;">Overview</div>
            <div class="card-body">{teardown.get("description", "")}</div>
    </div>
    """, unsafe_allow_html=True)
    # 2-column card grid
    st.markdown(f"""
    <div class="cards-grid">
        <div class="card card-problem">
            <div class="card-label">Problem</div>
            <div class="card-body">{teardown.get("problem", "")}</div>
        </div>
        <div class="card card-rootcause">
            <div class="card-label">Root Cause</div>
            <div class="card-body">{teardown.get("root_cause", "")}</div>
        </div>
        <div class="card card-userimpact">
            <div class="card-label">User Impact</div>
            <div class="card-body">{teardown.get("user_impact", "")}</div>
        </div>
        <div class="card card-bizcost">
            <div class="card-label">Business Cost</div>
            <div class="card-body">{teardown.get("business_cost", "")}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Recommendation (full width)
    st.markdown(f"""
    <div class="card-rec">
        <div class="card-label">Recommendation</div>
        <div class="card-body">{teardown.get("recommendation", "")}</div>
        <div class="confidence">{teardown.get("confidence_note", "")}</div>
    </div>
    """, unsafe_allow_html=True)

    # Sources
    with st.expander("Sources"):
        for s in sources:
            st.markdown(f"""
            <div class="source-item">
                <span>{s['title']}</span>
                <a href="{s['url']}" target="_blank">View</a>
            </div>
            """, unsafe_allow_html=True)


# ── Main app ──

st.markdown("""
    <h1 class="header-title">AI Product Teardown Generator</h1>
    <p class="header-sub">Enter any digital product. Get a structured teardown backed by live research.</p>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])
with col1:
    app_input = st.text_input(
        label="app_input",
        placeholder="e.g. Swiggy, Notion, Figma, PhonePe...",
        label_visibility="collapsed"
    )
with col2:
    analyze = st.button("Analyze")

if analyze and app_input.strip():
    pipeline_slot = st.empty()
    results_slot  = st.empty()

    # Stage 1 — Searching
    pipeline_slot.markdown(render_pipeline("Searching"), unsafe_allow_html=True)
    research, sources = get_research(app_input.strip())

    if research is None:
        pipeline_slot.empty()
        st.markdown(
            '<p style="color:#FF6B6B; font-size:14px; margin-top:16px;">Could not verify this product. Try a well-known digital product like Swiggy, Notion, or Netflix.</p>',
            unsafe_allow_html=True
        )
        st.stop()

    # Stage 2 — Compiling
    pipeline_slot.markdown(render_pipeline("Compiling"), unsafe_allow_html=True)
    time.sleep(0.5)

    # Stage 3 — Analyzing
    pipeline_slot.markdown(render_pipeline("Analyzing"), unsafe_allow_html=True)
    teardown = generate_teardown(app_input.strip(), research)

    # Stage 4 — Complete
    pipeline_slot.markdown(render_pipeline("Complete"), unsafe_allow_html=True)

    with results_slot.container():
        render_results(teardown, sources)

elif analyze and not app_input.strip():
    st.markdown(
        '<p style="color:#FF6B6B; font-size:13px; margin-top:8px;">Enter an app name first.</p>',
        unsafe_allow_html=True
    )

import streamlit as st
from google import genai

st.set_page_config(page_title="AI Marketing Strategy Studio", page_icon="🎯", layout="wide")

st.markdown("""
<style>
:root { --ink:#eef2ff; --muted:#a8b3cc; --panel:#111a2e; --line:#273653; --accent:#8b5cf6; }
.stApp { background: radial-gradient(ellipse at 15% 0%, #1d2450 0%, #0b1020 43%, #080d19 100%); color:var(--ink); }
.block-container { max-width:1240px; padding-top:1.8rem; padding-bottom:3rem; }
#MainMenu, footer { visibility:hidden; }
.hero { position:relative; overflow:hidden; padding:2rem 2.1rem; border-radius:22px; background:linear-gradient(115deg,rgba(91,52,173,.42),rgba(25,49,92,.72)); border:1px solid rgba(167,139,250,.3); margin-bottom:1.25rem; box-shadow:0 18px 55px rgba(0,0,0,.18); }
.hero:after { content:'✦'; position:absolute; right:6%; top:4%; font-size:5rem; color:rgba(221,214,254,.12); }
.eyebrow { color:#c4b5fd; font-size:.76rem; font-weight:700; letter-spacing:.16em; text-transform:uppercase; margin-bottom:.55rem; }
.hero h1 { margin:0; color:#fff; font-size:2.25rem; letter-spacing:-.04em; }
.hero p { color:#dbe4ff; margin:.65rem 0 0; font-size:1rem; max-width:760px; }
.section-title { font-size:1.08rem; font-weight:700; color:#f1f5ff; margin:.7rem 0 .2rem; }
.section-subtitle { color:var(--muted); font-size:.88rem; margin-bottom:1rem; }
div[data-testid="stMetric"] { background:linear-gradient(145deg,rgba(20,31,54,.96),rgba(15,23,42,.96)); border:1px solid var(--line); padding:1.05rem 1.15rem; border-radius:16px; box-shadow:0 8px 24px rgba(0,0,0,.12); }
div[data-testid="stMetricLabel"] { color:#aebbd5; }
div[data-testid="stMetricValue"] { color:#f5f3ff; }
section[data-testid="stSidebar"] { background:#0c1425; border-right:1px solid #24324b; }
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 { color:#f5f3ff; }
.stButton button[kind="primary"] { border:0; border-radius:11px; background:linear-gradient(100deg,#7c3aed,#6366f1); font-weight:700; min-height:2.8rem; box-shadow:0 8px 22px rgba(99,102,241,.2); }
.stButton button[kind="primary"]:hover { border:0; background:linear-gradient(100deg,#6d28d9,#4f46e5); }
.stTextInput input, .stNumberInput input, .stTextArea textarea, div[data-baseweb="select"] > div { border-radius:10px; }
.stTabs [data-baseweb="tab-list"] { gap:8px; }
.stTabs [data-baseweb="tab"] { background:#111a2e; border:1px solid #273653; border-radius:10px 10px 0 0; padding: .65rem 1rem; }
.workflow-card { background:rgba(17,26,46,.88); border:1px solid #273653; border-radius:16px; padding:1.15rem; height:100%; }
.workflow-number { display:inline-flex; width:32px; height:32px; align-items:center; justify-content:center; border-radius:10px; background:#30215d; color:#ddd6fe; font-weight:800; margin-bottom:.7rem; }
.workflow-card h4 { margin:.1rem 0 .45rem; color:#f5f3ff; font-size:1rem; }
.workflow-card p { color:#aebbd5; font-size:.88rem; margin:0; line-height:1.5; }
div[data-testid="stAlert"] { border-radius:12px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="eyebrow">Agentic AI · Campaign workspace</div>
  <h1>AI Marketing Strategy Studio</h1>
  <p>Turn a product idea into a structured campaign plan and ready-to-edit marketing content — with two AI steps working in sequence.</p>
</div>
""", unsafe_allow_html=True)



with st.sidebar:
    st.markdown("### 🎯 Campaign setup")
    st.caption("Configure your product and campaign before generating a plan.")
    product = st.text_input("Product", "Lightweight water bottle")
    audience = st.text_input("Target audience", "School children aged 6–16, with parents/guardians as purchasers")
    budget = st.number_input("Marketing budget (USD)", min_value=100, max_value=1_000_000, value=2000, step=100)
    market = st.text_input("Market / location", "United States")
    goal = st.selectbox("Main campaign goal", ["Increase awareness", "Drive online sales", "Generate website traffic", "Build social media engagement", "Promote a product launch"])
    tone = st.selectbox("Content tone", ["Fun and friendly", "Educational", "Energetic", "Premium", "Eco-conscious"])
    extra = st.text_area("Extra details (optional)", placeholder="Price, product features, available channels, campaign dates…")
    run = st.button("Generate campaign", type="primary", use_container_width=True)

if run:
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        st.error("Gemini API key is missing. Add GEMINI_API_KEY under Streamlit Cloud → App settings → Secrets.")
        st.stop()
    if not product.strip() or not audience.strip():
        st.warning("Please enter both a product and target audience.")
        st.stop()

    client = genai.Client(api_key=api_key)
    model = "gemini-2.5-flash"

    strategy_prompt = f"""You are Agent 1, the Marketing Strategist, in a sequential AI workflow.
Create a practical marketing plan from these details:
Product: {product}
Target audience: {audience}
Budget: USD {budget}
Market: {market}
Campaign goal: {goal}
Extra details: {extra or 'Not provided'}

Include: (1) campaign objective and audience insight, (2) 3–5 marketing channels with reasons,
(3) a budget allocation that adds up exactly to USD {budget}, (4) a four-week timeline,
(5) measurable KPIs, (6) assumptions and risks. Do not guarantee results. If the audience includes
minors, consider child privacy and avoid manipulative pressure; distinguish children from adult purchasers.
"""

    with st.spinner("Agent 1 — developing the marketing strategy…"):
        try:
            response1 = client.models.generate_content(model=model, contents=strategy_prompt)
            strategy = response1.text or "No strategy was returned. Please try again."
        except Exception as exc:
            st.error(f"Strategy generation failed: {exc}")
            st.stop()

    content_prompt = f"""You are Agent 2, the Content Creator. You MUST use the strategy from Agent 1 below.
Product: {product}
Target audience: {audience}
Market: {market}
Tone: {tone}
Campaign goal: {goal}

Create: 3 short social posts with calls to action; one 15–20 second Reel/video concept and script;
2 tagline/headline options; one message aimed at parents/guardians; and a note explaining which channel
fits each item. Keep claims truthful and do not invent product features or unsupported health/environmental claims.
Because children may be part of the audience, avoid manipulative pressure and do not ask children to share personal data.

STRATEGY FROM AGENT 1:
{strategy}
"""
    with st.spinner("Agent 2 — creating content based on the strategy…"):
        try:
            response2 = client.models.generate_content(model=model, contents=content_prompt)
            content = response2.text or "No content was returned. Please try again."
        except Exception as exc:
            st.error(f"Content generation failed: {exc}")
            st.stop()

    st.success("Campaign generated.")
    tab1, tab2, tab3 = st.tabs(["📊 Strategy", "✍️ Content", "📥 Export report"])
    with tab1:
        st.markdown(strategy)
    with tab2:
        st.markdown(content)
    with tab3:
        report = f"# AI Marketing Campaign\n\n## Campaign details\n- Product: {product}\n- Target audience: {audience}\n- Budget: USD {budget}\n- Market: {market}\n- Goal: {goal}\n\n## Agent 1 — Marketing Strategy\n\n{strategy}\n\n## Agent 2 — Content Creator\n\n{content}\n"
        st.download_button("Download campaign report (.md)", data=report, file_name="ai_marketing_campaign.md", mime="text/markdown")
else:
    a, b, c = st.columns(3)
    a.metric("AI agents", "02", "Strategy + content")
    b.metric("Campaign workflow", "Sequential", "Output from Agent 1 feeds Agent 2")
    c.metric("Sample budget", "$2,000", "Editable for your campaign")

    st.markdown('<div class="section-title">Your campaign workflow</div><div class="section-subtitle">Three clear steps from campaign brief to downloadable report.</div>', unsafe_allow_html=True)
    w1, w2, w3 = st.columns(3, gap="medium")
    with w1:
        st.markdown('<div class="workflow-card"><div class="workflow-number">01</div><h4>Define the brief</h4><p>Enter the product, audience, market, budget and campaign goal in the sidebar.</p></div>', unsafe_allow_html=True)
    with w2:
        st.markdown('<div class="workflow-card"><div class="workflow-number">02</div><h4>Generate with AI agents</h4><p>The Marketing Strategist drafts the plan. The Content Creator then builds content using that plan.</p></div>', unsafe_allow_html=True)
    with w3:
        st.markdown('<div class="workflow-card"><div class="workflow-number">03</div><h4>Review and export</h4><p>Review the strategy and content, make edits as needed, and download the campaign report.</p></div>', unsafe_allow_html=True)

    st.markdown("### Start with the sample campaign")
    st.markdown("Use the pre-filled lightweight water bottle example or change the details in the sidebar to suit your own product.")
    st.info("AI outputs are suggestions, not guaranteed results. Review budget assumptions and all campaign claims before using them. For audiences that include children, consider privacy and age-appropriate advertising.")

st.divider()
st.caption("AI MARKETING STRATEGY STUDIO  ·  PYTHON  /  STREAMLIT  /  GOOGLE GEMINI")

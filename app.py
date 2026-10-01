
import streamlit as st
import time
from google import genai
from google.genai import types


# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="AI Marketing Strategy Studio",
    page_icon="🎯",
    layout="wide"
)


# ==================================================
# PROFESSIONAL DARK THEME
# ==================================================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(
        ellipse at top left,
        #20264a 0%,
        #0b1020 48%,
        #080d19 100%
    );
    color: #f4f6ff;
}

.block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

header[data-testid="stHeader"] {
    background: rgba(8, 13, 25, 0.95);
}

#MainMenu, footer {
    visibility: hidden;
}

.hero {
    padding: 30px;
    border-radius: 22px;
    margin-bottom: 25px;
    background: linear-gradient(
        115deg,
        rgba(91, 52, 173, 0.48),
        rgba(25, 49, 92, 0.78)
    );
    border: 1px solid rgba(167, 139, 250, 0.35);
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
}

.hero-label {
    color: #c4b5fd;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero h1 {
    color: #ffffff;
    font-size: 36px;
    margin: 10px 0;
}

.hero p {
    color: #e0e7ff;
    font-size: 16px;
    line-height: 1.7;
}

section[data-testid="stSidebar"] {
    background: #0e172b;
    border-right: 1px solid #293752;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: #edf2ff !important;
}

.stMarkdown p,
.stMarkdown li,
.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3,
.stMarkdown h4 {
    color: #edf2ff;
}

[data-testid="stCaptionContainer"] p {
    color: #b8c5dd !important;
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
div[data-baseweb="select"] > div {
    background: #121d32 !important;
    color: #f4f6ff !important;
    border: 1px solid #344563 !important;
    border-radius: 10px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #8796b2 !important;
}

.stButton button[kind="primary"] {
    background: linear-gradient(100deg, #7c3aed, #6366f1);
    color: #ffffff;
    border: 1px solid #8b78ef;
    border-radius: 11px;
    font-weight: 700;
    min-height: 44px;
}

.stButton button[kind="primary"]:hover {
    background: linear-gradient(100deg, #6d28d9, #4f46e5);
    border-color: #c4b5fd;
}

.stDownloadButton button {
    background: #211a3b;
    color: #f4f0ff;
    border: 1px solid #6750a4;
    border-radius: 10px;
}

div[data-testid="stMetric"] {
    background: #111a2e;
    border: 1px solid #2b3a59;
    padding: 16px;
    border-radius: 15px;
}

div[data-testid="stMetricLabel"] p {
    color: #bdc9e1 !important;
}

div[data-testid="stMetricValue"] {
    color: #ffffff !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background: #111a2e;
    color: #e2e8f0;
    border-radius: 8px;
}

.stTabs [aria-selected="true"] {
    background: #352567 !important;
    color: #ffffff !important;
}

.workflow-card {
    background: #111a2e;
    border: 1px solid #2b3a59;
    border-radius: 15px;
    padding: 20px;
    min-height: 165px;
}

.workflow-card h4 {
    color: #f5f3ff;
}

.workflow-card p {
    color: #b8c5dd;
    font-size: 14px;
    line-height: 1.6;
}

.workflow-number {
    color: #d8ccff;
    font-weight: 800;
    font-size: 20px;
}

hr {
    border-color: #293752 !important;
}

@media (max-width: 700px) {
    .hero h1 {
        font-size: 27px;
    }

    .hero {
        padding: 20px;
    }
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# GEMINI SETTINGS
# ==================================================
MODEL_NAME = "gemini-3.8-flash"
MAX_ATTEMPTS = 2


def generate_with_retry(client, prompt):
    """Generate content with retry for temporary errors."""

    for attempt in range(MAX_ATTEMPTS):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.5,
                    max_output_tokens=1800
                )
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty response. Please retry."
                )

            return response.text

        except Exception as exc:
            error_text = str(exc).upper()

            temporary_error = any(
                code in error_text
                for code in [
                    "503",
                    "UNAVAILABLE",
                    "429",
                    "RESOURCE_EXHAUSTED",
                    "500",
                    "502",
                    "504",
                    "DEADLINE_EXCEEDED",
                    "INTERNAL"
                ]
            )

            if not temporary_error or attempt == MAX_ATTEMPTS - 1:
                raise

            # Wait before the final retry.
            time.sleep(4)

    raise RuntimeError("Unable to generate a response.")


# ==================================================
# HERO
# ==================================================
st.markdown("""
<div class="hero">
    <div class="hero-label">
        Agentic AI | Campaign workspace
    </div>
    <h1>AI Marketing Strategy Studio</h1>
    <p>
        Transform your product idea into a marketing strategy
        and ready-to-edit content using two AI agents working
        in sequence.
    </p>
</div>
""", unsafe_allow_html=True)


# ==================================================
# SIDEBAR INPUTS
# ==================================================
with st.sidebar:
    st.markdown("## Campaign Setup")
    st.caption("Enter your campaign details below.")

    with st.form("campaign_form"):
        product = st.text_input(
            "Product",
            value="Lightweight water bottle"
        )

        audience = st.text_input(
            "Target audience",
            value=(
                "School children aged 6-16, "
                "with parents or guardians as purchasers"
            )
        )

        budget = st.number_input(
            "Marketing budget (USD)",
            min_value=100,
            max_value=1000000,
            value=2000,
            step=100
        )

        market = st.text_input(
            "Market / Location",
            value="United States"
        )

        goal = st.selectbox(
            "Campaign goal",
            [
                "Increase awareness",
                "Drive online sales",
                "Generate website traffic",
                "Build social media engagement",
                "Promote a product launch"
            ]
        )

        tone = st.selectbox(
            "Content tone",
            [
                "Fun and friendly",
                "Educational",
                "Energetic",
                "Professional",
                "Premium"
            ]
        )

        extra = st.text_area(
            "Extra details (optional)",
            placeholder="Product price, features, dates..."
        )

        generate_button = st.form_submit_button(
            "Generate Campaign",
            type="primary",
            use_container_width=True
        )


# ==================================================
# SESSION STATE
# ==================================================
if "strategy" not in st.session_state:
    st.session_state.strategy = ""

if "content" not in st.session_state:
    st.session_state.content = ""

if "campaign_report" not in st.session_state:
    st.session_state.campaign_report = ""


# ==================================================
# GENERATE CAMPAIGN
# ==================================================
if generate_button:

    if not product.strip() or not audience.strip():
        st.error("Please enter the product and target audience.")

    else:
        api_key = st.secrets.get("GEMINI_API_KEY", "")

        if not api_key:
            st.error(
                "GEMINI_API_KEY is missing. Add it under "
                "Streamlit Cloud Settings, then Secrets."
            )

        else:
            client = genai.Client(
                api_key=api_key,
                http_options=types.HttpOptions(
                    timeout=90000
                )
            )

            # ------------------------------------------
            # AGENT 1: MARKETING STRATEGIST
            # ------------------------------------------
            strategy_prompt = f"""
You are Agent 1, a marketing strategist.

Create a concise, practical marketing strategy.

Product: {product}
Target audience: {audience}
Budget: USD {budget}
Market: {market}
Campaign goal: {goal}
Content tone: {tone}
Extra details: {extra or "None"}

Include:
1. Campaign objective and audience insight.
2. Four marketing channels with reasons.
3. Budget allocation totaling exactly USD {budget}.
4. A four-week campaign timeline.
5. Five measurable KPIs.
6. Three risks and practical solutions.

Use clear headings and Markdown tables.
Keep the response under 600 words.
Do not guarantee campaign results.
Do not invent product features.
If children are in the audience, consider child privacy
and use age-appropriate, non-manipulative marketing.
"""

            st.session_state.strategy = ""
            st.session_state.content = ""
            st.session_state.campaign_report = ""

            with st.spinner(
                "Agent 1 is developing the marketing strategy..."
            ):
                try:
                    strategy = generate_with_retry(
                        client,
                        strategy_prompt
                    )

                    st.session_state.strategy = strategy

                except Exception as exc:
                    st.error(
                        "Strategy generation failed: "
                        + str(exc)
                    )

                    error_text = str(exc).upper()

                    if "503" in error_text or "UNAVAILABLE" in error_text:
                        st.warning(
                            "Gemini is temporarily overloaded. "
                            "Wait a little and try again."
                        )

                    elif (
                        "429" in error_text
                        or "RESOURCE_EXHAUSTED" in error_text
                    ):
                        st.warning(
                            "The Gemini API rate limit or quota "
                            "has been reached. Check your API usage."
                        )

                    elif (
                        "404" in error_text
                        or "NOT_FOUND" in error_text
                    ):
                        st.warning(
                            "This model may not be available to your "
                            "API key. Check the model IDs available "
                            "in Google AI Studio."
                        )

                    elif (
                        "504" in error_text
                        or "DEADLINE_EXCEEDED" in error_text
                    ):
                        st.warning(
                            "Gemini took too long to respond. "
                            "Try again later or check model availability."
                        )

            # ------------------------------------------
            # AGENT 2: CONTENT CREATOR
            # Runs only after Agent 1 succeeds.
            # ------------------------------------------
            if st.session_state.strategy:

                content_prompt = f"""
You are Agent 2, a marketing content creator.

Use the strategy created by Agent 1 below.

Product: {product}
Audience: {audience}
Market: {market}
Goal: {goal}
Tone: {tone}
Budget: USD {budget}

Create:
1. Three short social media posts.
2. One 15-20 second video script.
3. Two campaign headlines or taglines.
4. One message for parents or guardians.
5. A recommended channel for each content item.

Use clear headings and concise wording.
Do not invent product features or unsupported claims.
Do not guarantee sales or campaign results.
Respect privacy and use age-appropriate language
when children are part of the target audience.

AGENT 1 STRATEGY:
{st.session_state.strategy}
"""

                with st.spinner(
                    "Agent 2 is creating content from the strategy..."
                ):
                    try:
                        content = generate_with_retry(
                            client,
                            content_prompt
                        )

                        st.session_state.content = content

                    except Exception as exc:
                        st.error(
                            "Content generation failed: "
                            + str(exc)
                        )

                        st.info(
                            "The strategy was generated successfully. "
                            "You can retry content generation later."
                        )

            # ------------------------------------------
            # BUILD REPORT
            # ------------------------------------------
            if (
                st.session_state.strategy
                and st.session_state.content
            ):
                st.session_state.campaign_report = f"""
# AI Marketing Campaign Report

## Campaign Details

- Product: {product}
- Target audience: {audience}
- Budget: USD {budget}
- Market: {market}
- Campaign goal: {goal}
- Content tone: {tone}

## Agent 1: Marketing Strategy

{st.session_state.strategy}

## Agent 2: Marketing Content

{st.session_state.content}
"""


# ==================================================
# RESULTS
# ==================================================
if st.session_state.strategy:

    st.success("Marketing strategy generated successfully.")

    tab1, tab2, tab3 = st.tabs(
        [
            "Marketing Strategy",
            "Content Creator",
            "Download Report"
        ]
    )

    with tab1:
        st.markdown(st.session_state.strategy)

    with tab2:
        if st.session_state.content:
            st.markdown(st.session_state.content)
        else:
            st.info(
                "Content is not available yet. "
                "Try generating the campaign again."
            )

    with tab3:
        if st.session_state.campaign_report:
            st.download_button(
                label="Download Campaign Report",
                data=st.session_state.campaign_report,
                file_name="ai_marketing_campaign.md",
                mime="text/markdown",
                type="primary"
            )
        else:
            st.info(
                "The report will be available after both agents "
                "finish successfully."
            )


# ==================================================
# HOME DASHBOARD
# ==================================================
else:

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "AI Agents",
        "02",
        "Strategy and content"
    )

    col2.metric(
        "Workflow",
        "Sequential",
        "Agent 1 then Agent 2"
    )

    col3.metric(
        "Sample Budget",
        "$2,000",
        "Fully editable"
    )

    st.markdown("## Campaign Workflow")

    st.caption(
        "From campaign brief to strategy and marketing content."
    )

    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-number">01</div>
            <h4>Define the Brief</h4>
            <p>
                Enter the product, target audience, budget,
                market and campaign objective.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-number">02</div>
            <h4>Generate with AI</h4>
            <p>
                The strategist builds the plan. The content
                creator then uses that plan to create content.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-number">03</div>
            <h4>Review and Export</h4>
            <p>
                Review the strategy, inspect content and
                download the campaign report.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.info(
        "Start by entering your campaign details in the sidebar "
        "and clicking Generate Campaign. AI outputs should be "
        "reviewed before use."
    )


# ==================================================
# FOOTER
# ==================================================
st.divider()

st.caption(
    "AI MARKETING STRATEGY STUDIO | "
    "STREAMLIT + GOOGLE GEMINI"
)

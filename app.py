import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ----------------------------------
# CONFIG
# ----------------------------------

st.set_page_config(
    page_title="SmartOps ATS",
    page_icon="🧠",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/analyze"

# ----------------------------------
# SIDEBAR (SAAS STYLE)
# ----------------------------------

with st.sidebar:
    st.title("🧠 SmartOps ATS")

    st.caption("AI Recruitment Intelligence Platform")

    st.divider()

    st.subheader("Modules")
    st.write("📄 Resume Analyzer")
    st.write("📊 Skill Scoring")
    st.write("🎤 Interview Generator")
    st.write("🧑‍💼 Hiring Decision Engine")

    st.divider()

    st.info("Powered by FastAPI + AI Engine")

# ----------------------------------
# HEADER
# ----------------------------------

st.title("🚀 ATS SaaS Dashboard")
st.markdown("Upload a resume and get **AI-powered hiring insights** instantly.")

# ----------------------------------
# UPLOAD
# ----------------------------------

uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

# ----------------------------------
# CALL BACKEND
# ----------------------------------

if uploaded_file:

    with st.spinner("Analyzing resume..."):

        try:
            res = requests.post(
                API_URL,
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf"
                    )
                }
            )

            data = res.json()

        except Exception as e:
            st.error("Backend not running or failed.")
            st.stop()

    st.success("Analysis Complete")

    profile = data.get("profile", {})
    questions = data.get("questions", [])
    decision = data.get("decision", {})

    # ----------------------------------
    # KPI DASHBOARD
    # ----------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Hire Decision", decision.get("hire", "N/A"))

    with col2:
        st.metric("Confidence Score", f"{decision.get('confidence', 0)} / 100")

    with col3:
        st.metric("Skills Found", len(profile.get("skills", [])))

    st.divider()

    # ----------------------------------
    # TABS (SAAS STYLE)
    # ----------------------------------

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview",
        "💪 Skills Radar",
        "🎤 Interview Questions",
        "🧠 Raw AI Output"
    ])

    # ----------------------------------
    # TAB 1 - OVERVIEW
    # ----------------------------------

    with tab1:

        st.subheader("Candidate Summary")

        st.write(profile)

        st.markdown("### Key Insights")

        if decision.get("hire") == "YES":
            st.success("Strong candidate — recommended for interview")
        elif decision.get("hire") == "MAYBE":
            st.warning("Moderate candidate — needs review")
        else:
            st.error("Weak match for role")

    # ----------------------------------
    # TAB 2 - SKILLS RADAR
    # ----------------------------------

    with tab2:

        st.subheader("Skill Distribution")

        skills = profile.get("skills", [])

        if skills:

            df = pd.DataFrame({
                "Skill": skills,
                "Score": [80 for _ in skills]
            })

            fig = px.bar(df, x="Skill", y="Score")

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("No skills detected")

    # ----------------------------------
    # TAB 3 - INTERVIEW QUESTIONS
    # ----------------------------------

    with tab3:

        st.subheader("Generated Interview Questions")

        if questions:
            for i, q in enumerate(questions, 1):
                st.write(f"{i}. {q}")
        else:
            st.info("No questions generated")

    # ----------------------------------
    # TAB 4 - RAW OUTPUT
    # ----------------------------------

    with tab4:

        st.subheader("Raw API Response")

        st.json(data)

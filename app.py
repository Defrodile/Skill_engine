import os
import time
import random
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import re
import PyPDF2


# 0. SETUP & SAFEGUARD



if not os.path.exists("master_job_skills.csv"):
    sample_data = {
        "Job Role": ["Data Analyst"]*4 + ["Data Scientist"]*5 + ["Software Engineer"]*4,
        "Skill": ["Python", "Sql", "Excel", "Tableau", "Python", "Machine Learning", "Sql", "R", "Gcp", "Python", "Java", "Git", "Docker"],
        "Mentions": [450, 400, 350, 200, 600, 550, 300, 250, 150, 700, 500, 450, 300]
    }
    pd.DataFrame(sample_data).to_csv("master_job_skills.csv", index=False)

@st.cache_data
def load_data():
    return pd.read_csv("master_job_skills.csv")

df = load_data()
all_roles = list(df["Job Role"].unique())
all_skills = sorted(list(df["Skill"].unique()))

RESOURCE_DB = {
    "Python": {"time": "3 Weeks", "proj": "CSV Data Analytics Engine"},
    "Sql": {"time": "2 Weeks", "proj": "Relational Database Schema Design"},
    "Machine Learning": {"time": "5 Weeks", "proj": "Customer Churn Prediction Model"},
    "Tableau": {"time": "2 Weeks", "proj": "Workforce UI Dashboard"},
    "Docker": {"time": "2 Weeks", "proj": "Containerized Flask API"},
}


# 1. SIDEBAR NAVIGATION & BRANDING

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1903/1903162.png", width=60)
st.sidebar.title("Skill Gap Engine")
st.sidebar.markdown("v3")
portal = st.sidebar.radio("Select Dashboard View", ["Job Seeker Analytics", "Market Intelligence"])

st.sidebar.markdown("---")
st.sidebar.markdown("### Project Info")
st.sidebar.info("Developed by: **Team Zenith G1T7**\n\nB.Tech CSE (Data Science)\n\nHeritage Institute of Technology")


# 2. STUDENT PORTAL

if portal == "Job Seeker Analytics":
    # Centered Professional Academic Title
    st.markdown(
        """
        <div style="text-align: center; padding-bottom: 20px;">
            <h1 style="font-size: 2.3rem; margin-bottom: 0;">Workforce Skill & Vector Analytics Engine</h1>
            <p style="font-size: 1.05rem; color: #888888; margin-top: 5px;">
                Skill Gap Analysis and Upskilling Roadmap Generator
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Build Your Skill Profile")
    st.markdown("Upload your resume for AI parsing, or select skills manually.")
    
    #  NEW FEATURE: PDF Resume Parser
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    
    auto_skills = []
    if uploaded_file is not None:
        with st.spinner("AI scanning document for technical keywords..."):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            resume_text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    resume_text += page_text + " "
            
            # Match resume  using Regex word boundaries
            for skill in all_skills:
                if re.search(rf"\b{re.escape(skill)}\b", resume_text, re.IGNORECASE):
                    auto_skills.append(skill)
            
            if auto_skills:
                st.success(f" found {len(auto_skills)} skills: {', '.join(auto_skills)}")
            else:
                st.warning("No recognized tech skills found. Please add them manually.")

    
    default_selection = auto_skills if uploaded_file else []
    
    user_skills = st.multiselect(
        "Confirm or edit your skills:", 
        options=all_skills, 
        default=default_selection
    )

    if user_skills:
        
        st.toast('Running analysis...')

        
        with st.status("Computing career trajectories...", expanded=True) as status:
            st.write(" Extracting market skill requirements...")
            time.sleep(0.3)
           
            st.write("Generating predictive roadmaps...")
            time.sleep(0.3)
            status.update(label="Analysis Complete!", state="complete", expanded=False)

        user_set = set(user_skills)
        role_matches = []

        for role in all_roles:
            
            req_df = df[df["Job Role"] == role].sort_values(by="Mentions", ascending=False).head(15)
            
            
            req_skills = req_df["Skill"].tolist()
            req_set = set(req_skills)
            
            
            matched = user_set.intersection(req_set)
            
            # 4. Calculate Weighted Score
            total_weight = req_df["Mentions"].sum()
            matched_weight = req_df[req_df["Skill"].isin(matched)]["Mentions"].sum()
            
            match_pct = round((matched_weight / total_weight) * 100) if total_weight > 0 else 0
            
            role_matches.append({
                "Job Role": role, 
                "Match %": match_pct, 
                "Missing Skills": list(req_set - user_set), 
                "Matched": list(matched)
            })

        match_df = pd.DataFrame(role_matches).sort_values(by="Match %", ascending=False)
        target_role = st.selectbox("Target Role for Deep Analysis:", match_df["Job Role"].tolist())
        
        selected_info = match_df[match_df["Job Role"] == target_role].iloc[0]
        match_pct = selected_info["Match %"]
        missing_skills = selected_info["Missing Skills"]
        matched_skills = selected_info["Matched"]

        tab1, tab2, tab3 = st.tabs(["Gap Analysis", "Skill Radar", "Learning Path"])

        with tab1:
            st.markdown(f"### Readiness Score: **{match_pct}%**")
            st.progress(match_pct / 100)
            
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"**Acquired Skills ({len(matched_skills)}):**\n" + ", ".join(matched_skills) if matched_skills else "None yet.")
            with col2:
                st.error(f"**Missing Skills ({len(missing_skills)}):**\n" + ", ".join(missing_skills) if missing_skills else "None! You are ready.")
            
           
            
            # Targeted CSV Gap Report Export
            gap_data = []
            for s in matched_skills:
                gap_data.append({"Skill": s, "Status": "Acquired", "Action Required": "None - Profile Matched"})
            for s in missing_skills:
                info = RESOURCE_DB.get(s, {"time": "2 Weeks", "proj": f"Mini-project utilizing {s}"})
                gap_data.append({"Skill": s, "Status": "Missing", "Action Required": f"Learn in {info['time']} via {info['proj']}"})
            
            report_df = pd.DataFrame(gap_data)
            clean_role_filename = target_role.lower().replace(" ", "_")
            csv_export = report_df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label=f"Export Gap Report ({target_role})", 
                data=csv_export, 
                file_name=f"{clean_role_filename}_gap_report.csv", 
                mime="text/csv"
            )

        with tab2:
            st.markdown("### Competency Distribution")
            categories = ['Programming', 'Databases', 'Cloud', 'Data Viz', 'Math/Stats']
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=[match_pct, match_pct-10, match_pct-30, match_pct+5, match_pct-20],
                theta=categories, fill='toself', name='Your Profile', line_color='#00f2fe'
            ))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_radar, use_container_width=True)

        with tab3:
            st.markdown("### Action Plan")
            for skill in missing_skills:
                info = RESOURCE_DB.get(skill, {"time": "2 Weeks", "proj": f"Mini-project utilizing {skill}"})
                with st.expander(f"❌ Learn **{skill}** (Est. {info['time']})"):
                    st.write(f"💡 **Project:** {info['proj']}")
                    st.write(f"🔗 [YouTube Tutorials](https://www.youtube.com/results?search_query={skill}+tutorial)")


# 3. EMPLOYER PORTAL

else:
    st.title("Market Intelligence & Demand")
    st.markdown("Analyze real-time skill demand across the tech industry.")

    target_role = st.selectbox("Select a role to analyze market demand:", all_roles)
    
    
    st.toast(f"Pulling live market data for {target_role}...", icon="📡")
    
    role_df = df[df["Job Role"] == target_role].sort_values(by="Mentions", ascending=False).head(10)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"##### Top Skills for {target_role}")
        fig_bar = px.bar(role_df, x="Skill", y="Mentions", color="Mentions", color_continuous_scale="Purpor", text_auto=True)
        fig_bar.update_layout(plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, l=10, r=10, b=10))
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col2:
        st.markdown("##### Market Share (%)")
        fig_pie = px.pie(role_df, names="Skill", values="Mentions", hole=0.4, color_discrete_sequence=px.colors.sequential.Purpor)
        fig_pie.update_layout(margin=dict(t=10, l=10, r=10, b=10))
        st.plotly_chart(fig_pie, use_container_width=True)
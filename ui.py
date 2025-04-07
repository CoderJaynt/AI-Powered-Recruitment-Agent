import streamlit as st
from agent import ResumeAnalysisAgent
from app import process_resume  # The function you just created


def render_ui():
    """Render the main UI layout for the LLaMA-powered Recruitment Agent."""
    st.set_page_config(page_title="AI-Powered Recruitment Agent", layout="wide")
    
    st.title("🧠 AI-Powered Recruitment Agent (LLaMA-Driven)")
    st.markdown("🚀 Powered by a local LLaMA model – no API key required.")

    # Four feature columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.header("📄 Resume Analysis")
        st.session_state.uploaded_file = st.file_uploader("📤 Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
        st.session_state.role = st.selectbox("🎯 Select Role", [
            "AI/ML Engineer", "Frontend Engineer", "Backend Engineer", "Data Engineer",
            "DevOps Engineer", "Cybersecurity Engineer", "Full Stack Developer"
        ])
        st.session_state.custom_jd = st.text_area("📝 Custom Job Description (Optional)")
        if st.button("🔍 Analyze Resume"):
            if st.session_state.uploaded_file:
                st.session_state.trigger_analysis = True
                agent = ResumeAnalysisAgent()
                analysis_message = agent.analyze_resume(st.session_state.uploaded_file)
                
                # Display analysis results
                if agent.resume_weaknesses:
                    st.subheader("Weak Skills Identified:")
                    for weakness in agent.resume_weaknesses:
                        st.write(f"**Skill**: {weakness['skill']}")
                        st.write(f"**Score**: {weakness['score']}")
                        st.write(f"**Weakness**: {weakness['detail']}")
                        st.write(f"**Improvement Suggestions**: {', '.join(weakness['suggestions'])}")
                        st.write(f"**Example to Add**: {weakness['example']}")
                        st.write("---")
                else:
                    st.write("No weak skills identified.")
            else:
                st.warning("Please upload a resume first.")

    with col2:
        st.header("❓ Resume Q&A")
        st.session_state.question = st.text_input("💬 Ask a question about your resume")
        if st.button("🧠 Get Answer"):
            st.session_state.trigger_qna = True

    with col3:
        st.header("🎤 Interview Questions")
        
        st.session_state.question_types = st.multiselect(
            "📌 Question Types", ["Technical", "Behavioral", "HR", "Situational"]
        )
        st.session_state.difficulty = st.select_slider(
            "📊 Difficulty", options=["Easy", "Medium", "Hard"]
        )
        st.session_state.num_questions = st.number_input(
            "🔢 Number of Questions", min_value=1, max_value=20, value=5
        )

        if st.button("🚀 Generate Interview Questions"):
            if "uploaded_file" in st.session_state and st.session_state.uploaded_file:
                with st.spinner("Analyzing resume and generating questions..."):
                    questions = process_resume(
                        st.session_state.uploaded_file,
                        types=st.session_state.question_types,
                        difficulty=st.session_state.difficulty,
                        count=st.session_state.num_questions
                    )
                st.success("Questions generated!")
                st.subheader("📌 Interview Questions")
                for q in questions:
                    st.write(f"• {q}")
            else:
                st.warning("Please upload a resume first.")


    with col4:
        st.header("📈 Resume Improvement")
        st.session_state.improvement_areas = st.multiselect("🛠 Areas to Improve", ["Skills", "Experience", "Formatting", "Achievements"])
        st.session_state.target_role = st.text_input("🎯 Target Role (Optional)")
        if st.button("✨ Get Suggestions"):
            st.session_state.trigger_improvement = True


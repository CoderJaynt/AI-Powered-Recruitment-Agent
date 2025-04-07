import streamlit as st
import ui
from agent import ResumeAnalysisAgent
import atexit

# Role requirements dictionary
ROLE_REQUIREMENTS = {
    "AI/ML Engineer": [
        "Python", "PyTorch", "TensorFlow", "Machine Learning", "Deep Learning",
        "MLOps", "Scikit-Learn", "NLP", "Computer Vision", "Reinforcement Learning",
        "Hugging Face", "Data Engineering", "Feature Engineering", "AutoML"
    ],
    "Frontend Engineer": [
        "React", "Vue", "Angular", "HTML5", "CSS3", "JavaScript", "TypeScript",
        "Next.js", "Svelte", "Bootstrap", "Tailwind CSS", "GraphQL", "Redux",
        "WebAssembly", "Three.js", "Performance Optimization"
    ],
    "Backend Engineer": [
        "Python", "Java", "Node.js", "REST APIs", "Cloud Services", "Kubernetes",
        "Docker", "GraphQL", "Microservices", "gRPC", "Spring Boot",
        "NoSQL Databases", "SQL Databases", "Message Queues", "Redis"
    ],
    "Data Engineer": [
        "Python", "SQL", "Apache Spark", "Hadoop", "Kafka", "Airflow",
        "Data Warehousing", "ETL", "BigQuery", "Snowflake", "AWS Glue",
        "Cloud Data Engineering", "Data Modeling", "Redshift"
    ],
    "DevOps Engineer": [
        "CI/CD", "Docker", "Kubernetes", "Terraform", "AWS", "Azure", "Google Cloud",
        "Jenkins", "Ansible", "Prometheus", "Grafana", "Infrastructure as Code (IaC)",
        "Monitoring & Logging", "Security Best Practices"
    ],
    "Cybersecurity Engineer": [
        "Network Security", "Penetration Testing", "Cryptography", "SOC",
        "Ethical Hacking", "SIEM", "Threat Intelligence", "Incident Response",
        "Firewalls", "Identity & Access Management", "Security Compliance"
    ],
    "Full Stack Developer": [
        "JavaScript", "React", "Node.js", "Express.js", "MongoDB", "GraphQL",
        "SQL", "Django", "Flask", "REST APIs", "Microservices", "Docker",
        "Cloud Deployment", "Serverless Architecture"
    ]
}

# Initialize session state variables
defaults = {
    'resume_agent': None,
    'resume_analyzed': False,
    'analysis_result': None,
}

for key, default in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default

def setup_agent(config):
    # Simulate UI prompt for consistency, but no key is actually needed
    if not config.get("openai_api_key"):
        st.warning("ℹ No API key needed for local LLaMA, continuing without it.")
    
    agent = st.session_state.get("resume_agent")

    if agent is None:
        agent = ResumeAnalysisAgent()  # No API key required
        st.session_state.resume_agent = agent

    return agent

def analyze_resume(agent, resume_file, role, custom_jd=None):
    if agent is None:
        st.error("⚠ The LLaMA-based resume analysis agent is not initialized.")
        return None

    if not resume_file:
        st.error("⚠ Please upload a resume file for analysis.")
        return None

    # Perform resume analysis using the local agent
    result = agent.analyze_resume(resume_file, role_requirements=role, custom_jd=custom_jd)

    # Store results in Streamlit session state
    st.session_state.resume_analyzed = True
    st.session_state.analysis_result = result

    return result

def ask_question(agent, question):
    """Ask a question about the resume using the LLaMA-powered agent"""
    if agent is None:
        return "⚠ Resume analysis agent is not initialized."

    try:
        with st.spinner("💬 Thinking..."):
            response = agent.ask_question(question)
            return response
    except Exception as e:
        return f"❌ Error while answering the question: {e}"
    
def generate_interview_questions(agent, question_types, difficulty, num_questions):
    """Generate interview questions based on the resume analysis"""
    if agent is None:
        st.error("⚠ Resume analysis agent is not initialized.")
        return []

    try:
        with st.spinner("🤖 Generating interview questions..."):
            questions = agent.generate_interview_questions(question_types, difficulty, num_questions)
            return questions
    except Exception as e:
        st.error(f"⚠ Error generating interview questions: {e}")
        return []


def get_improved_resume(agent, target_role, highlight_skills):
    """Get an improved version of the resume"""
    if agent is None:
        st.error("⚠ Resume analysis agent is not initialized.")
        return ""

    try:
        with st.spinner("✨ Creating improved resume..."):
            improved_resume = agent.get_improved_resume(target_role, highlight_skills)
            return improved_resume
    except Exception as e:
        st.error(f"⚠ Error creating improved resume: {e}")
        return ""
from agent import ResumeAnalysisAgent

def process_resume(uploaded_file):
    agent = ResumeAnalysisAgent()

    # Step 1: Extract text
    resume_text = agent.extract_text_from_file(uploaded_file)

    # Step 2: Set it inside the agent
    agent.resume_text = resume_text

    # Step 3: Initialize vector store (load or create)
    agent.initialize_vector_store()

    # Step 4: Now you can generate interview questions
    questions = agent.generate_interview_questions()

    return questions
    

def improve_resume(agent, improvement_areas, target_role=""):
    """Generate resume improvement suggestions"""
    if agent is None:
        st.error("⚠ Resume analysis agent is not initialized.")
        return ""

    try:
        with st.spinner("✨ Generating resume improvement suggestions..."):
            suggestions = agent.improve_resume(improvement_areas, target_role)
            return suggestions
    except Exception as e:
        st.error(f"⚠ Error generating resume improvements: {e}")
        return ""



def main():
    """Main function to set up the UI and functionalities."""
    
    # Page Configuration
    st.set_page_config(page_title="AI-Powered Recruitment Agent", layout="wide")

    # Sidebar Configuration
    st.sidebar.title("Configuration")
    st.sidebar.markdown("Using **LLaMA API** for all processing. No API key needed.")
    
    # Setup Configuration (no API key needed for LLaMA)
    config = {}

    # Setup the Resume Analysis Agent
    setup_agent(config)

    # Page Title
    st.title("🧠 AI-Powered Recruitment Agent")

    # Tabs for Different Functionalities
    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Resume Analysis",
        "❓ Resume Q&A",
        "🎤 Interview Questions",
        "🔍 Improved Resume"
    ])

    with tab1:
        st.header("Resume Analysis")
        uploaded_file = st.file_uploader("📤 Upload your resume (PDF/DOCX)", type=["pdf", "docx","txt"])
        role = st.selectbox("🎯 Select Role", list(ROLE_REQUIREMENTS.keys()))
        custom_jd = st.text_area("📝 Enter Custom Job Description (Optional)")

        if st.button("🔍 Analyze Resume"):
            if uploaded_file:
                analyze_resume(st.session_state.resume_agent, uploaded_file, role, custom_jd)
            else:
                st.warning("⚠ Please upload a resume file.")

    with tab2:
        st.header("Resume Q&A")
        question = st.text_input("❓ Ask a question about your resume")
        if st.button("💬 Get Answer"):
            if question:
                response = ask_question(st.session_state.resume_agent, question)
                st.write(response)
            else:
                st.warning("⚠ Enter a question to ask.")

    with tab3:
        st.header("Interview Questions Generator")
        question_types = st.multiselect("📌 Select Question Types", ["Technical", "Behavioral", "HR", "Situational"])
        difficulty = st.select_slider("📊 Select Difficulty", options=["Easy", "Medium", "Hard"])
        num_questions = st.number_input("🔢 Number of Questions", min_value=1, max_value=20, value=5)

        if st.button("🚀 Generate Questions"):
            questions = generate_interview_questions(st.session_state.resume_agent, question_types, difficulty, num_questions)
            st.write(questions)

    with tab4:
        st.header("📈 Improve Resume")
        improvement_areas = st.multiselect("🛠 Select Areas to Improve", ["Skills", "Experience", "Formatting", "Achievements"])
        target_role = st.text_input("🎯 Target Role (Optional)")

        if st.button("🧠 Get Improvement Suggestions"):
            suggestions = improve_resume(st.session_state.resume_agent, improvement_areas, target_role)
            st.write(suggestions)

# # Run the app
# if __name__ == "__main__":
#     main()

if __name__ == "__main__":
    main()


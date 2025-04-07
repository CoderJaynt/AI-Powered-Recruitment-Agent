# 🤖 AI-Powered Recruitment Agent

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/langchain-LLM-green)](https://www.langchain.com/)
[![Streamlit](https://img.shields.io/badge/streamlit-ui-red)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)

An **AI-powered assistant** that transforms how recruiters and job seekers interact with resumes. Built using **LangChain**, **ChatOllama**, **HuggingFace**, **FAISS**, and **Streamlit**, this tool extracts and analyzes resume content, matches it with job descriptions, generates interview questions, and provides improvement suggestions — all in an intuitive interface.

---

## 🌟 Key Features

- 📄 **Resume Upload & Parsing**  
  Upload PDF or text resumes and extract key insights like skills, experience, and education.

- 🔍 **Resume Q&A**  
  Ask custom questions about the resume. Get intelligent, context-aware answers from the LLM.

- 💡 **Resume Improvements**  
  Receive AI-driven suggestions to improve grammar, structure, and content.

- 🎯 **Interview Questions Generator**  
  Generates personalized interview questions based on the uploaded resume and job description.

- 🧠 **Semantic Matching**  
  Uses vector embeddings and FAISS to semantically match resume content with job requirements.

- 🖥️ **Interactive UI with Streamlit**  
  A responsive and user-friendly interface with simulated agent responses using predefined results (for demonstration without API keys).

---

## 🛠️ Tech Stack

| Component            | Technology                          |
|---------------------|--------------------------------------|
| Core Language        | Python                               |
| UI                   | Streamlit                            |
| LLM Integration      | LangChain + ChatOllama               |
| Embedding Models     | HuggingFace Transformers             |
| Vector DB            | FAISS                                |
| File Handling        | PyMuPDF / Python-docx / base64       |
| NLP Utilities        | NLTK, spaCy (optional)               |

---

## 📁 Project Structure

agent.py
app.py
ui.py
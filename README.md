<div align="center">

<!-- Animated Header -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=7c5cfc&height=200&section=header&text=AI%20Recruitment%20Agent&fontSize=48&fontColor=ffffff&fontAlignY=50" width="100%"/>

<br/>

<!-- Badges -->
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![FAISS](https://img.shields.io/badge/FAISS-Vector%20DB-00bfae?style=for-the-badge&logo=meta&logoColor=white)](https://faiss.ai/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Embeddings-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

<br/>

> **An AI-powered assistant that transforms how recruiters and job seekers interact with resumes.**  
> Built using **LangChain**, **ChatOllama**, **HuggingFace**, **FAISS**, and **Streamlit** — this tool extracts and analyzes resume content, semantically matches it with job descriptions, generates interview questions, and provides improvement suggestions.

<br/>

[🚀 Quick Start](#-quick-start) · [✨ Features](#-features) · [🛠️ Tech Stack](#️-tech-stack) · [📁 Project Structure](#-project-structure) · [🤝 Contributing](#-contributing)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 📄 Resume Upload & Parsing
Upload PDF or text resumes and extract key insights — skills, experience, education — in seconds.

### 🔍 Resume Q&A
Ask custom questions about any resume. Get intelligent, context-aware answers powered by the LangGraph agent pipeline.

### 💡 Resume Improvements
Receive AI-driven suggestions to improve grammar, structure, impact, and content quality.

</td>
<td width="50%">

### 🎯 Interview Question Generator
Generates personalized, role-specific interview questions based on the uploaded resume and job description.

### 🧠 Semantic Matching
Uses vector embeddings + FAISS to semantically match resume content with job requirements — beyond keyword search.

### 🖥️ Interactive Streamlit UI
A responsive, user-friendly interface with real-time agent responses and intuitive file uploads.

</td>
</tr>
</table>

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| 🤖 **Agent Orchestration** | [LangGraph](https://langchain-ai.github.io/langgraph/) | Stateful, multi-step agentic workflows |
| 🗣️ **LLM Backend** | ChatOllama | Local LLM inference |
| 🔢 **Embeddings** | HuggingFace Transformers | Semantic text representations |
| 🗄️ **Vector Store** | FAISS | Fast similarity search |
| 🖼️ **UI** | Streamlit | Interactive web interface |
| 🐍 **Language** | Python 3.9+ | Core implementation |
| 📂 **File Handling** | PyMuPDF · python-docx · base64 | PDF & document parsing |
| 🔡 **NLP Utilities** | NLTK · spaCy *(optional)* | Text preprocessing |

---

## 📁 Project Structure

```
recruitment-agent/
│
├── agent.py          # LangGraph agent definition — tools, nodes, graph edges
├── app.py            # Application logic — resume processing & pipeline orchestration
├── ui.py             # Streamlit UI — file upload, chat, results rendering
│
├── requirements.txt  # Python dependencies
└── README.md
```

### Agent Pipeline

```
User Input
    │
    ▼
┌─────────┐     ┌─────────┐     ┌───────────┐     ┌────────────┐
│  ui.py  │────▶│  app.py │────▶│  agent.py │────▶│ LangGraph  │
│ Streamlit│     │ Orchestr│     │  Tools &  │     │  StateGraph│
└─────────┘     └─────────┘     │   Nodes   │     └─────┬──────┘
                                 └───────────┘           │
                                                         ▼
                                               ┌──────────────────┐
                                               │  FAISS + ChatOllama│
                                               │  Embeddings + LLM  │
                                               └──────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.ai/) installed and running locally
- Git

### 1. Clone the repository

```bash
git clone https://github.com/your-username/recruitment-agent.git
cd recruitment-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Pull a local model via Ollama

```bash
ollama pull llama3
```

### 4. Launch the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` 🎉

---

## 🧩 How It Works

```
1. Upload Resume (PDF / TXT)
        │
        ▼
2. Document is chunked and embedded via HuggingFace
        │
        ▼
3. Chunks stored in FAISS vector index
        │
        ▼
4. User pastes Job Description
        │
        ▼
5. LangGraph agent runs multi-step pipeline:
   ├── Tool: SemanticMatcher  → computes JD ↔ resume match score
   ├── Tool: QuestionGenerator → generates tailored interview Qs
   ├── Tool: ResumeQA         → answers custom user questions
   └── Tool: ImprovementAgent → suggests resume enhancements
        │
        ▼
6. Results rendered in Streamlit UI
```

---

## 📦 Requirements

```txt
langgraph
langchain-community
langchain-ollama
streamlit
faiss-cpu
sentence-transformers
transformers
PyMuPDF
python-docx
nltk
```

Install all at once:

```bash
pip install -r requirements.txt
```

---

## 🖼️ Screenshots

> _Add screenshots of your Streamlit UI here_

| Resume Upload | Semantic Match | Interview Qs |
|:---:|:---:|:---:|
| *(screenshot)* | *(screenshot)* | *(screenshot)* |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

```bash
# 1. Fork the repo and clone your fork
git clone https://github.com/your-username/recruitment-agent.git

# 2. Create a feature branch
git checkout -b feature/amazing-feature

# 3. Commit your changes
git commit -m "feat: add amazing feature"

# 4. Push and open a Pull Request
git push origin feature/amazing-feature
```

Please follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ using LangGraph + Streamlit**

<img src="https://capsule-render.vercel.app/api?type=waving&color=7c5cfc&height=100&section=footer" width="100%"/>

</div>

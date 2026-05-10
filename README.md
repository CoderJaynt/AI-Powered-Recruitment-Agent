<div align="center">

<!-- Animated Header Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=AI%20Resume%20Analysis%20Agent&fontSize=42&fontColor=fff&animation=twinkling&fontAlignY=35&desc=LLaMA-Powered%20%E2%80%A2%20Local%20%E2%80%A2%20No%20API%20Key%20Required&descAlignY=55&descSize=18" />

<br/>

<!-- Badges Row 1 -->
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-🦜-1C3C3C?style=for-the-badge)](https://langchain.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Ollama](https://img.shields.io/badge/Ollama-LLaMA3-black?style=for-the-badge&logo=llama&logoColor=white)](https://ollama.com)
[![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-0467DF?style=for-the-badge&logo=meta&logoColor=white)](https://github.com/facebookresearch/faiss)

<!-- Badges Row 2 -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge&logo=github)](CONTRIBUTING.md)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Embeddings-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co)
[![Offline](https://img.shields.io/badge/100%25-Offline%20Ready-success?style=for-the-badge&logo=lock&logoColor=white)]()

<br/>

> **🔒 Fully local. Zero cloud dependency. Your resume never leaves your machine.**

<br/>

</div>

---

## 🌟 What Is This?

**AI Resume Analysis Agent** is a fully local, LLaMA-powered recruitment intelligence tool that analyzes resumes, matches them against job descriptions, generates interview questions, and suggests improvements — all without sending a single byte to the cloud.

Built with `LangChain`, `FAISS`, `HuggingFace Embeddings`, and `Ollama`, it gives you enterprise-grade resume screening right on your laptop.

<br/>

---

## ✨ Features at a Glance

| Feature | Description |
|---|---|
| 📄 **Resume Analysis** | Upload PDF, DOCX, or TXT — get instant skill gap analysis |
| 🧠 **Semantic Skill Matching** | Cosine similarity scoring against JD-extracted skills |
| ❓ **Resume Q&A (RAG)** | Ask anything about the resume via retrieval-augmented generation |
| 🎤 **Interview Generator** | Technical, behavioral, HR & situational questions by difficulty |
| 📈 **Resume Improver** | LLaMA rewrites your resume for target roles, ATS-optimized |
| 🔍 **JD Skill Extractor** | Automatically parse required skills from any job description |
| 🧩 **Weakness Analyser** | Deep-dives into missing skills with specific fix suggestions |
| 💾 **Persistent Vector Store** | FAISS index saved to disk — no re-embedding on reload |

<br/>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Streamlit UI (app.py / ui.py)            │
│  ┌──────────────┐ ┌──────────────┐ ┌────────────┐ ┌──────────┐ │
│  │Resume Upload │ │  Resume Q&A  │ │ Interview  │ │ Improve  │ │
│  │ + Role Pick  │ │  (RAG Chat)  │ │  Generator │ │ Resume   │ │
│  └──────┬───────┘ └──────┬───────┘ └─────┬──────┘ └────┬─────┘ │
└─────────┼────────────────┼───────────────┼─────────────┼────────┘
          │                │               │             │
          ▼                ▼               ▼             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ResumeAnalysisAgent (agent.py)               │
│                                                                 │
│  ┌─────────────────┐        ┌──────────────────────────────┐    │
│  │  Text Extractor  │        │     LLM Layer (ChatOllama)   │    │
│  │  PDF / DOCX / TXT│───────▶│  llama3 / llama2 / mistral  │    │
│  └─────────────────┘        └──────────────────────────────┘    │
│           │                              │                       │
│           ▼                              ▼                       │
│  ┌─────────────────┐        ┌──────────────────────────────┐    │
│  │  Text Chunker    │        │    JD Skill Extractor        │    │
│  │  (RecursiveText  │        │    (LLaMA → Python list)     │    │
│  │   Splitter 1000) │        └──────────────────────────────┘    │
│  └────────┬────────┘                     │                       │
│           │                              ▼                       │
│           ▼                  ┌──────────────────────────────┐    │
│  ┌─────────────────┐        │   Semantic Skill Analyser    │    │
│  │  HuggingFace     │───────▶│   (Cosine Similarity Score)  │    │
│  │  Embeddings      │        └──────────────────────────────┘    │
│  │  all-MiniLM-L6-v2│                                            │
│  └────────┬────────┘                                             │
│           │                                                      │
│           ▼                                                      │
│  ┌─────────────────────────────────────┐                        │
│  │           FAISS Vector Store         │                        │
│  │  (Persisted to disk: faiss_vectorstore/) │                   │
│  │  Used for: RAG, Q&A, Skill Retrieval │                        │
│  └─────────────────────────────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
```

<br/>

---

## 🔄 Workflow

```
  User Uploads Resume
         │
         ▼
  ┌─────────────┐
  │ Text Extract │  ◄── PDF (PyPDF2) / DOCX (Unstructured) / TXT
  └──────┬──────┘
         │
         ▼
  ┌──────────────────┐
  │ Chunk & Embed     │  ◄── RecursiveCharacterTextSplitter → HuggingFace Embeddings
  └──────┬───────────┘
         │
         ▼
  ┌──────────────┐
  │  FAISS Index  │  ◄── Saved locally for session persistence
  └──────┬───────┘
         │
    ┌────┴──────────────────────────┐
    │                               │
    ▼                               ▼
┌─────────────────┐       ┌───────────────────────┐
│  Skill Matching  │       │  RAG Q&A Pipeline      │
│  (Cosine Sim)    │       │  (Similarity Search +  │
│  vs JD Skills    │       │   LLaMA Context Answer)│
└────────┬────────┘       └───────────┬────────────┘
         │                            │
         ▼                            ▼
┌─────────────────────────────────────────────────┐
│           Structured Analysis Output             │
│  • Skill scores (0–10)                           │
│  • Matched / Missing skills                      │
│  • Weakness breakdown with suggestions           │
│  • Interview questions (by type & difficulty)    │
│  • Rewritten / improved resume text              │
└─────────────────────────────────────────────────┘
```

<br/>

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **UI** | Streamlit | Multi-tab web interface |
| **LLM** | Ollama (LLaMA 3 / LLaMA 2) | All text generation & reasoning |
| **Orchestration** | LangChain | Chains, prompts, document loaders |
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2` | Local semantic embeddings |
| **Vector DB** | FAISS | Fast similarity search & RAG |
| **PDF Parsing** | PyPDF2, LangChain PyPDFLoader | Text extraction from PDFs |
| **DOCX Parsing** | UnstructuredWordDocumentLoader | Text extraction from Word docs |
| **Skill Scoring** | scikit-learn (cosine_similarity) | Resume-to-JD semantic matching |
| **Language** | Python 3.9+ | Core runtime |

<br/>

---

## 📦 Installation

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com) installed and running
- At least one LLaMA model pulled locally

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-resume-agent.git
cd ai-resume-agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

<details>
<summary>📋 Full requirements.txt</summary>

```txt
streamlit
langchain
langchain-community
langchain-huggingface
langchain-core
faiss-cpu
sentence-transformers
PyPDF2
numpy
scikit-learn
python-dotenv
unstructured[docx]
```

</details>

### 3. Pull a LLaMA Model via Ollama

```bash
ollama pull llama3
# or
ollama pull llama2
# or
ollama pull mistral
```

### 4. Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` 🚀

<br/>

---

## 🗂️ Project Structure

```
ai-resume-agent/
│
├── app.py                  # Main Streamlit app — routing & tab logic
├── agent.py                # Core ResumeAnalysisAgent class
├── ui.py                   # UI rendering helpers & layout
│
├── faiss_vectorstore/      # Persisted FAISS index (auto-created)
├── resume_faiss_index/     # Secondary FAISS index for resume RAG
│
├── requirements.txt
└── README.md
```

<br/>

---

## 🎯 Supported Roles

The agent ships with pre-loaded skill requirements for 7 engineering tracks:

| Role | Key Skills Checked |
|---|---|
| 🤖 AI/ML Engineer | PyTorch, TensorFlow, NLP, MLOps, Hugging Face... |
| 🎨 Frontend Engineer | React, TypeScript, Next.js, Tailwind, WebAssembly... |
| ⚙️ Backend Engineer | Node.js, Kubernetes, gRPC, Microservices, Redis... |
| 🗄️ Data Engineer | Spark, Kafka, Airflow, Snowflake, BigQuery... |
| 🚀 DevOps Engineer | Terraform, CI/CD, Prometheus, IaC, Grafana... |
| 🔐 Cybersecurity Engineer | SIEM, Pen Testing, SOC, IAM, Cryptography... |
| 🌐 Full Stack Developer | React + Node + MongoDB + Docker + Serverless... |

You can also paste any **custom job description** and the agent will extract skills on the fly using LLaMA.

<br/>

---

## 🖥️ UI Tabs Overview

```
┌──────────────────────────────────────────────────────────┐
│  📄 Resume Analysis │ ❓ Resume Q&A │ 🎤 Interview │ 🔍 Improve │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Tab 1 — Upload resume, select role or paste JD,         │
│           click Analyze → get skill gap + score          │
│                                                          │
│  Tab 2 — Ask natural language questions about the        │
│           resume (RAG-powered, context-aware)            │
│                                                          │
│  Tab 3 — Pick question types, difficulty, count →        │
│           get a tailored interview question set          │
│                                                          │
│  Tab 4 — Select weak areas + target role →               │
│           get an ATS-optimized rewritten resume          │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

<br/>

---

## 🔑 Key Design Decisions

- **100% local inference** — LLaMA runs via Ollama on-device. No OpenAI, no Anthropic, no billing.
- **FAISS persistence** — Vector store is saved to disk so repeated sessions don't re-embed from scratch.
- **Dual vector stores** — One for RAG Q&A (`resume_faiss_index`), one for skill retrieval (`faiss_vectorstore`), keeping concerns separated.
- **Graceful JSON fallback** — LLM weakness analysis attempts structured JSON; falls back to raw text on parse failure.
- **Semantic scoring** — Skill matching uses cosine similarity on embeddings rather than naive keyword matching, giving far more accurate gap analysis.

<br/>

---

## ⚠️ Known Limitations & Roadmap

| Status | Item |
|---|---|
| 🔧 | `generate_interview_questions` references `self.vector_store` but attribute is `self.rag_vectorstore` — needs fix |
| 🔧 | `create_vector_store` called with and without arguments inconsistently |
| 🔧 | `analyze_resume_weaknesses` invokes `llm.invoke()` but expects `.strip()` on a `BaseMessage` object |
| 🗺️ | Add multi-resume batch comparison |
| 🗺️ | Export improved resume as downloadable PDF/DOCX |
| 🗺️ | Add scoring dashboard with radar chart visualization |
| 🗺️ | Support for multilingual resumes |
| 🗺️ | Plug in Mistral / Phi-3 as alternative local models |

<br/>

---

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you'd like to change.

```bash
# Fork → Clone → Branch → PR
git checkout -b feature/your-feature-name
git commit -m "feat: add your feature"
git push origin feature/your-feature-name
```

<br/>

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

<br/>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer&animation=twinkling" />

**Built with ❤️ and local LLaMA inference**

*No cloud. No cost. No compromise on privacy.*

[![Star this repo](https://img.shields.io/github/stars/your-username/ai-resume-agent?style=social)](https://github.com/your-username/ai-resume-agent)

</div>

from langchain_community.chat_models import ChatOllama

import json
import re
import io
import os
import PyPDF2
import numpy as np
import tempfile
from sklearn.metrics.pairwise import cosine_similarity

# LangChain & HuggingFace components
# from langchain_ollama import ChatOllama
# from langchain_community.chat_models import ChatOllama

from langchain_community.llms import Ollama
from typing import Optional
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    TextLoader,
)

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader
from langchain.schema import Document


class ResumeAnalysisAgent:

    def __init__(self, cutoff_score=75):
            # Initialization of parameters
            self.cutoff_score = cutoff_score
            self.resume_text = None
            self.rag_vectorstore = None  # This will be your FAISS index
            self.analysis_result = None
            self.jd_text = None
            self.extracted_skills = None
            self.resume_weaknesses = []
            self.resume_strengths = []
            self.improvement_suggestions = {}

            # Initialize LLaMA model (via Ollama)
            self.llm = ChatOllama(model="llama2")

            # HuggingFace Embeddings for FAISS
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            # Initialize the vector store (FAISS index) if necessary
            self.initialize_vector_store()

            self.vectorstore_path = "faiss_vectorstore"
            self.vectorstore = None
            self.resume_weaknesses = []

            if os.path.exists(self.vectorstore_path):
                print("Loading existing vector store...")
                self.vectorstore = FAISS.load_local(self.vectorstore_path, self.embeddings, allow_dangerous_deserialization=True)
            else:
                print("Vector store is not initialized. Creating it now...")
                self.create_vector_store()  # Automatically creates it

    def initialize_vector_store(self):
            """Initialize the vector store (FAISS index) if it doesn't exist."""
            vectorstore_path = "rag_vectorstore"
            if os.path.exists(vectorstore_path):
                print(f"Loading existing vector store from {vectorstore_path}...")
                # Load the existing vector store from disk
                self.rag_vectorstore = FAISS.load_local(vectorstore_path, self.embeddings)
                print("Vector store loaded successfully.")
            else:
                print("Vector store not found, creating a new one...")
                # If no vector store exists, create a new one
                if self.resume_text:
                    self.rag_vectorstore = self.create_rag_vector_store(self.resume_text)
                else:
                    print("Resume text is not available to create a vector store.")

    def _create_vector_store(self, resume_text: str):
        docs = [Document(page_content=resume_text)]
        index_path = "resume_faiss_index"
        self.rag_vectorstore = FAISS.from_documents(docs, self.embeddings)
        self.rag_vectorstore.save_local(index_path)

    def _load_vector_store(self):
        index_path = "resume_faiss_index"
        if os.path.exists(index_path):
            self.rag_vectorstore = FAISS.load_local(index_path, self.embeddings)


    def extract_text_from_pdf(self, pdf_file):
        """Extract text from a PDF file"""
        try:
            # Check if it's an uploaded file (e.g., from Streamlit or Flask)
            if hasattr(pdf_file, 'getvalue'):
                pdf_data = pdf_file.getvalue()
                pdf_file_like = io.BytesIO(pdf_data)
                reader = PyPDF2.PdfReader(pdf_file_like)
            else:
                reader = PyPDF2.PdfReader(pdf_file)

            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            return text.strip()
        except Exception as e:
            print(f"[PDF Extraction Error] {e}")
            return ""

    def extract_text_from_txt(self, txt_file):
        """Extract text from a plain text file (TXT)"""
        try:
            # If it's a file-like object (e.g., uploaded via Streamlit or Flask)
            if hasattr(txt_file, 'getvalue'):
                content = txt_file.getvalue()
                if isinstance(content, bytes):
                    return content.decode('utf-8')
                return str(content)
            else:
                # It's a file path
                with open(txt_file, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            print(f"[TXT Extraction Error] {e}")
            return ""

    def extract_text_from_file(self, file):
            """Extract text from a file (PDF or TXT)"""
            if hasattr(file, 'name'):
                file_extension = file.name.split('.')[-1].lower()
            else:
                file_extension = file.split('.')[-1].lower()

            if file_extension == 'pdf':
                return self.extract_text_from_pdf(file)
            elif file_extension == 'txt':
                return self.extract_text_from_txt(file)
            else:
                print(f"Unsupported file extension: {file_extension}")
                return ""
            
    from langchain_community.embeddings import HuggingFaceEmbeddings

    def create_rag_vector_store(self, text):
        """Create a vector store for RAG using LLaMA-compatible HuggingFace embeddings"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = text_splitter.split_text(text)

        # Use HuggingFace embeddings (lightweight + LLaMA compatible)
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        vectorstore = FAISS.from_texts(chunks, embeddings)
        return vectorstore

    from langchain_community.embeddings import HuggingFaceEmbeddings
    def embeddings(self):
            from langchain.embeddings import HuggingFaceEmbeddings
            return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")    

    def create_vector_store(self, text):
            """Create and return a vector store for skill analysis using Hugging Face embeddings."""
            
            # Wrap the input text in a Document object (FAISS works with Document objects)
            docs = [Document(page_content=text)]
            
            # Create the vector store (FAISS index) using the Hugging Face embeddings
            vectorstore = FAISS.from_documents(docs, self.embeddings)
            
            # Define the path to save the vector store
            vectorstore_path = "faiss_vectorstore"
            
            # Check if the directory exists, if not, create it
            if not os.path.exists(vectorstore_path):
                os.mkdir(vectorstore_path)
            
            # Save the vector store to disk for persistence
            try:
                vectorstore.save_local(vectorstore_path)
                print(f"Vector store created and saved at {vectorstore_path}.")
            except Exception as e:
                print(f"Error saving vector store: {e}")
                return None

            # Return the created vector store
            return vectorstore

    def load_vector_store(self):
            """Load the vector store from disk if it exists."""
            vectorstore_path = "faiss_vectorstore"
            
            if os.path.exists(vectorstore_path):
                try:
                    # Load the saved vector store from disk
                    self.rag_vectorstore = FAISS.load_local(vectorstore_path, self.embeddings)
                    print(f"Vector store loaded successfully from {vectorstore_path}.")
                except Exception as e:
                    print(f"Error loading vector store: {e}")
                    return None
            else:
                print(f"No vector store found at {vectorstore_path}. Please create one first.")
                return None

    def analyze_skill(self, qa_chain, skill):
        """Analyze a skill in the resume using a QA chain"""
        query = (
            f"On a scale of 0-10, how clearly does the candidate mention proficiency in {skill}? "
            f"Provide the numeric rating first, then a brief reasoning."
        )

        try:
            response = qa_chain.run(query).strip()
            print(f"[LLaMA Response] {response}")  # Optional: useful for debugging

            # Extract the numeric score
            match = re.search(r"\b(\d{1,2})\b", response)
            score = int(match.group(1)) if match else 0
            score = min(score, 10)  # Clamp score to 10 max

            # Extract reasoning
            reasoning = response
            if '.' in response:
                parts = response.split('.', 1)
                if len(parts) > 1:
                    reasoning = parts[1].strip()

            return skill, score, reasoning

        except Exception as e:
            print(f"[Skill Analysis Error] {e}")
            return skill, 0, "Unable to analyze skill."
            
    def analyze_resume_weaknesses(self):
        """Analyze specific weaknesses in the resume based on missing skills using LLaMA"""
        if not self.resume_text or not self.extracted_skills or not self.analysis_result:
            return []

        weaknesses = []

        for skill in self.analysis_result.get("missing_skills", []):
            # Initialize LLaMA LLM (Ollama must be running with a model like llama3 or mistral)
            llm = ChatOllama(model="llama3")  # or "mistral", "llama2", etc.

            prompt = f'''
            Analyze why the resume is weak in demonstrating proficiency in "{skill}".

            For your analysis, consider:
            1. What's missing from the resume regarding this skill?
            2. How could it be improved with specific examples?
            3. What specific action items would make this skill stand out?

            Resume Content:
            {self.resume_text[:3000]}...

            Provide your response in this JSON format:
            {{
                "weakness": "A concise description of what's missing or problematic (1-2 sentences)",
                "improvement_suggestions": [
                    "Specific suggestion 1",
                    "Specific suggestion 2",
                    "Specific suggestion 3"
                ],
                "example_addition": "A specific bullet point that could be added to showcase this skill"
            }}

            Return only valid JSON, no other text.
            '''

            try:
                response = llm.invoke(prompt).strip()

                # Try to load the response as JSON
                weakness_data = json.loads(response)
                weaknesses.append({
                    "skill": skill,
                    "score": self.analysis_result.get("skill_scores", {}).get(skill, 0),
                    "detail": weakness_data.get("weakness", "No specific details provided."),
                    "suggestions": weakness_data.get("improvement_suggestions", []),
                    "example": weakness_data.get("example_addition", "")
                })

            except json.JSONDecodeError:
                # Fallback if JSON is not returned, show raw response
                weaknesses.append({
                    "skill": skill,
                    "score": self.analysis_result.get("skill_scores", {}).get(skill, 0),
                    "detail": response[:200]  # Display a snippet of the raw response
                })

        self.resume_weaknesses = weaknesses
        return weaknesses

    def extract_skills_from_jd(self, jd_text):
        """Extract skills from a job description using LLaMA"""
        try:
            llm = ChatOllama(model="llama3")  # or "mistral", "llama2", etc.

            prompt = f"""
            Extract a comprehensive list of technical skills, technologies, and 
            competencies required from the following job description.

            Format the output strictly as a Python list of strings. Do NOT include any explanations or extra text.

            Job Description:
            {jd_text}
            """

            response = llm.invoke(prompt)
            skills_text = response.strip()

            # Try to extract list using regex
            match = re.search(r'\[(.*?)\]', skills_text, re.DOTALL)
            if match:
                skills_text = f"[{match.group(1)}]"

            try:
                skills_list = eval(skills_text)
                if isinstance(skills_list, list):
                    return [skill.strip() for skill in skills_list if isinstance(skill, str)]
            except Exception:
                pass

            # Fallback: Try to parse manually
            skills = []
            for line in skills_text.split('\n'):
                line = line.strip()

                if line.startswith('- ') or line.startswith('* '):
                    skill = line[2:].strip()
                    if skill:
                        skills.append(skill)

                elif line.startswith('"') and line.endswith('"'):
                    skill = line.strip('"')
                    if skill:
                        skills.append(skill)

            return skills

        except Exception as e:
            print(f"Error extracting skills from job description: {e}")
            return []
        
    # from langchain.embeddings import HuggingFaceEmbeddings

    def semantic_skill_analysis(self, resume_text, skills):
        """Performs semantic skill analysis using local HuggingFace embeddings."""
        try:
            # Initialize local embeddings (e.g., all-MiniLM-L6-v2)
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

            # Embed the resume text
            resume_embedding = np.array(embeddings.embed_query(resume_text)).reshape(1, -1)

            skill_scores = {}

            # Compare each skill with the resume embedding
            for skill in skills:
                skill_embedding = np.array(embeddings.embed_query(skill)).reshape(1, -1)
                similarity = cosine_similarity(resume_embedding, skill_embedding)[0][0]
                skill_scores[skill] = round(similarity, 2)

            return skill_scores

        except Exception as e:
            print(f"Error in semantic skill analysis: {e}")
            return {}

 


    def load_resume_file_from_path(self, file_path, suffix):
        from langchain_community.document_loaders import (
            PyPDFLoader,
            UnstructuredWordDocumentLoader,
            TextLoader,
        )

        supported_suffixes = [".pdf", ".docx", ".txt"]  # List of supported file types

        if suffix not in supported_suffixes:
            raise ValueError(f"Unsupported file type: {suffix}. Supported types are: {', '.join(supported_suffixes)}")

        if suffix == ".pdf":
            loader = PyPDFLoader(file_path)
        elif suffix == ".docx":
            loader = UnstructuredWordDocumentLoader(file_path)
        elif suffix == ".txt":
            loader = TextLoader(file_path)

        return loader.load()


    def analyze_resume(self, resume_file, role_requirements=None, custom_jd=None):
        import os

        file_name = resume_file.name.lower()
        suffix = os.path.splitext(file_name)[-1]  # Extract the file extension

        # Decode the file content if it's a text file
        if suffix == ".txt":
            resume_content = resume_file.read().decode("utf-8", errors="ignore")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding='utf-8') as tmp:
                tmp.write(resume_content)
                tmp_path = tmp.name
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(resume_file.read())
                tmp_path = tmp.name

        # Now load the file properly based on extension
        docs = self.load_resume_file_from_path(tmp_path, suffix)
        self.resume_text = docs[0].page_content
        vectorstore = self.create_vector_store(self.resume_text)

        # Create FAISS vector store
        self._create_vector_store(self.resume_text)

        skill_count = len(role_requirements) if role_requirements else 0
        return f"✅ Resume processed. Found {skill_count} skill requirement(s)."




    def ask_question(self, question):
        """Ask a question based on the resume's context using the vector store for retrieval."""
        try:
            # Ensure vector store exists
            if not hasattr(self, "rag_vectorstore") or self.rag_vectorstore is None:
                print("Vector store is not initialized. Run create_vector_store first.")
                return None

            # Perform similarity search in the vector store for relevant context
            docs = self.rag_vectorstore.similarity_search(question, k=3)
            context = "\n".join([doc.page_content for doc in docs])

            # Generate a response from the LLM (ChatOllama)
            llm = ChatOllama(model="llama3")  # Ensure model is valid and accessible
            response = llm.invoke(f"Based on the resume info below, answer the question:\n\n{context}\n\nQuestion: {question}")

            # Return the generated response
            return response.strip() if hasattr(response, "strip") else response

        except Exception as e:
            print(f"Error during question answering: {e}")
            return None


    def generate_interview_questions(self, question_types, difficulty, num_questions):
        """Generate interview questions based on strengths, weaknesses, and difficulty level."""
        try:
            # Ensure vector store exists
            if not hasattr(self, "vector_store") or self.vector_store is None:
                print("Vector store is not initialized. Run create_vector_store first.")
                return None

            # Analyze strengths and weaknesses using semantic analysis
            strengths, weaknesses = self.semantic_skill_analysis(self.resume_text, self.extracted_skills)

            # Construct the prompt for generating interview questions
            prompt = f"""
            Generate {num_questions} interview questions based on the candidate's strengths and weaknesses.

            - Strengths: {', '.join(strengths) if strengths else "Not available"}
            - Weaknesses: {', '.join(weaknesses) if weaknesses else "Not available"}
            - Question Types: {', '.join(question_types)}
            - Difficulty Level: {difficulty}

            Ensure the questions are relevant to the candidate's expertise level. 
            Format output as a numbered list of questions.
            """

            # Debug: Print the constructed prompt to verify
            print("Prompt for generating interview questions:", prompt)

            # Call LLaMA LLM to generate the questions
            llm = ChatOllama(model="llama3")  # Ensure the correct model is used
            response = llm.invoke(prompt)

            # Check if the response is valid and return the generated questions
            questions_text = response.strip() if hasattr(response, "strip") else response
            if questions_text:
                return questions_text.split("\n")  # Return as a list of questions
            else:
                print("No interview questions generated.")
                return []

        except Exception as e:
            print(f"Error generating interview questions: {e}")
            return []


    
    def improve_resume(self, improvement_areas, target_role=""):
        """Generate an improved version of the resume based on weaknesses and the target role."""
        try:
            # Ensure resume text exists
            if not hasattr(self, "resume_text") or not self.resume_text:
                print("Resume text not available. Extract text first.")
                return None

            # Construct improvement prompt
            prompt = f"""
            You are a professional resume writer. Your task is to rewrite and improve the given resume 
            while focusing on the specified improvement areas and aligning it with the target job role.

            - Target Role: {target_role if target_role else "General Improvement"}
            - Areas to Improve: {', '.join(improvement_areas)}

            Make the resume more professional, concise, and impactful. 
            Enhance clarity, quantify achievements, and improve readability while keeping it ATS-friendly.

            Resume to Improve:
            {self.resume_text[:3000]}...

            Return only the improved resume text. Do not include any explanation.
            """

            llm = ChatOllama(model="llama3")
            response = llm.invoke(prompt)

            improved_resume = response.strip() if hasattr(response, "strip") else response
            return improved_resume

        except Exception as e:
            print(f"Error improving resume: {e}")
            return None
        



    def generate_new_resume(self, target_role="", highlight_skills=""):
        """Generate a completely new, optimized resume based on the target role and highlighted skills."""
        try:
            # Ensure resume text exists
            if not hasattr(self, "resume_text") or not self.resume_text:
                print("Resume text not available. Extract text first.")
                return None

            # Construct prompt for LLM
            prompt = f"""
            You are a professional resume writer. Create a **brand new resume** for the given candidate 
            that is optimized for the target job role.

            - **Target Role:** {target_role if target_role else "General Resume"}
            - **Highlighted Skills:** {highlight_skills if highlight_skills else "Candidate's core strengths"}
            - **Missing Skills to Add:** Identify and include relevant missing skills based on the job role.
            - **Suggestions:** Improve clarity, structure, and readability. Use bullet points and concise descriptions.

            Format the resume professionally with clear sections.

            Resume Text:
            {self.resume_text}

            Output the **full improved resume**, ensuring it is **ATS-friendly** and tailored for recruiters.
            """

            # Use LLaMA model
            llm = ChatOllama(model="llama3")  # You can replace with "mistral", "llama2", etc. as needed
            response = llm.invoke(prompt)

            # Extract new resume text
            new_resume = response.content if response else "Error: No resume generated."

            return new_resume

        except Exception as e:
            print(f"Error generating new resume: {e}")
            return None


    def cleanup(self):
        """Clean up temporary files and cached data."""
        try:
            temp_paths = ["resume_file_path", "improved_resume_path", "vector_store_path"]

            for path_attr in temp_paths:
                if hasattr(self, path_attr):
                    path = getattr(self, path_attr)
                    if path and os.path.exists(path):
                        os.unlink(path)
                        print(f"Deleted: {path}")

        except Exception as e:
            print(f"Error cleaning up temporary files: {e}")

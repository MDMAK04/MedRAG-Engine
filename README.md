# 🧠 MedRAG-Engine 🩺
**Multimodal Agentic Medical Intelligence Platform (100% Local & Private)**

---

## 📌 Overview
**MedRAG-Engine** is a **100% local, private, and free** Medical Research Assistant. It leverages **Advanced RAG (Retrieval-Augmented Generation)** to analyze complex medical PDFs and answer intricate clinical questions with **traceable sources**.

Unlike standard cloud-based chatbots, this platform runs entirely on your machine using **Ollama** and **Qdrant**, ensuring **total patient data confidentiality** and **zero API costs**.

---

## ✨ Key Features
- 🔍 **Advanced Multi-Document RAG**: Ingests multiple PDFs, chunks them, embeds them, and retrieves the most relevant passages.
- 🧠 **Local LLM**: Powered by `Ollama` (`qwen2.5:7b`). No cloud dependency, no API keys, no data leaks.
- 📚 **Traceable Sources**: Automatically displays the exact **PDF file and page number** for every fact presented.
- 🤖 **Agentic AI**: Utilizes a **Supervisor** to intelligently classify queries and route them to specialized agents (RAG, General, Python Tool).
- 💬 **Dual Mode**:  
  - **Research Mode**: Ask specific questions about your uploaded PDFs.  
  - **General Chat Mode**: Ask general medical questions without any documents.
- 🎨 **Professional UI**: Built with Next.js and Tailwind CSS, featuring a collapsible sidebar and modern design.
- 🌍 **Multilingual Ready**: Architecture supports English, French, and Arabic.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | Next.js, TypeScript, Tailwind CSS |
| **Backend** | Python, FastAPI, REST APIs |
| **Vector DB** | Qdrant (Docker) |
| **Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` |
| **LLM** | Ollama (Local) - `qwen2.5:7b` |
| **Agents** | Supervisor, RAG, General, Python Tool |
| **DevOps** | Git, Docker, Local Deployment |

---
## 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │       User          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Next.js UI      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │       Backend       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Supervisor Agent   │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
      ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
      │   RAG Agent   │     │ Vision Agent  │     │ General Agent │
      └───────┬───────┘     └───────┬───────┘     └───────┬───────┘
              │                     │                     │
              ▼                     ▼                     ▼
        ┌──────────┐          ┌──────────┐          ┌──────────┐
        │  Qdrant  │          │  Ollama  │          │  Ollama  │
        └────┬─────┘          │  LLaVA   │          │ Qwen 2.5 │
             │                └──────────┘          └──────────┘
             ▼
       Retrieved Context
             │
             ▼
        Ollama Qwen
             │
             ▼
      Final Answer + Sources

```

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker Desktop
- Ollama (Download from [https://ollama.com](https://ollama.com))

### Step 1: Start Qdrant (Vector Database)
```bash
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant
```

### Step 2: Install Ollama & Download Model
```bash
# Modèle pour le texte
ollama pull qwen2.5:7b

# Modèle pour les images (Vision)
ollama pull llava:7b
```

### Step 3: Setup Python Backend
```bash
python -m venv MYENV
MYENV\Scripts\activate  # On Linux/macOS: source MYENV/bin/activate
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload --port 8000
```

### Step 4: Setup Frontend
```bash
cd frontend
npm install
npm run dev
```

### Step 5: Access the Application
Open your browser and go to: `http://localhost:3000`

---

## 🧪 How to Test
1. Click the **"+"** button to upload multiple PDFs.
2. Ask a comparative question such as:  
   *"Compare the risk factors for ischemic stroke across all the documents."*
3. Observe the structured response and the blue source pills at the bottom indicating the exact file and page.

---

## 🔒 Privacy & Security
- **Zero Cloud Dependency**: All inference is processed locally via Ollama.
- **Data Confidentiality**: Your medical documents never leave your machine.
- **Controlled Execution**: All Python analysis tools run in a controlled environment.

---

## 🏆 What This Project Demonstrates
- **Advanced RAG Pipeline Design** (Ingestion, Chunking, Vectorization, Retrieval).
- **Agentic AI Architecture** (Supervisor + Specialized Agents).
- **Multi-Document Analysis** (Synthesizing information from multiple sources).
- **Local/Private AI Deployment** (No external API dependencies).
- **Full-Stack Development** (FastAPI + Next.js).
- **Problem Solving** (Handling complex PDF parsing, multilingual support, and state management).

---

## 👨‍💻 Author
**MDMAK04**  
AI Engineer | Full-Stack Developer  
GitHub | LinkedIn

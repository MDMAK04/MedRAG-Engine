# 🧠 MedRAG-Engine 🩺

**Multimodal Agentic Medical Intelligence Platform (100% Local & Private)**

![CI/CD Status](https://github.com/MDMAK04/MedRAG-Engine/actions/workflows/deploy.yml/badge.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/elmakhloufi/medrag-backend)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Overview

**MedRAG-Engine** is a **100% local, private, and free** Medical Research Assistant. It leverages **Advanced RAG (Retrieval-Augmented Generation)** and **Multimodal AI** to analyze complex medical PDFs, images, and answer intricate clinical questions with **traceable sources**.

Unlike standard cloud-based chatbots, this platform runs entirely on your machine using **Ollama** and **Qdrant**, ensuring **total patient data confidentiality** and **zero API costs**.

---

## ✨ Key Features

- 🔍 **Advanced Multi-Document RAG**: Ingests multiple PDFs, chunks them, embeds them, and retrieves the most relevant passages.
- 🖼️ **Vision Agent**: Analyzes images, radiographs, and graphs directly uploaded by the user.
- 🧠 **Local LLM**: Powered by `Ollama` (`qwen2.5:7b` for text, `llava:7b` for vision). No cloud dependency, no API keys, no data leaks.
- 📚 **Traceable Sources**: Automatically displays the exact **PDF file and page number** for every fact presented.
- 🤖 **Agentic AI**: Utilizes a **Supervisor** to intelligently classify queries and route them to specialized agents (RAG, Vision, General, Python Tool).
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
| **LLM (Text)** | Ollama (Local) - `qwen2.5:7b` |
| **LLM (Vision)** | Ollama (Local) - `llava:7b` |
| **Agents** | Supervisor, RAG, Vision, General, Python Tool |
| **DevOps** | Docker, Docker Compose, GitHub Actions |
| **Cloud-Ready** | AWS (Terraform), Kubernetes (K8s) |

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

---

## 📦 Docker & CI/CD

Le projet est livré avec une architecture Microservices et un pipeline CI/CD complet.

### Images Docker (Publiées sur Docker Hub)
- **Backend**: `elmakhloufi/medrag-backend`
- **Frontend**: `elmakhloufi/medrag-frontend`
- **Vector DB**: `qdrant/qdrant` (Image officielle)

### 🚀 Lancer le projet avec Docker Compose

1. Installez Docker Desktop.

2. Téléchargez les modèles Ollama :
```bash
ollama pull qwen2.5:7b
ollama pull llava:7b
```

3. Clonez le dépôt :
```bash
git clone https://github.com/MDMAK04/MedRAG-Engine.git
cd MedRAG-Engine
```

4. Lancez tout avec une seule commande :
```bash
docker compose -f docker/docker-compose.yml up
```

5. Ouvrez votre navigateur sur `http://localhost:3000`.

### 🔄 CI/CD avec GitHub Actions

À chaque `git push` sur la branche `main`, un pipeline automatisé :
- Vérifie le code (installation des dépendances et tests).
- Construit les images Docker.
- Les publie automatiquement sur Docker Hub.

---

## ⚙️ Installation & Setup (Manuelle)

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker Desktop
- Ollama (Download from [https://ollama.com](https://ollama.com))

### Step 1: Start Qdrant (Vector Database)
```bash
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant
```

### Step 2: Install Ollama & Download Models
```bash
ollama pull qwen2.5:7b
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

### 📄 Test with Medical PDFs
1. Click the **"+"** button to upload multiple PDFs.
2. Ask a comparative question such as:  
   *"Compare the risk factors for ischemic stroke across all the documents."*
3. Observe the structured response and the blue source pills at the bottom indicating the exact file and page.

### 🩻 Test with Medical Images
1. Click the **"+"** button and upload a medical image (e.g., an X-ray).
2. Ask a question such as:  
   *"What is this image? Describe what you see in detail."*
3. The Vision Agent will analyze the image and provide a detailed description.

---

## ☁️ Cloud & MLOps

Le projet est conçu pour une architecture Cloud-Ready :

### AWS (Terraform)
- `deployment/terraform/main.tf` : Infrastructure as Code pour déployer sur AWS (S3, EC2, RDS).
- Prêt pour un déploiement cloud automatisé.

### Kubernetes (K8s)
- `k8s/deployment.yaml` : Déploiement de l'application.
- `k8s/service.yaml` : Exposition du service.
- Prêt pour l'orchestration à grande échelle.

---

## 🔒 Privacy & Security
- **Zero Cloud Dependency**: All inference is processed locally via Ollama.
- **Data Confidentiality**: Your medical documents and images never leave your machine.
- **Controlled Execution**: All Python analysis tools run in a controlled environment.

---

## 🏆 What This Project Demonstrates
- **Advanced RAG Pipeline Design** (Ingestion, Chunking, Vectorization, Retrieval).
- **Agentic AI Architecture** (Supervisor + Specialized Agents: RAG, Vision, General, Python).
- **Multimodal Analysis** (Analyzing PDFs, Images, Radiographs, and Graphs).
- **Multi-Document Analysis** (Synthesizing information from multiple sources).
- **Local/Private AI Deployment** (No external API dependencies).
- **Full-Stack Development** (FastAPI + Next.js).
- **MLOps & DevOps** (Docker, Docker Compose, GitHub Actions, CI/CD, Docker Hub).
- **Cloud-Ready** (Terraform, Kubernetes).
- **Problem Solving** (Handling complex PDF parsing, multilingual support, and state management).

---

## 👨‍💻 Author
**MDMAK04**  
AI Engineer | Full-Stack Developer  
GitHub: https://github.com/MDMAK04  
LinkedIn: https://linkedin.com/

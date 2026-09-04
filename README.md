# 🧠 MedRAG-Engine 🩺

**Multimodal Agentic Medical Intelligence Platform (100% Local & Private)**

![CI/CD Status](https://github.com/MDMAK04/MedRAG-Engine/actions/workflows/deploy.yml/badge.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/elmakhloufi/medrag-backend)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Overview

**MedRAG-Engine** is a **100% local, private, and free** Medical Research Assistant. It leverages **Advanced RAG (Retrieval-Augmented Generation)** and **Multimodal AI** to analyze complex medical PDFs, images, and answer intricate clinical questions with **accurate and contextualized answers**.

Unlike standard cloud-based chatbots, this platform runs entirely on your machine using **Ollama** and **Qdrant**, ensuring **total patient data confidentiality** and **zero API costs**.

---

## ✨ Key Features

- 🔍 **Advanced Multi-Document RAG**: Ingests multiple PDFs, chunks them, embeds them, and retrieves the most relevant passages.
- 🖼️ **Vision Agent**: Analyzes images, radiographs, and graphs directly uploaded by the user.
- 🧠 **Local LLM**: Powered by `Ollama` (`qwen2.5:7b` for text, `llava:7b` for vision). No cloud dependency, no API keys, no data leaks.
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
| **Cloud-Ready** | AWS (Terraform) |

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
      Final Answer
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

Les images sont disponibles publiquement sur Docker Hub pour faciliter le déploiement :

- **Backend** : [`elmakhloufi/medrag-backend`](https://hub.docker.com/r/elmakhloufi/medrag-backend)
- **Frontend** : [`elmakhloufi/medrag-frontend`](https://hub.docker.com/r/elmakhloufi/medrag-frontend)

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

MedRAG-Engine a été conçu avec une architecture **"Cloud-Ready"** et est livré avec des fichiers de configuration pour le déploiement automatisé.

### 🏗️ Infrastructure as Code (AWS avec Terraform)

Le dossier `deployment/terraform/` contient des scripts Terraform pour déployer l'infrastructure nécessaire sur AWS. Cette configuration permet de créer automatiquement :

- **S3** : Stockage des documents PDF.
- **RDS (PostgreSQL)** : Base de données pour les métadonnées.
- **EC2** : Serveur pour héberger la base de données vectorielle Qdrant.

**Fichiers inclus :**
- `main.tf` : Les ressources AWS (S3, RDS, EC2).
- `variables.tf` : Les variables de configuration (dont le mot de passe sécurisé de la base de données).
- `outputs.tf` : Les sorties de l'infrastructure (ex : IP de l'instance EC2).

> **Note de sécurité :** Les mots de passe et identifiants sensibles ne sont PAS dans le code. Ils sont stockés séparément dans `terraform.tfvars` (qui est ignoré par Git).

> **Note sur l'infrastructure :** 
> L'architecture cloud est entièrement modélisée via Terraform et prête à être déployée. Par souci de **bonne gestion des coûts cloud**, l'infrastructure n'est pas maintenue active en permanence, conformément aux limites du **Free Tier AWS**. Le code est 100% reproductible et peut être appliqué sur n'importe quel compte AWS en quelques minutes via la commande `terraform apply`.


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

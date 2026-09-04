# MedRAG-Engine

**A Local-First Medical Research Platform Powered by Advanced RAG and Multimodal AI**

![CI/CD Status](https://github.com/MDMAK04/MedRAG-Engine/actions/workflows/deploy.yml/badge.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/elmakhloufi/medrag-backend)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Overview

**MedRAG-Engine** is a sophisticated medical intelligence platform that combines Retrieval-Augmented Generation (RAG) with multimodal AI to extract and analyze evidence-based medical information. The platform operates entirely on your infrastructure using local models and vector databases, ensuring data confidentiality, compliance with healthcare privacy standards, and zero API dependencies.

Built with production-grade architecture, MedRAG-Engine enables healthcare professionals, researchers, and developers to create intelligent medical applications with complete control over data processing and model inference.

---

## Key Features

- **Multi-Document RAG Pipeline** — Efficiently ingests, chunks, vectorizes, and retrieves relevant passages from multiple PDFs with precise source attribution
- **Multimodal Analysis** — Processes both text documents and medical images (radiographs, graphs, diagnostic imaging)
- **Local LLM Inference** — Powered by Ollama with specialized models for text (`qwen2.5:7b`) and vision (`llava:7b`) tasks
- **Agentic Architecture** — Intelligent supervisor agent that routes queries to specialized agents (RAG, Vision, General, Python Tools)
- **Dual-Mode Operation**
  - **Research Mode** — Answer specific questions based on uploaded medical documents
  - **General Mode** — Query general medical knowledge without documents
- **Modern UI** — Production-ready interface built with Next.js, TypeScript, and Tailwind CSS
- **Multilingual Support** — Architecture supports English, French, and Arabic
- **Enterprise-Grade Deployment** — Docker containerization, CI/CD pipelines, and cloud-ready infrastructure

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Next.js, TypeScript, Tailwind CSS |
| **Backend** | Python, FastAPI |
| **Vector Database** | Qdrant |
| **Embeddings** | sentence-transformers (all-MiniLM-L6-v2) |
| **Text LLM** | Ollama (qwen2.5:7b) |
| **Vision LLM** | Ollama (llava:7b) |
| **Containerization** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **Infrastructure** | AWS, Terraform |

---

## Architecture

```
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
                   ┌───────────────┼───────────────┐
                   │               │               │
                   ▼               ▼               ▼
           ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
           │   RAG Agent   │   │ Vision Agent  │   │ General Agent │
           └───────┬───────┘   └───────┬───────┘   └───────┬───────┘
                   │                   │                   │
                   ▼                   ▼                   ▼
             ┌──────────┐         ┌──────────┐         ┌──────────┐
             │  Qdrant  │         │  Ollama  │         │  Ollama  │
             │(Vector DB)         │  LLaVA   │         │ Qwen 2.5 │
             └────┬─────┘         └──────────┘         └──────────┘
                  │
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

## Quick Start

### Prerequisites

- Python 3.11 or later
- Node.js 18 or later
- Docker Desktop
- Ollama ([download](https://ollama.com))

### Docker Compose (Recommended)

The fastest way to run MedRAG-Engine with all services:

```bash
# 1. Clone the repository
git clone https://github.com/MDMAK04/MedRAG-Engine.git
cd MedRAG-Engine

# 2. Pull required Ollama models
ollama pull qwen2.5:7b
ollama pull llava:7b

# 3. Start all services
docker compose -f docker/docker-compose.yml up

# 4. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
```

### Manual Installation

#### Step 1: Start Vector Database

```bash
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant
```

#### Step 2: Setup Ollama

```bash
ollama pull qwen2.5:7b
ollama pull llava:7b
```

#### Step 3: Install and Run Backend

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload --port 8000
```

#### Step 4: Install and Run Frontend

```bash
cd frontend
npm install
npm run dev
```

#### Step 5: Open Application

Visit `http://localhost:3000` in your browser.

---

## Usage Examples

### Medical Document Analysis

1. Click the upload button (**+**) to add PDF documents
2. Ask comparative or analytical questions:
   - *"Compare the risk factors for ischemic stroke across all uploaded documents"*
   - *"Summarize the treatment protocols for COVID-19 from these studies"*
3. Review the structured response with source attribution (document and page references)

### Medical Image Analysis

1. Upload a medical image (X-ray, CT scan, radiograph, etc.)
2. Ask for analysis:
   - *"Describe the findings in this chest X-ray"*
   - *"Identify any abnormalities in this image"*
3. The Vision Agent provides detailed clinical interpretation

---

## CI/CD and Deployment

### GitHub Actions Pipeline

On every `git push` to the `main` branch:
- Code validation (dependency installation and testing)
- Docker image building
- Automatic publishing to Docker Hub

**Published Images:**
- Backend: [`elmakhloufi/medrag-backend`](https://hub.docker.com/r/elmakhloufi/medrag-backend)
- Frontend: [`elmakhloufi/medrag-frontend`](https://hub.docker.com/r/elmakhloufi/medrag-frontend)

### Cloud Deployment (AWS with Terraform)

The entire cloud infrastructure is defined as code and can be deployed to AWS in minutes. Terraform configuration files are located in `deployment/terraform/`:

```
deployment/terraform/
├── main.tf          # AWS resources (S3, RDS, EC2)
├── variables.tf     # Configuration variables
└── outputs.tf       # Infrastructure outputs
```

**Infrastructure Components:**
- **S3 Bucket** — Secure document storage
- **RDS (PostgreSQL)** — Metadata and application database
- **EC2 Instance** — Qdrant vector database server
- **Security Groups & IAM Roles** — Network and access control

**Deployment:**
```bash
cd deployment/terraform
terraform init
terraform plan
terraform apply
```

> **Infrastructure Management:** The complete cloud architecture is fully reproducible and can be deployed to any AWS account within minutes using `terraform apply`. For cost optimization and compliance with AWS Free Tier limits, the infrastructure is designed to be spun up on-demand and torn down when not in use. All configuration is version-controlled and 100% repeatable, ensuring consistent deployments across environments.

**Security Note:** Sensitive credentials (database passwords, API keys) are stored in `terraform.tfvars` (git-ignored), never in version control.

---

## Security and Privacy

- **Zero Cloud Dependency** — All AI inference runs locally
- **Data Confidentiality** — Medical documents and images never leave your infrastructure
- **Controlled Execution** — Python tools run in sandboxed environments
- **Compliance-Ready** — Suitable for HIPAA, GDPR, and other healthcare privacy standards

---

## What This Project Demonstrates

- **Advanced RAG Implementation** — Production-grade document ingestion, chunking, vectorization, and retrieval pipeline
- **Agentic AI Architecture** — Supervisor pattern with specialized agents for different task types
- **Multimodal Processing** — Unified interface for text and vision-based analysis
- **Local/Private AI** — No external API dependencies or data transmission
- **Full-Stack Development** — FastAPI backend with Next.js frontend
- **Enterprise DevOps** — Docker, GitHub Actions, CI/CD, container registry integration
- **Infrastructure as Code** — Terraform configuration for reproducible cloud deployment
- **Production Readiness** — Error handling, logging, monitoring capabilities

---

## Project Structure

```
MedRAG-Engine/
├── backend/              # FastAPI application
│   ├── agents/          # Agent implementations
│   ├── rag/             # RAG pipeline
│   ├── vision/          # Vision processing
│   └── main.py          # Application entry point
├── frontend/            # Next.js application
│   ├── app/             # React components and pages
│   ├── public/          # Static assets
│   └── package.json     # Dependencies
├── deployment/          # Deployment configurations
│   ├── terraform/       # AWS infrastructure
│   └── docker/          # Docker compositions
└── docker/              # Docker build files
```

---

## Contributing

Contributions are welcome. Please ensure code follows the project's standards and include appropriate tests.

---

## License

MIT License — See LICENSE file for details

---

## Author

**MDMAK04**  
AI Engineer | Full-Stack Developer

- GitHub: [MDMAK04](https://github.com/MDMAK04)
- LinkedIn: [Your LinkedIn Profile]

---

## Acknowledgments

This project leverages excellent open-source tools:
- [Ollama](https://ollama.com) for local LLM inference
- [Qdrant](https://qdrant.tech) for vector database
- [sentence-transformers](https://www.sbert.net) for embeddings
- [FastAPI](https://fastapi.tiangolo.com) for backend framework
- [Next.js](https://nextjs.org) for frontend framework

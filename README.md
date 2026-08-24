<p align="center">
  <img src="https://img.shields.io/badge/Status-Completed-brightgreen" alt="Status">
  <img src="https://img.shields.io/badge/Python-3.11-blue" alt="Python">
  <img src="https://img.shields.io/badge/Next.js-14-black" alt="Next.js">
  <img src="https://img.shields.io/badge/License-MIT-orange" alt="License">
</p>

<h1 align="center">🧠 MedRAG-Engine 🩺</h1>

<p align="center">
  <b>Multimodal Agentic Medical Intelligence Platform (100% Local & Private)</b>
</p>

---

## 📖 Table of Contents
1. [📌 Overview](#-overview)
2. [✨ Key Features](#-key-features)
3. [🚀 Architecture](#-architecture)
4. [🎥 Demo & Screenshots](#-demo--screenshots)
5. [🛠️ Tech Stack](#️-tech-stack)
6. [⚙️ Installation & Setup](#️-installation--setup)
7. [🧪 How to Test](#-how-to-test)
8. [📊 Evaluation Metrics](#-evaluation-metrics)
9. [🔒 Privacy & Security](#-privacy--security)
10. [🏆 What This Project Demonstrates](#-what-this-project-demonstrates)
11. [📄 License](#-license)

---

## 📌 Overview
**MedRAG-Engine** is a **100% local, private, and free** Medical Research Assistant. It leverages **Advanced RAG (Retrieval-Augmented Generation)** to analyze complex medical PDFs and answer intricate clinical questions with **traceable sources**.

Unlike standard cloud-based chatbots, this platform runs entirely on your machine using **Ollama** and **Qdrant**, ensuring **total patient data confidentiality** and **zero API costs**.

---

## ✨ Key Features
- 🔍 **Advanced Multi-Document RAG**: Ingests multiple PDFs simultaneously, chunks them, embeds them, and retrieves the most relevant passages using semantic search.
- 🧠 **Local LLM**: Powered by `Ollama` (`qwen2.5:7b`). No cloud dependency, no API keys, no data leaks.
- 📚 **Traceable Sources**: Automatically displays the exact **PDF file and page number** for every fact presented (displayed in blue pills).
- 🤖 **Agentic AI**: Utilizes a **Supervisor** to intelligently classify queries and route them to specialized agents (RAG Agent, General Agent, Python Analysis Tool).
- 💬 **Dual Mode**:
  - **Research Mode**: Ask specific questions about your uploaded PDFs.
  - **General Chat Mode**: Ask general medical questions without any documents.
- 🎨 **Professional UI**: Built with Next.js and Tailwind CSS. Features a collapsible sidebar, clean modern design, and history tracking.
- 🌍 **Multilingual Ready**: Architecture supports English, French, and Arabic.
- ⚡ **Real-time Ingestion**: Automatically ingests PDFs into the vector database the moment they are uploaded.

---

## 🚀 Architecture
```text
User Interface (Next.js)
        ↓
API Gateway (FastAPI)
        ↓
AI Orchestrator / Supervisor
        ↓
      ├── RAG Agent (Multi-Document Retrieval)
      ├── General Agent (Knowledge based)
      └── Python Analysis Tool (Math/Calculations)
        ↓
Retrieval Layer (Qdrant Vector DB)
        ↓
Embedding Model (all-MiniLM-L6-v2)
        ↓
Local LLM (Ollama - qwen2.5:7b)
        ↓
Answer + Sources + Evidence
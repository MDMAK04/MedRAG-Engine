# 🧠 MedIntel-AI 🩺
### Multimodal Agentic Medical Intelligence Platform (Local & Private)

![Status](https://img.shields.io/badge/Status-Fully%20Functional-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![License](https://img.shields.io/badge/License-MIT-orange)

---

## 📖 Overview
**MedIntel-AI** is a **100% local, private, and free** Medical Research Assistant. It leverages **Advanced RAG (Retrieval-Augmented Generation)** to analyze medical PDFs and answer complex clinical questions with **traceable sources**. 

Unlike standard cloud-based chatbots, this platform runs entirely on your machine using **Ollama** and **Qdrant**, ensuring **total patient data confidentiality** and **zero API costs**.

---

## ✨ Key Features
- 🔍 **Advanced RAG**: Ingests PDFs, chunks them, embeds them, and retrieves the most relevant passages using semantic search.
- 🧠 **Local LLM**: Powered by `Ollama` (`qwen2.5:7b`) - No cloud dependency, no API keys, no data leaks.
- 📚 **Traceable Sources**: Automatically displays the exact **PDF file and page number** for every fact presented.
- 💬 **Dual Mode**: 
  - **Research Mode**: Ask specific questions about your uploaded PDFs.
  - **General Chat Mode**: Ask general medical questions without any documents.
- 🎨 **Professional UI**: Built with Next.js, Tailwind CSS, featuring a collapsible sidebar and a clean, modern design.
- 🌍 **Multilingual Ready**: Architecture supports English, French, and Arabic.

---

## 🏗️ Architecture
```text
User Interface (Next.js)
        ↓
API Gateway (FastAPI)
        ↓
AI Orchestrator / RAG Service
        ↓
Retrieval Layer (Qdrant Vector DB)
        ↓
Embedding Model (all-MiniLM-L6-v2)
        ↓
Local LLM (Ollama - qwen2.5:7b)
        ↓
Answer + Sources + Evidence
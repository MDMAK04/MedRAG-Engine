import requests
import json
import re

# Configuration Ollama
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:7b"

def classify_question(question: str) -> str:
    prompt = f"""
You are an AI Supervisor. Classify the following user question into exactly one of these categories:
- 'RAG' : If the question requires information from specific documents or PDFs.
- 'MATH' : If the question requires a calculation.
- 'GENERAL' : If the question is a general conversation or medical knowledge question without needing documents.

Output ONLY the category name (RAG, MATH, or GENERAL). Nothing else.

User question:
{question}
"""
    try:
        response = requests.post(
            url=f"{OLLAMA_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=30
        )
        response.raise_for_status()
        category = response.json().get("response", "").strip().upper()
        
        if "RAG" in category:
            return "RAG"
        elif "MATH" in category:
            return "MATH"
        else:
            return "GENERAL"
    except:
        return "GENERAL"

def python_tool(question: str) -> str:
    numbers = re.findall(r'\d+\.?\d*', question)
    
    if len(numbers) >= 2:
        try:
            values = [float(n) for n in numbers]
            average = sum(values) / len(values)
            return f"Calculated average: {average:.2f}"
        except:
            pass
    
    prompt = f"""
You are a calculator. Solve the following math problem. Output ONLY the result.
Problem: {question}
"""
    response = requests.post(
        url=f"{OLLAMA_URL}/api/generate",
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=30
    )
    return response.json().get("response", "").strip()

def rag_agent(question: str, pdf_names: list) -> dict:
    from Scripts.retrieval.retriever import retrieve_balanced
    
    pdf_names = [name.lower() for name in pdf_names]
    
    results = retrieve_balanced(question=question, pdf_names=pdf_names)
    
    context_parts = []
    
    for result in results:
        context_parts.append(
            f"FILE: {result.get('file_name')}, PAGE: {result.get('page')}\n{result.get('text', '')}"
        )
    
    context = "\n\n".join(context_parts) if context_parts else "No context retrieved."
    
    # PROMPT ASSOUPLI : Permet d'utiliser les connaissances générales si besoin
    prompt = f"""
You are MedIntel-AI, a medical research assistant.
Answer the user's question using the retrieved information provided below, AND your general medical knowledge if needed.
ALWAYS ANSWER IN ENGLISH.
Do not invent information.
If the exact statistics are not in the documents, explain what is known generally.

User question:
{question}

Retrieved medical evidence:
{context}
"""
    
    response = requests.post(
        url=f"{OLLAMA_URL}/api/generate",
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=180
    )
    
    raw_answer = response.json().get("response", "").strip()
    
    return {
        "answer": raw_answer
    }

def general_agent(question: str) -> str:
    prompt = f"""
You are MedIntel-AI, a helpful medical research assistant.
Answer the user's question concisely and accurately.
ALWAYS ANSWER IN ENGLISH.

User question:
{question}
"""
    response = requests.post(
        url=f"{OLLAMA_URL}/api/generate",
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=60
    )
    return response.json().get("response", "").strip()

def orchestrate(question: str, pdf_names: list) -> dict:
    print(f"\n[SUPERVISOR] Analyzing question: {question}")
    
    if pdf_names:
        pdf_names = [name.lower() for name in pdf_names]
        
        print(f"[SUPERVISOR] {len(pdf_names)} PDF(s) detected! Forcing RAG Agent...")
        print(f"[AGENT] Executing RAG Agent...")
        return rag_agent(question, pdf_names)
    
    category = classify_question(question)
    print(f"[SUPERVISOR] Category selected: {category}")
    
    if category == "MATH":
        print(f"[AGENT] Executing Python Analysis Tool...")
        result = python_tool(question)
        return {"answer": result}
    
    else:
        print(f"[AGENT] Executing General Agent...")
        answer = general_agent(question)
        return {"answer": answer}
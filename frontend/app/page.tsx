"use client";

import { useRef, useState, useEffect } from "react";

type SelectedFile = {
  id: string;
  file: File;
};

type Message = {
  role: "user" | "assistant";
  content: string;
};

type Research = {
  id: string;
  title: string;
  timestamp: number;
  messages: Message[];
};

export default function Home() {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const [question, setQuestion] = useState("");
  const [selectedFiles, setSelectedFiles] = useState<SelectedFile[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const [researches, setResearches] = useState<Research[]>([]);
  const [currentResearchId, setCurrentResearchId] = useState<string>("");
  const [showHistory, setShowHistory] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem("medrag_history");
    if (saved) {
      const parsed = JSON.parse(saved);
      setResearches(parsed);
    }

    const initialId = "research_" + Date.now() + "_" + Math.random().toString(36).substring(7);
    setCurrentResearchId(initialId);
  }, []);

  useEffect(() => {
    if (researches.length > 0) {
      localStorage.setItem("medrag_history", JSON.stringify(researches));
    }
  }, [researches]);

  function handleNewResearch() {
    if (messages.length > 0) {
      const firstQuestion = messages.find((m) => m.role === "user")?.content || "Untitled Research";
      const title = firstQuestion.substring(0, 50) + (firstQuestion.length > 50 ? "..." : "");

      const savedId = "research_" + Date.now() + "_" + Math.random().toString(36).substring(7);
      
      const savedResearch: Research = {
        id: savedId,
        title,
        timestamp: Date.now(),
        messages,
      };

      setResearches((prev) => {
        const filtered = prev.filter((r) => r.id !== currentResearchId);
        return [savedResearch, ...filtered];
      });
    }

    const newId = "research_" + Date.now() + "_" + Math.random().toString(36).substring(7);
    setCurrentResearchId(newId);
    setMessages([]);
    setQuestion("");
    setSelectedFiles([]);
    setShowHistory(false);
  }

  function handleLoadResearch(research: Research) {
    setCurrentResearchId(research.id);
    setMessages(research.messages);
    setQuestion("");
    setSelectedFiles([]);
    setShowHistory(false);
  }

  function handleDeleteResearch(id: string, e: React.MouseEvent) {
    e.stopPropagation();
    setResearches((prev) => prev.filter((r) => r.id !== id));

    if (id === currentResearchId) {
      handleNewResearch();
    }
  }

  async function handleFileSelect(event: React.ChangeEvent<HTMLInputElement>) {
    const files = Array.from(event.target.files || []);

    const pdfFiles = files.filter(
      (file) =>
        file.type === "application/pdf" ||
        file.name.toLowerCase().endsWith(".pdf")
    );

    setSelectedFiles((previous) => {
      const existingNames = new Set(previous.map((item) => item.file.name));

      const newFiles = pdfFiles
        .filter((file) => !existingNames.has(file.name))
        .map((file) => ({
          id: `${file.name}-${file.size}-${file.lastModified}-${Math.random()}`,
          file,
        }));

      return [...previous, ...newFiles];
    });

    for (const file of pdfFiles) {
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch("http://127.0.0.1:8000/api/upload", {
          method: "POST",
          body: formData,
        });
        
        if (response.ok) {
          console.log(`PDF ${file.name} ingested successfully!`);
        } else {
          console.error(`Error ingesting ${file.name}`);
        }
      } catch (error) {
        console.error("Upload error:", error);
      }
    }

    event.target.value = "";
  }

  function removeFile(id: string) {
    setSelectedFiles((previous) =>
      previous.filter((item) => item.id !== id)
    );
  }

  async function handleAsk() {
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading) {
      return;
    }

    setLoading(true);

    const userMessage: Message = {
      role: "user",
      content: trimmedQuestion,
    };

    setMessages((previous) => [...previous, userMessage]);

    setQuestion("");

    try {
      const formData = new FormData();

      formData.append("question", trimmedQuestion);
      formData.append("history", JSON.stringify(messages));

      const selectedPdfNames = selectedFiles.length > 0 
        ? selectedFiles.map((item) => item.file.name.toLowerCase()).join(",")
        : ""; 

      formData.append("selected_pdfs", selectedPdfNames);

      const response = await fetch(
        "http://127.0.0.1:8000/api/chat",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Backend error:", errorText);
        throw new Error(errorText || "Request failed.");
      }

      const data = await response.json();

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);
    } catch (error) {
      console.error("Chat error:", error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: "Unable to process your request. Check the backend terminal.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(event: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleAsk();
    }
  }

  return (
    <main className="min-h-screen bg-white text-slate-900 flex">
      <aside className={`${sidebarOpen ? 'w-[220px]' : 'w-0'} border-r border-slate-200 flex flex-col shrink-0 fixed left-0 top-0 h-screen overflow-hidden transition-all duration-300`}>
        <div className="w-[220px] px-5 py-5 border-b border-slate-200">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-600 to-cyan-500 text-white flex items-center justify-center shadow-md">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor" className="w-5 h-5">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
              </svg>
            </div>
            <div>
              <div className="font-bold text-sm tracking-tight">MedIntel-AI</div>
              <div className="text-[11px] text-slate-500">Medical AI Platform</div>
            </div>
          </div>
        </div>

        <div className="w-[220px] p-4">
          <button
            type="button"
            onClick={handleNewResearch}
            className="w-full bg-black text-white rounded-lg py-3 text-sm hover:bg-slate-800 transition"
          >
            + New research
          </button>
        </div>

        <div className="w-[220px] px-5 flex-1 overflow-y-auto">
          <div className="text-[11px] tracking-[0.2em] text-slate-400 mb-3">
            WORKSPACE
          </div>

          <button
            onClick={() => {
              setShowHistory(false);
              setMessages([]);
              setQuestion("");
              setSelectedFiles([]);
            }}
            className={`w-full text-left rounded-lg px-3 py-2 text-sm transition ${
              !showHistory && messages.length === 0
                ? "bg-slate-100 font-medium"
                : "text-slate-600 hover:bg-slate-100"
            }`}
          >
            Research
          </button>

          <button
            onClick={() => setShowHistory(!showHistory)}
            className={`w-full text-left mt-2 rounded-lg px-3 py-2 text-sm transition ${
              showHistory
                ? "bg-slate-100 font-medium"
                : "text-slate-600 hover:bg-slate-100"
            }`}
          >
            History ({researches.length})
          </button>

          {showHistory && (
            <div className="mt-4 space-y-2">
              {researches.length === 0 ? (
                <div className="text-xs text-slate-400 px-2">
                  No research saved yet
                </div>
              ) : (
                researches.map((research) => (
                  <div
                    key={research.id}
                    onClick={() => handleLoadResearch(research)}
                    className="group relative cursor-pointer"
                  >
                    <div className="border border-slate-200 rounded-lg p-3 hover:bg-slate-50 hover:border-slate-300 transition">
                      <div className="text-xs font-semibold text-slate-800 truncate mb-1">
                        {research.title}
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-[10px] text-slate-400">
                          {new Date(research.timestamp).toLocaleDateString()} 
                        </span>
                        <span className="text-[10px] bg-slate-100 rounded-full px-2 py-0.5">
                          {research.messages.length} msgs
                        </span>
                      </div>
                    </div>

                    <button
                      onClick={(e) => handleDeleteResearch(research.id, e)}
                      className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 text-slate-400 hover:text-red-600 text-lg leading-none transition"
                      aria-label="Delete research"
                    >
                      ×
                    </button>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      </aside>

      <section className={`flex-1 flex flex-col min-w-0 transition-all duration-300 ${sidebarOpen ? 'ml-[220px]' : 'ml-0'}`}>
        <header className="h-[70px] border-b border-slate-200 flex items-center justify-between px-8">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="w-8 h-8 rounded-lg border border-slate-300 flex items-center justify-center text-slate-600 hover:bg-slate-100 transition"
              title={sidebarOpen ? "Hide sidebar" : "Show sidebar"}
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
                <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
              </svg>
            </button>
            
            <div>
              <div className="font-bold text-lg">Medical Research Assistant</div>
              <div className="text-xs text-slate-500">
                Search and analyze scientific literature
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="border border-slate-200 rounded-full px-3 py-1.5 text-[10px] text-slate-600 bg-slate-50">
              ⚡ Powered by <span className="font-bold">Ollama</span>
            </div>
            
            <div className="border border-slate-200 rounded-full px-4 py-1.5 text-xs text-slate-600">
              <span className="inline-block w-2 h-2 rounded-full bg-green-500 mr-2" />
              System ready
            </div>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto px-8 py-10">
          {messages.length === 0 && !showHistory && (
            <div className="max-w-2xl mx-auto text-center pt-20">
              <div className="text-xs tracking-[0.25em] text-slate-400 mb-4">
                AI MEDICAL RESEARCH
              </div>

              <h1 className="text-4xl font-semibold mb-5">
                Research medical literature
              </h1>

              <p className="text-slate-500">
                Ask a medical research question or add PDFs to analyze their
                scientific content.
              </p>
            </div>
          )}

          <div className="max-w-3xl mx-auto space-y-8">
            {messages.map((message, index) => (
              <div
                key={index}
                className={
                  message.role === "user"
                    ? "flex justify-end"
                    : "flex justify-start"
                }
              >
                <div
                  className={
                    message.role === "user"
                      ? `
                          max-w-[80%]
                          bg-black
                          text-white
                          rounded-2xl
                          px-5
                          py-4
                          text-sm
                        `
                      : `
                          max-w-[90%]
                          text-slate-800
                          leading-7
                          text-sm
                        `
                  }
                >
                  {message.role === "assistant" && (
                    <div className="text-[11px] tracking-[0.2em] text-slate-400 mb-2">
                      MEDINTEL-AI
                    </div>
                  )}

                  <div className="whitespace-pre-wrap">
                    {message.content}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="border-t border-slate-200 p-6">
          <div className="max-w-3xl mx-auto">
            <div className="border border-slate-300 rounded-2xl overflow-hidden bg-white shadow-sm">
              <textarea
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={
                  selectedFiles.length > 0
                    ? "Ask a question about your PDFs..."
                    : "Ask a medical research question..."
                }
                rows={3}
                className="
                  w-full
                  resize-none
                  border-0
                  outline-none
                  px-5
                  pt-5
                  text-sm
                  placeholder:text-slate-400
                "
              />

              {selectedFiles.length > 0 && (
                <div className="px-4 py-2 flex flex-wrap gap-2">
                  {selectedFiles.map((item) => (
                    <div
                      key={item.id}
                      className="
                        flex
                        items-center
                        gap-2
                        bg-slate-100
                        border
                        border-slate-200
                        rounded-lg
                        px-3
                        py-2
                        text-xs
                      "
                    >
                      <span className="text-slate-500">PDF</span>
                      <span className="max-w-[180px] truncate">
                        {item.file.name}
                      </span>
                      <button
                        type="button"
                        onClick={() => removeFile(item.id)}
                        disabled={loading}
                        className="
                          text-slate-500
                          hover:text-black
                          text-base
                          leading-none
                          disabled:opacity-40
                        "
                        aria-label={`Remove ${item.file.name}`}
                      >
                        ×
                      </button>
                    </div>
                  ))}
                </div>
              )}

              <div className="flex items-center justify-between px-4 py-3 border-t border-slate-100">
                <div className="flex items-center gap-3">
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="application/pdf,.pdf"
                    multiple
                    onChange={handleFileSelect}
                    className="hidden"
                  />

                  <button
                    type="button"
                    onClick={() => fileInputRef.current?.click()}
                    disabled={loading}
                    className="
                      w-8
                      h-8
                      rounded-full
                      border
                      border-slate-300
                      flex
                      items-center
                      justify-center
                      text-slate-600
                      hover:bg-slate-100
                      disabled:opacity-40
                    "
                    title="Add PDF"
                  >
                    +
                  </button>

                  <span className="text-xs text-slate-500">
                    {selectedFiles.length === 0
                      ? "Add PDFs"
                      : `${selectedFiles.length} PDF${
                          selectedFiles.length > 1 ? "s" : ""
                        } selected`}
                  </span>
                </div>

                <button
                  type="button"
                  onClick={handleAsk}
                  disabled={loading || !question.trim()}
                  className="
                    bg-black
                    text-white
                    rounded-lg
                    px-5
                    py-2.5
                    text-sm
                    disabled:bg-slate-300
                    disabled:cursor-not-allowed
                    hover:bg-slate-800
                    transition
                  "
                >
                  {loading ? "Processing..." : "Ask"}
                </button>
              </div>
            </div>

            <div className="text-[11px] text-slate-400 mt-2 px-2">
              Enter to send · Shift + Enter for a new line
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
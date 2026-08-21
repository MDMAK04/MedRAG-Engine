"use client";

import { useRef, useState } from "react";

type SelectedFile = {
  id: string;
  file: File;
};

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function Home() {
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const [question, setQuestion] = useState("");

  const [selectedFiles, setSelectedFiles] =
    useState<SelectedFile[]>([]);

  const [messages, setMessages] =
    useState<Message[]>([]);

  const [loading, setLoading] = useState(false);

  // =========================================================
  // SELECT PDF
  // =========================================================

  function handleFileSelect(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    const files = Array.from(event.target.files || []);

    const pdfFiles = files.filter(
      (file) =>
        file.type === "application/pdf" ||
        file.name.toLowerCase().endsWith(".pdf")
    );

    setSelectedFiles((previous) => {
      const existingNames = new Set(
        previous.map((item) => item.file.name)
      );

      const newFiles = pdfFiles
        .filter((file) => !existingNames.has(file.name))
        .map((file) => ({
          id: `${file.name}-${file.size}-${file.lastModified}-${Math.random()}`,
          file,
        }));

      return [...previous, ...newFiles];
    });

    // Allow selecting the same file again
    event.target.value = "";
  }

  // =========================================================
  // REMOVE PDF
  // =========================================================

  function removeFile(id: string) {
    setSelectedFiles((previous) =>
      previous.filter((item) => item.id !== id)
    );
  }

  // =========================================================
  // ASK
  // =========================================================

  async function handleAsk() {
    const trimmedQuestion = question.trim();
  
    if (!trimmedQuestion || loading) {
      return;
    }
  
    if (selectedFiles.length === 0) {
      alert("Please select at least one PDF.");
      return;
    }
  
    setLoading(true);
  
    const userMessage: Message = {
      role: "user",
      content: trimmedQuestion,
    };
  
    setMessages((previous) => [
      ...previous,
      userMessage,
    ]);
  
    try {
      const formData = new FormData();
  
      // -----------------------------------------------------
      // Question
      // -----------------------------------------------------
  
      formData.append(
        "question",
        trimmedQuestion
      );
  
      // -----------------------------------------------------
      // History
      // -----------------------------------------------------
  
      formData.append(
        "history",
        JSON.stringify(messages)
      );
  
      // -----------------------------------------------------
      // Selected PDFs
      //
      // Example:
      //
      // Test.pdf,Test2.pdf
      // -----------------------------------------------------
  
      const selectedPdfNames = selectedFiles
        .map((item) => item.file.name)
        .join(",");
  
      formData.append(
        "selected_pdfs",
        selectedPdfNames
      );
  
      // -----------------------------------------------------
      // Debug
      // -----------------------------------------------------
  
      console.log(
        "Sending question:",
        trimmedQuestion
      );
  
      console.log(
        "Selected PDFs:",
        selectedPdfNames
      );
  
      // -----------------------------------------------------
      // Backend request
      // -----------------------------------------------------
  
      const response = await fetch(
        "http://127.0.0.1:8000/api/chat",
        {
          method: "POST",
          body: formData,
        }
      );
  
      // -----------------------------------------------------
      // Error handling
      // -----------------------------------------------------
  
      if (!response.ok) {
        const errorText =
          await response.text();
  
        console.error(
          "Backend error:",
          errorText
        );
  
        throw new Error(
          errorText ||
          "Request failed."
        );
      }
  
      // -----------------------------------------------------
      // Response
      // -----------------------------------------------------
  
      const data = await response.json();
  
      console.log(
        "Backend response:",
        data
      );
  
      // -----------------------------------------------------
      // Add assistant message
      // -----------------------------------------------------
  
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);
  
      // -----------------------------------------------------
      // Clear question
      // -----------------------------------------------------
  
      setQuestion("");
  
    } catch (error) {
  
      console.error(
        "Chat error:",
        error
      );
  
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "Unable to process your request. Check the backend terminal.",
        },
      ]);
  
    } finally {
      setLoading(false);
    }
  }

  // =========================================================
  // ENTER
  // =========================================================

  function handleKeyDown(
    event: React.KeyboardEvent<HTMLTextAreaElement>
  ) {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();

      handleAsk();
    }
  }

  return (
    <main
      className="
        min-h-screen
        bg-white
        text-slate-900
        flex
      "
    >

      {/* ================================================= */}
      {/* SIDEBAR */}
      {/* ================================================= */}

      <aside
        className="
          w-[220px]
          border-r
          border-slate-200
          flex
          flex-col
          shrink-0
        "
      >

        <div
          className="
            px-5
            py-5
            border-b
            border-slate-200
          "
        >

          <div
            className="
              flex
              items-center
              gap-3
            "
          >

            <div
              className="
                w-8
                h-8
                rounded-lg
                bg-black
                text-white
                flex
                items-center
                justify-center
                font-semibold
              "
            >
              M
            </div>

            <div>

              <div
                className="
                  font-semibold
                  text-sm
                "
              >
                MedIntel-AI
              </div>

              <div
                className="
                  text-xs
                  text-slate-500
                "
              >
                Medical Research
              </div>

            </div>

          </div>

        </div>

        <div className="p-4">

          <button
            type="button"
            className="
              w-full
              bg-black
              text-white
              rounded-lg
              py-3
              text-sm
            "
          >
            + New research
          </button>

        </div>

        <div className="px-5">

          <div
            className="
              text-[11px]
              tracking-[0.2em]
              text-slate-400
              mb-3
            "
          >
            WORKSPACE
          </div>

          <div
            className="
              bg-slate-100
              rounded-lg
              px-3
              py-2
              text-sm
            "
          >
            Research
          </div>

          <div
            className="
              px-3
              py-3
              text-sm
              text-slate-600
            "
          >
            History
          </div>

        </div>

      </aside>


      {/* ================================================= */}
      {/* MAIN */}
      {/* ================================================= */}

      <section
        className="
          flex-1
          flex
          flex-col
          min-w-0
        "
      >

        {/* HEADER */}

        <header
          className="
            h-[70px]
            border-b
            border-slate-200
            flex
            items-center
            justify-between
            px-8
          "
        >

          <div>

            <div
              className="
                font-semibold
              "
            >
              Medical Research Assistant
            </div>

            <div
              className="
                text-sm
                text-slate-500
              "
            >
              Search and analyze scientific literature
            </div>

          </div>

          <div
            className="
              border
              border-slate-200
              rounded-full
              px-4
              py-2
              text-xs
              text-slate-600
            "
          >

            <span
              className="
                inline-block
                w-2
                h-2
                rounded-full
                bg-green-500
                mr-2
              "
            />

            System ready

          </div>

        </header>


        {/* ================================================= */}
        {/* CHAT */}
        {/* ================================================= */}

        <div
          className="
            flex-1
            overflow-y-auto
            px-8
            py-10
          "
        >

          {messages.length === 0 && (

            <div
              className="
                max-w-2xl
                mx-auto
                text-center
                pt-20
              "
            >

              <div
                className="
                  text-xs
                  tracking-[0.25em]
                  text-slate-400
                  mb-4
                "
              >
                AI MEDICAL RESEARCH
              </div>

              <h1
                className="
                  text-4xl
                  font-semibold
                  mb-5
                "
              >
                Research medical literature
              </h1>

              <p
                className="
                  text-slate-500
                "
              >
                Ask a medical research question
                or add PDFs to analyze their
                scientific content.
              </p>

            </div>

          )}

          <div
            className="
              max-w-3xl
              mx-auto
              space-y-8
            "
          >

            {messages.map(
              (message, index) => (

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

                      <div
                        className="
                          text-[11px]
                          tracking-[0.2em]
                          text-slate-400
                          mb-2
                        "
                      >
                        MEDINTEL-AI
                      </div>

                    )}

                    <div
                      className="
                        whitespace-pre-wrap
                      "
                    >
                      {message.content}
                    </div>

                  </div>

                </div>

              )
            )}

          </div>

        </div>


        {/* ================================================= */}
        {/* INPUT */}
        {/* ================================================= */}

        <div
          className="
            border-t
            border-slate-200
            p-6
          "
        >

          <div
            className="
              max-w-3xl
              mx-auto
            "
          >

            <div
              className="
                border
                border-slate-300
                rounded-2xl
                overflow-hidden
                bg-white
                shadow-sm
              "
            >

              {/* QUESTION */}

              <textarea
                value={question}
                onChange={(event) =>
                  setQuestion(
                    event.target.value
                  )
                }
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


              {/* SELECTED FILES */}

              {selectedFiles.length > 0 && (

                <div
                  className="
                    px-4
                    py-2
                    flex
                    flex-wrap
                    gap-2
                  "
                >

                  {selectedFiles.map(
                    (item) => (

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

                        <span
                          className="
                            text-slate-500
                          "
                        >
                          PDF
                        </span>

                        <span
                          className="
                            max-w-[180px]
                            truncate
                          "
                        >
                          {item.file.name}
                        </span>

                        <button
                          type="button"
                          onClick={() =>
                            removeFile(item.id)
                          }
                          disabled={loading}
                          className="
                            text-slate-500
                            hover:text-black
                            text-base
                            leading-none
                            disabled:opacity-40
                          "
                          aria-label={
                            `Remove ${item.file.name}`
                          }
                        >
                          ×
                        </button>

                      </div>

                    )
                  )}

                </div>

              )}


              {/* BOTTOM BAR */}

              <div
                className="
                  flex
                  items-center
                  justify-between
                  px-4
                  py-3
                  border-t
                  border-slate-100
                "
              >

                <div
                  className="
                    flex
                    items-center
                    gap-3
                  "
                >

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
                    onClick={() =>
                      fileInputRef.current?.click()
                    }
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

                  <span
                    className="
                      text-xs
                      text-slate-500
                    "
                  >
                    {selectedFiles.length === 0
                      ? "Add PDFs"
                      : `${selectedFiles.length} PDF${
                          selectedFiles.length > 1
                            ? "s"
                            : ""
                        } selected`}
                  </span>

                </div>


                {/* ASK */}

                <button
                  type="button"
                  onClick={handleAsk}
                  disabled={
                    loading ||
                    !question.trim()
                  }
                  className="
                    bg-black
                    text-white
                    rounded-lg
                    px-5
                    py-2.5
                    text-sm
                    disabled:bg-slate-300
                    disabled:cursor-not-allowed
                  "
                >

                  {loading
                    ? "Processing..."
                    : "Ask"}

                </button>

              </div>

            </div>


            <div
              className="
                text-[11px]
                text-slate-400
                mt-2
                px-2
              "
            >
              Enter to send · Shift + Enter for a new line
            </div>

          </div>

        </div>

      </section>

    </main>
  );
}
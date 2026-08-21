"use client"

import { useState } from "react"

export default function Sidebar() {
  const [active, setActive] = useState("Research")

  return (
    <aside className="hidden w-[250px] shrink-0 border-r border-gray-200 bg-white lg:flex lg:flex-col">

      <div className="flex h-16 items-center border-b border-gray-200 px-6">

        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-black text-sm font-semibold text-white">
          M
        </div>

        <div className="ml-3">
          <div className="text-sm font-semibold tracking-tight">
            MedIntel-AI
          </div>

          <div className="text-xs text-gray-500">
            Medical Research
          </div>
        </div>

      </div>

      <div className="p-4">

        <button
          onClick={() => setActive("New research")}
          className="mb-6 flex w-full items-center justify-center rounded-lg bg-black px-4 py-3 text-sm font-medium text-white transition hover:bg-gray-800"
        >
          + New research
        </button>

        <div className="mb-3 px-2 text-[11px] font-semibold uppercase tracking-widest text-gray-400">
          Workspace
        </div>

        <button
          onClick={() => setActive("Research")}
          className={`mb-1 flex w-full items-center rounded-lg px-3 py-2.5 text-sm transition ${
            active === "Research"
              ? "bg-gray-100 font-medium text-black"
              : "text-gray-600 hover:bg-gray-50"
          }`}
        >
          Research
        </button>

        <button
          onClick={() => setActive("History")}
          className={`flex w-full items-center rounded-lg px-3 py-2.5 text-sm transition ${
            active === "History"
              ? "bg-gray-100 font-medium text-black"
              : "text-gray-600 hover:bg-gray-50"
          }`}
        >
          History
        </button>

      </div>

      <div className="mt-auto border-t border-gray-200 p-4">

        <div className="rounded-xl border border-gray-200 bg-gray-50 p-4">

          <div className="mb-2 text-[10px] font-semibold uppercase tracking-widest text-gray-400">
            Architecture
          </div>

          <div className="text-sm font-medium">
            Retrieval-Augmented Generation
          </div>

          <div className="mt-2 text-xs leading-5 text-gray-500">
            PMC
            {" → "}
            Embeddings
            {" → "}
            Qdrant
            {" → "}
            LLM
          </div>

        </div>

      </div>

    </aside>
  )
}
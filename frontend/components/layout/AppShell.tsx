"use client"

import { ReactNode } from "react"

type AppShellProps = {
  children: ReactNode
  onNewResearch?: () => void
}

export default function AppShell({
  children,
  onNewResearch,
}: AppShellProps) {
  return (
    <div className="h-screen overflow-hidden bg-white text-black">

      <div className="flex h-full">

        {/* SIDEBAR */}

        <aside className="flex h-full w-[220px] shrink-0 flex-col border-r border-gray-200 bg-white">

          {/* Logo */}

          <div className="border-b border-gray-200 px-5 py-4">

            <div className="flex items-center gap-3">

              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-black text-sm font-semibold text-white">
                M
              </div>

              <div>
                <div className="text-sm font-semibold">
                  MedIntel-AI
                </div>

                <div className="text-[11px] text-gray-500">
                  Medical Research
                </div>
              </div>

            </div>

          </div>


          {/* New research */}

          <div className="px-4 py-4">

            <button
              onClick={onNewResearch}
              className="w-full rounded-lg bg-black px-4 py-3 text-sm font-medium text-white transition hover:bg-gray-800"
            >
              + New research
            </button>

          </div>


          {/* Navigation */}

          <nav className="px-3">

            <div className="mb-2 px-2 text-[10px] font-semibold uppercase tracking-[0.18em] text-gray-400">
              Workspace
            </div>

            <button className="mb-1 w-full rounded-lg bg-gray-100 px-3 py-2.5 text-left text-sm font-medium text-black">
              Research
            </button>

            <button className="w-full rounded-lg px-3 py-2.5 text-left text-sm text-gray-600 transition hover:bg-gray-50 hover:text-black">
              History
            </button>

          </nav>


          {/* Architecture */}
{/* 
          <div className="mt-auto border-t border-gray-200 p-4">

            <div className="rounded-lg border border-gray-200 bg-gray-50 p-4">

              <div className="mb-3 text-[10px] font-semibold uppercase tracking-[0.18em] text-gray-400">
                Architecture
              </div>

              <div className="text-sm font-semibold">
                Retrieval-Augmented
                <br />
                Generation
              </div>

              <div className="mt-2 text-[11px] leading-5 text-gray-500">
                PMC → Embeddings → Qdrant → LLM
              </div>

            </div>

          </div> */}

        </aside>


        {/* MAIN APPLICATION */}

        <main className="flex min-w-0 flex-1 flex-col">

          {/* TOP BAR */}
{/* 
          <header className="flex h-[70px] shrink-0 items-center justify-between border-b border-gray-200 bg-white px-8">

            <div>

              <h1 className="text-sm font-semibold">
                Medical Research Assistant
              </h1>

              <p className="mt-1 text-xs text-gray-500">
                Search and analyze scientific literature
              </p>

            </div>


            <div className="flex items-center gap-2 rounded-full border border-gray-200 px-3 py-1.5">

              <span className="h-2 w-2 rounded-full bg-green-500" />

              <span className="text-xs text-gray-600">
                System ready
              </span>

            </div>

          </header> */}


          {/* ONLY THIS AREA SCROLLS */}

          <section className="min-h-0 flex-1 overflow-y-auto">

            {children}

          </section>

        </main>

      </div>

    </div>
  )
}
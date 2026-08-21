"use client"

import { useState } from "react"

export default function PdfUpload() {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState("")

  async function handleUpload() {
    if (!file) {
      setMessage("Please select a PDF.")
      return
    }

    if (file.type !== "application/pdf") {
      setMessage("Only PDF files are allowed.")
      return
    }

    setUploading(true)
    setMessage("Uploading and indexing PDF...")

    try {
      const formData = new FormData()
      formData.append("file", file)

      const response = await fetch(
        "http://127.0.0.1:8000/api/upload",
        {
          method: "POST",
          body: formData,
        }
      )

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.status}`)
      }

      const data = await response.json()

      setMessage(
        `PDF indexed successfully. ${data.chunks ?? 0} chunks added.`
      )

      setFile(null)
    } catch (error) {
      console.error(error)
      setMessage("Unable to upload the PDF.")
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="w-full max-w-5xl mx-auto px-8 pt-6">

      <div className="rounded-2xl border border-gray-200 bg-white p-5">

        <div className="flex items-center justify-between gap-4">

          <div>
            <h3 className="text-sm font-semibold text-black">
              Add medical document
            </h3>

            <p className="mt-1 text-xs text-gray-500">
              Upload a PDF to add it to the medical knowledge base.
            </p>
          </div>

          <div className="flex items-center gap-3">

            <label className="cursor-pointer rounded-lg border border-gray-300 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">

              Select PDF

              <input
                type="file"
                accept=".pdf,application/pdf"
                className="hidden"
                onChange={(event) => {
                  const selectedFile =
                    event.target.files?.[0] || null

                  setFile(selectedFile)
                  setMessage("")
                }}
              />

            </label>

            <button
              onClick={handleUpload}
              disabled={!file || uploading}
              className="rounded-lg bg-black px-4 py-2 text-sm font-medium text-white hover:bg-gray-800 disabled:cursor-not-allowed disabled:bg-gray-300"
            >
              {uploading ? "Indexing..." : "Upload"}
            </button>

          </div>
        </div>

        {file && (
          <div className="mt-4 rounded-lg bg-gray-50 px-4 py-3 text-sm text-gray-700">
            Selected file: {file.name}
          </div>
        )}

        {message && (
          <p className="mt-3 text-sm text-gray-500">
            {message}
          </p>
        )}

      </div>

    </div>
  )
}
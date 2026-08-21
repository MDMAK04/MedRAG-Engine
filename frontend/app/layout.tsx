import type { Metadata } from "next"
import "./globals.css"

export const metadata: Metadata = {
  title: "MedIntel-AI",
  description: "Medical literature research assistant powered by RAG",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
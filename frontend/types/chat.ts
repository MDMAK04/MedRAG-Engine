export interface Source {
  id?: number;
  chunk_id: string;
  pmcid: string;
  path: string;
  score: number;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
}

export interface ChatResponse {
  answer: string;
  sources: Source[];
}

export interface ChatRequest {
  question: string;
  history?: string;
  selected_pdfs?: string;
}
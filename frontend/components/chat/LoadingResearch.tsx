"use client";

export default function LoadingResearch() {
  return (
    <div className="flex justify-center py-10">
      <div className="w-full max-w-xl rounded-2xl border border-slate-800 bg-slate-950/70 p-8 text-center">
        <div className="mx-auto mb-5 h-10 w-10 animate-spin rounded-full border-2 border-slate-700 border-t-blue-500" />

        <h3 className="text-sm font-semibold text-white">
          Researching the literature
        </h3>

        <p className="mt-2 text-sm text-slate-400">
          Retrieving relevant evidence from Qdrant and generating the answer.
        </p>
      </div>
    </div>
  );
}
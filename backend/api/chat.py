from fastapi import APIRouter, Form, HTTPException # type: ignore
from typing import Optional

from backend.services.rag_service import ask_medintel


router = APIRouter()


@router.post("/chat")
async def chat(
    question: str = Form(...),
    selected_pdfs: str = Form(...),
    history: Optional[str] = Form(None),
):
    try:
        # -----------------------------------------------------
        # Convert:
        #
        # "Test.pdf,Test2.pdf"
        #
        # into:
        #
        # ["Test.pdf", "Test2.pdf"]
        # -----------------------------------------------------

        pdfs = [
            pdf.strip()
            for pdf in selected_pdfs.split(",")
            if pdf.strip()
        ]

        # -----------------------------------------------------
        # Validate question
        # -----------------------------------------------------

        if not question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question is required."
            )

        # -----------------------------------------------------
        # Validate PDFs
        # -----------------------------------------------------

        if not pdfs:
            raise HTTPException(
                status_code=400,
                detail="At least one PDF must be selected."
            )

        # -----------------------------------------------------
        # Logs
        # -----------------------------------------------------

        print("\n" + "=" * 60)
        print("MEDINTEL CHAT")
        print("=" * 60)

        print("Question:", question)
        print("Selected PDFs:", pdfs)

        # -----------------------------------------------------
        # RAG
        # -----------------------------------------------------

        result = ask_medintel(
            question=question,
            selected_pdfs=pdfs,
            history=history,
        )

        # -----------------------------------------------------
        # Response
        # -----------------------------------------------------

        return {
            "answer": result.get("answer", ""),
            "sources": result.get("sources", []),
        }

    except HTTPException:
        raise

    except Exception as e:
        print("\n" + "=" * 60)
        print("CHAT ERROR")
        print("=" * 60)

        print("Error type:", type(e).__name__)
        print("Error:", str(e))

        raise HTTPException(
            status_code=500,
            detail="Unable to process your request."
        )
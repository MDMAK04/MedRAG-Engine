from pathlib import Path

from fastapi import APIRouter, File, UploadFile, HTTPException

from Scripts.ingestion.pdf_ingestion import ingest_pdf


router = APIRouter()


# =========================================================
# CONFIGURATION
# =========================================================

UPLOAD_DIR = Path("Data/uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# UPLOAD PDF
# =========================================================

@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    # -----------------------------------------------------
    # Validate filename
    # -----------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    # Keep only the filename
    filename = Path(file.filename).name

    # -----------------------------------------------------
    # Validate extension
    # -----------------------------------------------------

    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    # -----------------------------------------------------
    # Save PDF
    # -----------------------------------------------------

    file_path = UPLOAD_DIR / filename

    try:

        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded PDF is empty."
            )

        with open(
            file_path,
            "wb"
        ) as buffer:

            buffer.write(content)

        print()
        print("=" * 60)
        print("PDF UPLOAD")
        print("=" * 60)

        print(
            f"Filename: {filename}"
        )

        print(
            f"Saved to: {file_path}"
        )

        print(
            f"Size: {len(content)} bytes"
        )

    except HTTPException:
        raise

    except Exception as e:

        print()
        print("UPLOAD ERROR")
        print(type(e).__name__)
        print(str(e))

        raise HTTPException(
            status_code=500,
            detail="Could not save the uploaded PDF."
        )

    # -----------------------------------------------------
    # INGEST PDF
    # -----------------------------------------------------

    try:

        result = ingest_pdf(
            str(file_path)
        )

    except Exception as e:

        print()
        print("PDF INGESTION ERROR")
        print(type(e).__name__)
        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=f"PDF ingestion failed: {str(e)}"
        )

    # -----------------------------------------------------
    # Check ingestion result
    # -----------------------------------------------------

    if result.get("chunks", 0) == 0:

        if result.get("already_indexed"):

            return {
                "message": "PDF was already indexed.",
                "filename": filename,
                "chunks": 0,
                "already_indexed": True
            }

        raise HTTPException(
            status_code=422,
            detail="The PDF was uploaded but no text chunks were extracted."
        )

    # -----------------------------------------------------
    # Success
    # -----------------------------------------------------

    print()
    print("=" * 60)
    print("UPLOAD + INGESTION SUCCESS")
    print("=" * 60)

    print(
        f"Filename: {filename}"
    )

    print(
        f"Chunks indexed: {result['chunks']}"
    )

    return {
        "message": "PDF successfully uploaded and indexed.",
        "filename": filename,
        "chunks": result["chunks"],
        "already_indexed": result.get(
            "already_indexed",
            False
        )
    }
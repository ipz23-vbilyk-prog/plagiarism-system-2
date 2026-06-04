from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import os

from backend.app.core.auth import get_current_user
from backend.app.services.document_service import (
    process_document,
    get_history,
    get_document_by_id,
    delete_document
)

router = APIRouter()


@router.post("/check")
async def check_document(
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    return await process_document(
        file=file,
        username=user["email"]
    )


@router.get("/history")
async def history(
    user=Depends(get_current_user)
):
    return get_history(
        username=user["email"]
    )

@router.delete("/delete/{document_id}")
async def delete_doc(
    document_id: int,
    user=Depends(get_current_user)
):
    success = delete_document(
        username=user["email"],
        document_id=document_id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Документ не знайдено"
        )

    return {
        "success": True,
        "message": "Документ видалено"
    } 

@router.get("/report/{document_id}")
async def download_report(
    document_id: int,
    user=Depends(get_current_user)
):
    document = get_document_by_id(
        username=user["email"],
        document_id=document_id
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Документ не знайдено"
        )

    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    pdf_path = os.path.join(
        reports_dir,
        f"report_{document_id}.pdf"
    )

    pdfmetrics.registerFont(
        TTFont(
            "TimesNewRoman",
            "backend/app/fonts/times.ttf"
        )
    )

    pdf = canvas.Canvas(
        pdf_path,
        pagesize=A4
    )

    width, height = A4

    similarity = float(document["similarity"])
    originality = round(100 - similarity, 2)

    pdf.setFont("TimesNewRoman", 28)

    pdf.drawCentredString(
        width / 2,
        height - 80,
        "PLAGIARISM SYSTEM"
    )

    pdf.setFont("TimesNewRoman", 18)

    pdf.drawCentredString(
        width / 2,
        height - 120,
        "ЗВІТ ПРО ПЕРЕВІРКУ"
    )

    pdf.line(
        50,
        height - 140,
        width - 50,
        height - 140
    )

    pdf.setFont("TimesNewRoman", 14)

    pdf.drawString(
        60,
        height - 200,
        f"Документ: {document['filename']}"
    )

    pdf.drawString(
        60,
        height - 230,
        f"ID документа: {document['id']}"
    )

    pdf.drawString(
        60,
        height - 260,
        f"Схожість: {similarity}%"
    )

    pdf.drawString(
        60,
        height - 290,
        f"Оригінальність: {originality}%"
    )

    pdf.drawString(
        60,
        height - 320,
        f"Рівень: {document['level']}"
    )

    pdf.save()

    response = FileResponse(
        path=pdf_path,
        media_type="application/pdf"
    )

    response.headers["Content-Disposition"] = (
        f'attachment; filename="report_{document_id}.pdf"'
    )

    return response
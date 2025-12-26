from flask import Blueprint, render_template, request, redirect, session
from models.report import Report
from models.comment import Comment
from models.db import db
from ai.ocr import extract_text_from_pdf
from ai.ai_medical import analyze_medical_report
import os

user_bp = Blueprint("user_bp", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@user_bp.route("/upload", methods=["POST"])
def upload_report():
    # 🔐 Only users can upload
    if session.get("role") != "user":
        return redirect("/")

    file = request.files.get("report")
    if not file:
        return redirect("/dashboard")

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # ----------------------------------
    # 🛡 SAFE OCR (limited + non-blocking)
    # ----------------------------------
    try:
        text = extract_text_from_pdf(filepath)
    except Exception as e:
        print("OCR failed:", e)
        text = ""

    if not text:
        text = "No readable text could be extracted from this document."

    # ----------------------------------
    # 🧠 SAFE AI ANALYSIS
    # ----------------------------------
    try:
        summary = analyze_medical_report(text)
    except Exception as e:
        print("AI analysis failed:", e)
        summary = (
            "AI analysis could not be completed automatically. "
            "Please consult a healthcare professional for detailed interpretation."
        )

    # ----------------------------------
    # 💾 SAVE REPORT
    # ----------------------------------
    report = Report(
        health_id=session.get("health_id"),
        filename=file.filename,
        ai_summary=summary
    )

    db.session.add(report)
    db.session.commit()

    return redirect("/dashboard")
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
    if session.get("role") != "user":
        return redirect("/dashboard")

    file = request.files["report"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    text = extract_text_from_pdf(filepath)
    summary = analyze_medical_report(text)

    report = Report(
        health_id=session.get("health_id"),
        filename=file.filename,
        ai_summary=summary
    )

    db.session.add(report)
    db.session.commit()

    return redirect("/dashboard")

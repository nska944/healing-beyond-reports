from flask import Blueprint, render_template, request, redirect, session
from models.report import Report
from models.comment import Comment
from models.db import db
import os

doctor_bp = Blueprint("doctor_bp", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@doctor_bp.route("/doctor", methods=["GET", "POST"])
def doctor_dashboard():
    if session.get("role") != "doctor":
        return redirect("/dashboard")

    reports = []
    searched_health_id = None

    # Restore last searched patient
    if request.method == "GET" and session.get("last_health_id"):
        searched_health_id = session.get("last_health_id")
        reports = Report.query.filter_by(
            health_id=searched_health_id
        ).order_by(Report.timestamp.desc()).all()

    # New search
    if request.method == "POST":
        searched_health_id = request.form.get("health_id")
        session["last_health_id"] = searched_health_id

        reports = Report.query.filter_by(
            health_id=searched_health_id
        ).order_by(Report.timestamp.desc()).all()

    return render_template(
        "doctor.html",
        reports=reports,
        searched_health_id=searched_health_id
    )


@doctor_bp.route("/doctor/comment", methods=["POST"])
def add_comment():
    if session.get("role") != "doctor":
        return redirect("/dashboard")

    prescription = request.files.get("prescription")
    filename = None

    if prescription and prescription.filename:
        filename = prescription.filename
        prescription.save(os.path.join(UPLOAD_FOLDER, filename))

    comment = Comment(
        report_id=request.form.get("report_id"),
        doctor_email=session.get("email"),  # ✅ FIXED
        content=request.form.get("content"),
        prescription_file=filename
    )

    db.session.add(comment)
    db.session.commit()

    # Redirect back to same patient
    return redirect("/doctor")

from flask import Blueprint, render_template, request, redirect, session
from models.user import User
from models.db import db

admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route("/admin", methods=["GET", "POST"])
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect("/dashboard")

    # Add new user / doctor
    if request.method == "POST":
        email = request.form.get("email")
        role = request.form.get("role")

        if email and role:
            existing = User.query.filter_by(email=email).first()
            if not existing:
                user = User(email=email, role=role)
                db.session.add(user)
                db.session.commit()

        return redirect("/admin")

    users = User.query.order_by(User.role).all()
    return render_template("admin.html", users=users)

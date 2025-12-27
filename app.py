from flask import Flask, render_template, request, redirect, session
from models.db import db
from models.user import User
from models.report import Report
from config import *

import firebase_admin
from firebase_admin import credentials, auth as fb_auth
import os, json

from routes.admin import admin_bp
from routes.doctor import doctor_bp
from routes.user import user_bp
from routes.google_fit import fit_bp

# --------------------------------------------------
# 🔐 Firebase Admin Init
# --------------------------------------------------
if not firebase_admin._apps:
    firebase_key_json = os.getenv("FIREBASE_KEY")
    if not firebase_key_json:
        raise RuntimeError("❌ FIREBASE_KEY environment variable missing")

    cred = credentials.Certificate(json.loads(firebase_key_json))
    firebase_admin.initialize_app(cred)
    print("✅ Firebase initialized")

# --------------------------------------------------
# Flask App Setup
# --------------------------------------------------
app = Flask(__name__)

# 🔥 SESSION CONFIG (THIS FIXES REDIRECT LOOP)
app.secret_key = SECRET_KEY
app.config.update(
    SESSION_COOKIE_SECURE=True,      # Railway uses HTTPS
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="None"   # REQUIRED for OAuth
)

app.config.from_object("config")
db.init_app(app)

app.register_blueprint(admin_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(user_bp)
app.register_blueprint(fit_bp)

# --------------------------------------------------
# Routes
# --------------------------------------------------
@app.route("/")
def login():
    # ✅ If already logged in, don't show login again
    if session.get("role") == "admin":
        return redirect("/admin")
    if session.get("role") == "doctor":
        return redirect("/doctor")
    if session.get("role") == "user":
        return redirect("/dashboard")

    return render_template("login.html")


@app.route("/firebase_login", methods=["POST"])
def firebase_login():
    id_token = request.form.get("idToken")
    if not id_token:
        return "Missing token", 400

    try:
        decoded = fb_auth.verify_id_token(id_token)
    except Exception as e:
        print("Firebase auth error:", e)
        return "Authentication failed", 401

    email = decoded.get("email")
    if not email:
        return "Invalid Firebase user", 401

    user = User.query.filter_by(email=email).first()

    if not user:
        is_first = User.query.count() == 0
        role = "admin" if is_first else "user"
        user = User(email=email, role=role)
        db.session.add(user)
        db.session.commit()

    # 🔥 VERY IMPORTANT: DO NOT CLEAR AFTER SETTING
    session.clear()
    session["user_id"] = user.id
    session["email"] = email
    session["role"] = user.role
    session["health_id"] = user.health_id

    session.modified = True  # 🔑 force save

    print("✅ Logged in:", session)

    if user.role == "admin":
        return redirect("/admin")
    elif user.role == "doctor":
        return redirect("/doctor")
    else:
        return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():
    if session.get("role") != "user":
        return redirect("/")

    reports = Report.query.filter_by(
        health_id=session.get("health_id")
    ).order_by(Report.timestamp.desc()).all()

    return render_template(
        "dashboard.html",
        reports=reports,
        health_id=session.get("health_id")
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")



# --------------------------------------------------
# DB Init
# --------------------------------------------------
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

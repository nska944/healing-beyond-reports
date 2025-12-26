
import uuid
from models.db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    role = db.Column(db.String(20), default="user")
    health_id = db.Column(db.String(20), default=lambda: "HID-" + uuid.uuid4().hex[:8].upper())

import uuid
from models.db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    health_id = db.Column(db.String(36), unique=True, nullable=True)

    def __init__(self, email, role="user"):
        self.email = email
        self.role = role

        if role == "user":
            self.health_id = str(uuid.uuid4())
        else:
            self.health_id = None

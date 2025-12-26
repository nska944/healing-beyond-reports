from models.db import db
import datetime

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    health_id = db.Column(db.String(20))
    filename = db.Column(db.String(200))
    ai_summary = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # ✅ RELATIONSHIP
    comments = db.relationship(
        "Comment",
        backref="report",
        lazy=True,
        cascade="all, delete"
    )

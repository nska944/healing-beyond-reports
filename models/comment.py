from models.db import db
import datetime

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey("report.id"))
    doctor_email = db.Column(db.String(120))
    content = db.Column(db.Text)
    prescription_file = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

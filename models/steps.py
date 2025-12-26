from models.db import db
import datetime

class StepData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    steps = db.Column(db.Integer)
    date = db.Column(db.Date)

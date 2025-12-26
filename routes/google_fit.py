from flask import Blueprint, redirect, request, session
import requests, datetime
from models.steps import StepData
from models.db import db

fit_bp = Blueprint("fit_bp", __name__)

CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"
CLIENT_SECRET = "YOUR_GOOGLE_CLIENT_SECRET"
REDIRECT_URI = "http://127.0.0.1:5000/fit/callback"

@fit_bp.route("/fit/connect")
def connect_fit():
    auth_url = (
        "https://accounts.google.com/o/oauth2/auth"
        f"?client_id={CLIENT_ID}"
        "&response_type=code"
        "&scope=https://www.googleapis.com/auth/fitness.activity.read"
        f"&redirect_uri={REDIRECT_URI}"
    )
    return redirect(auth_url)


@fit_bp.route("/fit/callback")
def fit_callback():
    code = request.args.get("code")

    token_resp = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
        },
    ).json()

    access_token = token_resp.get("access_token")
    fetch_steps(access_token)
    return redirect("/dashboard")


def fetch_steps(token):
    headers = {"Authorization": f"Bearer {token}"}

    end = int(datetime.datetime.now().timestamp() * 1000)
    start = end - (7 * 86400000)

    body = {
        "aggregateBy": [{"dataTypeName": "com.google.step_count.delta"}],
        "bucketByTime": {"durationMillis": 86400000},
        "startTimeMillis": start,
        "endTimeMillis": end,
    }

    resp = requests.post(
        "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate",
        headers=headers,
        json=body,
    ).json()

    user_id = session.get("user_id")

    for bucket in resp.get("bucket", []):
        date = datetime.date.fromtimestamp(
            int(bucket["startTimeMillis"]) / 1000
        )
        steps = sum(
            point["value"][0]["intVal"]
            for dataset in bucket["dataset"]
            for point in dataset["point"]
        )

        db.session.add(
            StepData(user_id=user_id, steps=steps, date=date)
        )

    db.session.commit()

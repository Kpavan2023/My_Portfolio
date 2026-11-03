import os
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory

load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    return send_from_directory(app.root_path, "index.html")


@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()[:100]
    email = str(data.get("email", "")).strip()[:200]
    message = str(data.get("message", "")).strip()[:3000]

    if not (name and email and message) or "@" not in email:
        return jsonify({"status": "error", "error": "Invalid input"}), 400

    subject = f"New message from your portfolio: {name}"
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    try:
        send_email(subject, body, reply_to=email)
    except Exception as exc:
        app.logger.error("Email send failed: %s", exc)
        return jsonify({"status": "error", "error": "Could not send message"}), 500

    return jsonify({"status": "success"})


def send_email(subject, body, reply_to):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    if not sender or not password:
        raise RuntimeError("EMAIL_USER / EMAIL_PASS missing in .env")

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = sender
    msg["Reply-To"] = reply_to

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
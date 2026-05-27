import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from pathlib import Path

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# -------------------------
# Project paths (ROBUST)
# -------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
SUBSCRIBER_FILE = BASE_DIR / "data" / "subscribers.json"


# -------------------------
# Load subscribers
# -------------------------
def load_subscribers():
    try:
        print("Loading from:", SUBSCRIBER_FILE)

        if not SUBSCRIBER_FILE.exists():
            print("Subscriber file NOT FOUND")
            return []

        with open(SUBSCRIBER_FILE, "r") as f:
            data = json.load(f)
            return data.get("emails", [])

    except json.JSONDecodeError:
        print("Invalid JSON in subscribers file")
        return []

    except Exception as e:
        print(f"Error loading subscribers: {e}")
        return []


# -------------------------
# Format email message
# -------------------------
def format_message(data):
    return f"""
📢 FEDAN Foreign Exchange Rate Update

🕙 10 AM USD: {data.get('10AM')}
🕑 2 PM USD: {data.get('2PM')}

--------------------------------
Automated Alert System
FEDAN Rate Monitor Bot
"""


# -------------------------
# Send single email
# -------------------------
def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)

        server.send_message(msg)
        server.quit()

        print(f"Sent → {to_email}")

    except Exception as e:
        print(f"Failed → {to_email} | {e}")


# -------------------------
# Send alert to all users
# -------------------------
def send_alert(data):
    subscribers = load_subscribers()

    if not subscribers:
        print("No subscribers found")
        return

    subject = "FEDAN FX Rate Update"
    body = format_message(data)

    for email in subscribers:
        send_email(email, subject, body)
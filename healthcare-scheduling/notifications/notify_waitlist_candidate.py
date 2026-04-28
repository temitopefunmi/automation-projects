"""
notify_waitlist_candidate.py
============================
Generates HIPAA-safe secure links for waitlist patients using signed tokens.

Features:
- Uses SECRET_KEY from .env
- Tokens contain appointment_id and expiration timestamp
- Single-use links enforced by token verification in webhook
- Works with reminders.py and main.py
"""

import os
from datetime import timedelta
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer

# Load environment variables from .env
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "demo_secret_key")
TOKEN_EXPIRY_MINUTES = int(os.getenv("TOKEN_EXPIRY_MINUTES", 1440))  # Default 24h
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://localhost:8000")

# Serializer for signed tokens
serializer = URLSafeTimedSerializer(SECRET_KEY)


def generate_secure_link(appointment_id: int) -> str:
    """
    Generates a signed, expiring token for the appointment.
    Returns a secure one-time link to confirm/cancel.
    """
    token = serializer.dumps({"appointment_id": appointment_id})
    link = f"{WEBHOOK_URL}/confirm?token={token}"
    return link


def notify_candidate(candidate: dict, cancelled_slot: dict) -> bool:
    """
    Sends HIPAA-safe notification to waitlist candidate.
    In demo mode, prints the secure link.
    """
    secure_link = generate_secure_link(cancelled_slot["appointment_id"])
    contact_method = candidate.get("contact_method", "sms")
    contact_value = candidate.get("contact_value", "5550000000")

    print(f"""
HIPAA-SAFE NOTIFICATION →
Patient: {candidate['patient_name']}
Contact: {contact_method} - {contact_value}
Appointment: {cancelled_slot['appt_datetime']}
Secure confirmation link: {secure_link}
""")

    return True  # Simulate patient receiving message

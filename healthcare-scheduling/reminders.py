"""
reminders.py
-------------
Runs each morning to:
1. Send reminders for all scheduled patients.
2. Detect CANCELLED slots and send FIRST waitlist offer.
   (After this, the webserver takes over for all next responses.)

No cascading logic here. No looping to the next waitlist candidate.
Just one-time morning processing.
"""

import os
import pandas as pd
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv

# -------------------------------
# Load environment
# -------------------------------
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "demo_secret_key")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://localhost:8000")
APPOINTMENTS_FILE = os.getenv("APPOINTMENTS_FILE", "data/appointments.csv")
WAITLIST_FILE = os.getenv("WAITLIST_FILE", "data/waitlist.csv")

serializer = URLSafeTimedSerializer(SECRET_KEY)


# -------------------------------
# CSV utils
# -------------------------------
def load_csv(file, parse_date=False):
    if os.path.exists(file):
        return pd.read_csv(file, parse_dates=["appt_datetime"] if parse_date else None)
    return pd.DataFrame()


# -------------------------------
# Secure link generator
# -------------------------------
def generate_token(appointment_id):
    return serializer.dumps({"appointment_id": appointment_id})


def generate_links(appointment_id):
    token = generate_token(appointment_id)
    return {
        "yes": f"{WEBHOOK_URL}/confirm?token={token}&decision=yes",
        "no": f"{WEBHOOK_URL}/confirm?token={token}&decision=no"
    }


# -------------------------------
# MAIN MORNING RUN LOGIC
# -------------------------------
def morning_run():
    print("\n=== Morning Reminder Run ===")

    appointments = load_csv(APPOINTMENTS_FILE, parse_date=True)
    waitlist = load_csv(WAITLIST_FILE)

    if appointments.empty:
        print("No appointments found.")
        return

    # ---------------------------------------------------------
    # 1. Send reminders for all scheduled patients
    # ---------------------------------------------------------
    scheduled = appointments[appointments["status"] == "scheduled"]

    print(f"Sending reminders for {len(scheduled)} scheduled patients...")

    for _, row in scheduled.iterrows():
        appt_id = row["appointment_id"]
        patient = row["patient_name"]

        links = generate_links(appt_id)

        # In a real system: send SMS/email using provider integrations
        print(f"\n[Reminder] → {patient}")
        print(f" YES: {links['yes']}")
        print(f" NO : {links['no']}")

    # ---------------------------------------------------------
    # 2. Detect cancelled slots and send FIRST waitlist offer
    # ---------------------------------------------------------
    cancelled = appointments[appointments["status"] == "cancelled"]

    print(f"\nProcessing {len(cancelled)} cancelled slots for waitlist offers...")

    for _, slot in cancelled.iterrows():
        appt_id = slot["appointment_id"]
        provider = slot["provider"]
        appt_time = slot["appt_datetime"]

        # If this slot already got a waitlist offer, do nothing
        if slot["patient_name"].startswith("WL:"):
            print(f"Slot {appt_id} already assigned to waitlist candidate. Skipping.")
            continue

        # Find matching waitlist candidates
        waiting = waitlist[
            (waitlist["status"] == "waiting") &
            (waitlist["provider_requested"] == provider)
        ]

        if waiting.empty:
            print(f"No waitlist available for slot {appt_id}.")
            continue

        # Pick best match (highest urgency)
        best = waiting.sort_values("urgency", ascending=False).iloc[0]
        wl_name = best["patient_name"]
        wl_idx = best.name

        print(f"\nOffering slot {appt_id} to waitlist candidate: {wl_name}")

        # Update waitlist status to "offered"
        waitlist.at[wl_idx, "status"] = "offered"
        waitlist.at[wl_idx, "appointment_offered"] = appt_id
        waitlist.at[wl_idx, "offer_timestamp"] = datetime.now()

        # In a real system: send SMS/email
        links = generate_links(appt_id)
        print(f" [Waitlist Offer] → {wl_name}")
        print(f"  YES: {links['yes']}")
        print(f"  NO : {links['no']}")

        # Tag appointment so we know this is now a WL candidate
        appointments.loc[appointments["appointment_id"] == appt_id, "patient_name"] = f"WL:{wl_name}"

    # Save updates
    appointments.to_csv(APPOINTMENTS_FILE, index=False)
    waitlist.to_csv(WAITLIST_FILE, index=False)

    print("\n=== Morning run complete ===\n")


if __name__ == "__main__":
    morning_run()

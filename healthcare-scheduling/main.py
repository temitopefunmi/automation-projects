"""
main.py
--------
Nightly batch orchestrator for the scheduling system.

Responsibilities:
1. Clean up expired waitlist offers (no response within expiry window).
2. Free the slot and prepare it for next morning’s waitlist cycle.
3. Generate daily summary reports (confirmed, declined, unclaimed, tomorrow's schedule).
4. Pull fresh appointment/waitlist exports from EHR (optional hook).
5. Run lightweight analytics for admins.

This file does NOT send reminders or handle confirmations.
"""

import os
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

# ---------------------------------------
# Load environment variables
# ---------------------------------------
load_dotenv()
APPOINTMENTS_FILE = os.getenv("APPOINTMENTS_FILE", "data/appointments.csv")
WAITLIST_FILE = os.getenv("WAITLIST_FILE", "data/waitlist.csv")
CANCELLATION_LOG = os.getenv("CANCELLATION_LOG", "data/cancellation_log.csv")
WAITLIST_EXPIRY_HOURS = int(os.getenv("WAITLIST_EXPIRY_HOURS", 12))
REPORTS_DIR = os.getenv("REPORTS_DIR", "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)


# ---------------------------------------
# Utility functions
# ---------------------------------------
def load_csv(path, parse_dates=False):
    if not os.path.exists(path):
        return pd.DataFrame()
    if parse_dates:
        return pd.read_csv(path, parse_dates=["appt_datetime"])
    return pd.read_csv(path)


def save_csv(df, path):
    df.to_csv(path, index=False)


# ---------------------------------------
# Step 1 — Clean expired waitlist offers
# ---------------------------------------
def cleanup_expired_waitlist_offers(appointments, waitlist, logs):
    """
    An offer becomes 'expired' if:
        - waitlist.status == "offered"
        - offer_timestamp older than WAITLIST_EXPIRY_HOURS
    When expired:
        - revert the appointment slot to 'cancelled'
        - mark waitlist entry as 'expired'
        - append to cancellation_log
    """

    if waitlist.empty:
        return appointments, waitlist, logs

    cutoff = datetime.now() - timedelta(hours=WAITLIST_EXPIRY_HOURS)

    expired_mask = (
        (waitlist["status"] == "offered") &
        (pd.to_datetime(waitlist["offer_timestamp"]) < cutoff)
    )

    expired_offers = waitlist[expired_mask]

    for _, row in expired_offers.iterrows():
        appt_id = row["appointment_id"]
        patient_name = row["patient_name"]

        # Free the slot
        appt_mask = appointments["appointment_id"] == appt_id
        if appt_mask.any():
            appointments.loc[appt_mask, "status"] = "cancelled"

        # Mark waitlist entry as expired
        idx = row.name
        waitlist.at[idx, "status"] = "expired"

        # Log expiration
        new_log = pd.DataFrame([{
            "appointment_id": appt_id,
            "original_patient": patient_name,
            "appt_datetime": appointments.loc[appt_mask, "appt_datetime"].values[0],
            "decision": "expired",
            "timestamp": datetime.now()
        }])
        logs = pd.concat([logs, new_log], ignore_index=True)

    return appointments, waitlist, logs


# ---------------------------------------
# Step 2 — Generate daily summary reports
# ---------------------------------------
def generate_daily_report(appointments, waitlist, logs):
    """
    Creates a CSV or text report containing:
        - confirmations & declines today
        - expired/unclaimed offers
        - list of still-open/cancelled slots
        - schedule for tomorrow
    """

    today = datetime.now().strftime("%Y-%m-%d")

    report_path = os.path.join(REPORTS_DIR, f"report_{today}.txt")

    with open(report_path, "w") as f:
        f.write("=== DAILY SCHEDULING REPORT ===\n")
        f.write(f"Date: {today}\n\n")

        # Activity from logs
        f.write("---- Activity Today ----\n")
        today_logs = logs[pd.to_datetime(logs["timestamp"]).dt.date == datetime.now().date()]
        if today_logs.empty:
            f.write("No confirmations, declines, or expirations today.\n\n")
        else:
            f.write(today_logs.to_string(index=False) + "\n\n")

        # Tomorrow's schedule
        f.write("---- Tomorrow's Schedule ----\n")
        appt_tomorrow = appointments[
            pd.to_datetime(appointments["appt_datetime"]).dt.date ==
            (datetime.now() + timedelta(days=1)).date()
        ]

        if appt_tomorrow.empty:
            f.write("No appointments tomorrow.\n\n")
        else:
            f.write(appt_tomorrow.to_string(index=False) + "\n\n")

        # Open slots
        f.write("---- Open/Cancelled Slots ----\n")
        cancelled_slots = appointments[appointments["status"] == "cancelled"]
        if cancelled_slots.empty:
            f.write("No open/cancelled slots.\n")
        else:
            f.write(cancelled_slots.to_string(index=False) + "\n")

    return report_path


# ---------------------------------------
# Optional — Step 3: Import new EHR exports
# ---------------------------------------
def import_ehr_exports():
    """
    Stub function.
    In production, this would read fresh nightly exports from the EHR.
    e.g., replacing appointments.csv with new dataset.
    """
    return


# ---------------------------------------
# Main execution workflow
# ---------------------------------------
def run_nightly():
    print("Running nightly orchestration...")

    appointments = load_csv(APPOINTMENTS_FILE)
    waitlist = load_csv(WAITLIST_FILE)
    logs = load_csv(CANCELLATION_LOG)

    # Step 1 — cleanup
    appointments, waitlist, logs = cleanup_expired_waitlist_offers(
        appointments, waitlist, logs
    )

    # Step 2 — reporting
    report_path = generate_daily_report(appointments, waitlist, logs)

    # Save updates
    save_csv(appointments, APPOINTMENTS_FILE)
    save_csv(waitlist, WAITLIST_FILE)
    save_csv(logs, CANCELLATION_LOG)

    print(f"✓ Nightly run complete. Report saved to: {report_path}")


if __name__ == "__main__":
    run_nightly()

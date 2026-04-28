# validators.py
def validate_appointments(df):
    # simple check: must contain required columns
    required_cols = ["appointment_id","patient_name","provider","appt_datetime","duration_minutes","type","status"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Appointments CSV missing columns: {missing}")

def validate_waitlist(df):
    required_cols = ["waitlist_id","patient_name","provider_requested","preferred_times","urgency","contact_method","contact_value","status"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Waitlist CSV missing columns: {missing}")

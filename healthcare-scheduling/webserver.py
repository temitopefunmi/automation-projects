# webserver.py
"""
FastAPI webhook server (updated)
- Validates signed tokens (itsdangerous) with expiry + salt
- Enforces single-use tokens (persistent used_tokens store)
- Handles patient & waitlist responses
- On waitlist decline, automatically notifies the next best candidate
- Uses CSV files for data (appointments, waitlist, cancellation_log)
"""

import os
import json
from typing import Optional, Dict, Any
from threading import Lock
from datetime import datetime

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer, BadData, SignatureExpired

# -----------------------
# Config / env
# -----------------------
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "demo_secret_key")
TOKEN_SALT = os.getenv("TOKEN_SALT", "confirmation-salt")
TOKEN_EXPIRY_MINUTES = int(os.getenv("TOKEN_EXPIRY_MINUTES", 1440))
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://localhost:8000")

APPOINTMENTS_FILE = os.getenv("APPOINTMENTS_FILE", "data/appointments.csv")
WAITLIST_FILE = os.getenv("WAITLIST_FILE", "data/waitlist.csv")
CANCELLATION_LOG = os.getenv("CANCELLATION_LOG", "data/cancellation_log.csv")
USED_TOKENS_FILE = os.getenv("USED_TOKENS_FILE", "data/used_tokens.json")

# -----------------------
# Serializer for tokens
# -----------------------
serializer = URLSafeTimedSerializer(SECRET_KEY)

# -----------------------
# Threading lock (CSV + token file safety)
# -----------------------
csv_lock = Lock()

# -----------------------
# FastAPI app
# -----------------------
app = FastAPI(title="Healthcare Scheduling Webhook Server")

# -----------------------
# Models
# -----------------------
class ConfirmationRequest(BaseModel):
    token: str
    decision: str  # "yes" or "no"

# -----------------------
# Utility: persistent used-tokens store
# -----------------------
def _load_used_tokens() -> Dict[str, Any]:
    """Load persistent used token store (returns dict of token -> used_at)."""
    if not os.path.exists(USED_TOKENS_FILE):
        return {}
    try:
        with open(USED_TOKENS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_used_tokens(store: Dict[str, Any]):
    """Save the used token store to disk."""
    os.makedirs(os.path.dirname(USED_TOKENS_FILE) or ".", exist_ok=True)
    with open(USED_TOKENS_FILE, "w", encoding="utf-8") as f:
        json.dump(store, f, default=str)

def _mark_token_used(token: str):
    store = _load_used_tokens()
    store[token] = {"used_at": datetime.utcnow().isoformat()}
    _save_used_tokens(store)

def _is_token_used(token: str) -> bool:
    store = _load_used_tokens()
    return token in store

# -----------------------
# CSV helpers
# -----------------------
def load_csv(file_path: str, parse_appt_datetime: bool = False) -> pd.DataFrame:
    """
    Load a CSV safely. Only parse appt_datetime when requested (appointments file).
    """
    if os.path.exists(file_path):
        if parse_appt_datetime:
            return pd.read_csv(file_path, parse_dates=["appt_datetime"])
        else:
            return pd.read_csv(file_path)
    else:
        return pd.DataFrame()

def save_csv(df: pd.DataFrame, file_path: str):
    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
    df.to_csv(file_path, index=False)

# -----------------------
# Token validation (signed, expiry, single-use)
# -----------------------
def validate_token(token: str) -> Dict[str, Any]:
    """
    Validate signed token and enforce expiry + single-use.
    Expected token payload examples:
      - patient token: {"appointment_id": 10, "actor": "patient"}
      - waitlist token: {"appointment_id": 10, "waitlist_id": 3, "actor": "waitlist"}
    Returns the token payload as dict on success.
    Raises HTTPException on failure.
    """
    # Single-use check
    if _is_token_used(token):
        raise HTTPException(status_code=400, detail="Token already used")

    try:
        data = serializer.loads(token, salt=TOKEN_SALT, max_age=TOKEN_EXPIRY_MINUTES * 60)
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="Token expired")
    except BadData:
        raise HTTPException(status_code=400, detail="Invalid token")

    # Basic payload validation
    if "appointment_id" not in data or "actor" not in data:
        raise HTTPException(status_code=400, detail="Invalid token payload")

    return data

# -----------------------
# Notification helper (demo)
# -----------------------
def _notify_candidate(candidate_row: pd.Series, appointment_row: pd.Series, appointment_id: int, waitlist_id: Optional[int] = None):
    """
    Demo: print a notification for a candidate.
    In production, replace this with Twilio/Email integration.
    We generate a signed token that includes appointment_id, waitlist_id and actor='waitlist'
    """
    payload = {"appointment_id": int(appointment_id), "actor": "waitlist"}
    if waitlist_id is not None:
        payload["waitlist_id"] = int(waitlist_id)

    token = serializer.dumps(payload, salt=TOKEN_SALT)
    link = f"{WEBHOOK_URL}/confirm?token={token}"

    # Simulated message content
    contact_method = candidate_row.get("contact_method", "sms")
    contact_val = candidate_row.get("contact_value", "unknown")
    print(f"""
WAITLIST OFFER →
Candidate: {candidate_row.get('patient_name')}
Provider: {candidate_row.get('provider_requested')}
Appointment: {appointment_row.get('appt_datetime')}
Contact: {contact_method} - {contact_val}
Secure link: {link}
""")
    # Mark waitlist entry as 'offered' is handled by caller before this function is called.

# -----------------------
# Find next best candidate
# -----------------------
def _select_next_waitlist_candidate(waitlist_df: pd.DataFrame, provider: str) -> Optional[pd.Series]:
    """
    Select the next waitlist candidate for a provider.
    Strategy: filter by provider_requested==provider and status == 'waiting', then pick highest urgency.
    Returns the selected row (pandas Series) or None.
    """
    if waitlist_df.empty:
        return None

    candidates = waitlist_df[
        (waitlist_df.get("provider_requested") == provider) & (waitlist_df.get("status") == "waiting")
    ]
    if candidates.empty:
        return None

    selected = candidates.sort_values("urgency", ascending=False).iloc[0]
    return selected

# -----------------------
# Main webhook endpoint
# -----------------------
@app.post("/confirm")
def confirm_slot(request: ConfirmationRequest):
    """
    Endpoint to handle confirmations from patients and waitlist candidates.

    Flow:
    - Validate token (signed + expiry + single-use)
    - Decode payload; expect payload['actor'] == 'patient' or 'waitlist'
    - For 'patient':
        - decision == 'yes'  -> appointments.status = 'confirmed'
        - decision == 'no'   -> appointments.status = 'cancelled' and trigger first waitlist offer (mark waitlist 'offered')
    - For 'waitlist':
        - decision == 'yes'  -> assign waitlist candidate into appointment (appointments updated & waitlist confirmed)
        - decision == 'no'   -> mark waitlist entry 'declined' and notify next candidate
    - Log every action to cancellation_log.csv
    - Mark token as used (persistent)
    """
    # Validate token payload
    payload = validate_token(request.token)
    appointment_id = int(payload["appointment_id"])
    actor = payload.get("actor")
    decision = request.decision.lower()
    if decision not in ("yes", "no"):
        raise HTTPException(status_code=400, detail="Decision must be 'yes' or 'no'")

    with csv_lock:
        # Load dataframes (appointments with parsed datetimes)
        appointments = load_csv(APPOINTMENTS_FILE, parse_appt_datetime=True)
        waitlist = load_csv(WAITLIST_FILE, parse_appt_datetime=False)
        cancellation_log = load_csv(CANCELLATION_LOG, parse_appt_datetime=False)

        # Locate appointment row
        slot_rows = appointments[appointments["appointment_id"] == appointment_id]
        if slot_rows.empty:
            raise HTTPException(status_code=404, detail="Appointment not found")
        slot_idx = slot_rows.index[0]
        slot_row = slot_rows.iloc[0]

        timestamp = datetime.utcnow().isoformat()

        # Helper to append to cancellation_log
        def _append_log(entry: Dict[str, Any]):
            nonlocal cancellation_log
            df = pd.DataFrame([entry])
            cancellation_log = pd.concat([cancellation_log, df], ignore_index=True)

        if actor == "patient":
            patient_name = slot_row.get("patient_name")
            if decision == "yes":
                # Patient confirmed their booking
                appointments.at[slot_idx, "status"] = "confirmed"
                _append_log({
                    "appointment_id": appointment_id,
                    "actor": patient_name,
                    "decision": "yes",
                    "timestamp": timestamp
                })
            else:
                # Patient declined: mark cancelled and log
                appointments.at[slot_idx, "status"] = "cancelled"
                _append_log({
                    "appointment_id": appointment_id,
                    "actor": patient_name,
                    "decision": "no",
                    "timestamp": timestamp
                })

                # Trigger first waitlist offer for this provider (do not auto-fill)
                provider = slot_row.get("provider")
                candidate = _select_next_waitlist_candidate(waitlist, provider)
                if candidate is not None:
                    # Mark candidate as offered
                    candidate_idx = candidate.name
                    waitlist.at[candidate_idx, "status"] = "offered"

                    # Write CSVs now (appointments + waitlist status change)
                    save_csv(appointments, APPOINTMENTS_FILE)
                    save_csv(waitlist, WAITLIST_FILE)

                    # Notify candidate (demo: prints link). Include waitlist_id in token
                    _notify_candidate(candidate, slot_row, appointment_id, waitlist_id=int(candidate_idx))

                    # Log offer
                    _append_log({
                        "appointment_id": appointment_id,
                        "actor": candidate.get("patient_name"),
                        "decision": "offered",
                        "timestamp": timestamp
                    })

                # If no candidate, just persist cancelled status
        elif actor == "waitlist":
            # Waitlist candidate responding to an offer
            waitlist_id = payload.get("waitlist_id")
            if waitlist_id is None:
                raise HTTPException(status_code=400, detail="Missing waitlist_id in token")

            # Ensure waitlist_id exists in current waitlist DF
            if waitlist_id not in waitlist.index:
                raise HTTPException(status_code=404, detail="Waitlist entry not found")

            candidate_row = waitlist.loc[waitlist_id]
            candidate_name = candidate_row.get("patient_name")

            if decision == "yes":
                # Candidate accepts → fill the appointment
                appointments.at[slot_idx, "patient_name"] = candidate_name
                appointments.at[slot_idx, "status"] = "scheduled"

                # Update waitlist status to confirmed
                waitlist.at[waitlist_id, "status"] = "confirmed"

                _append_log({
                    "appointment_id": appointment_id,
                    "actor": candidate_name,
                    "decision": "yes",
                    "timestamp": timestamp
                })

            else:
                # Candidate declined the offer
                waitlist.at[waitlist_id, "status"] = "declined"

                _append_log({
                    "appointment_id": appointment_id,
                    "actor": candidate_name,
                    "decision": "no",
                    "timestamp": timestamp
                })

                # Notify next candidate (if any)
                provider = slot_row.get("provider")
                next_candidate = _select_next_waitlist_candidate(waitlist, provider)
                if next_candidate is not None:
                    next_idx = next_candidate.name
                    waitlist.at[next_idx, "status"] = "offered"
                    save_csv(waitlist, WAITLIST_FILE)

                    # Notify (demo: print)
                    _notify_candidate(next_candidate, slot_row, appointment_id, waitlist_id=int(next_idx))

                    _append_log({
                        "appointment_id": appointment_id,
                        "actor": next_candidate.get("patient_name"),
                        "decision": "offered",
                        "timestamp": datetime.utcnow().isoformat()
                    })

        else:
            raise HTTPException(status_code=400, detail="Invalid token actor")

        # Persist CSVs and mark token used
        save_csv(appointments, APPOINTMENTS_FILE)
        save_csv(waitlist, WAITLIST_FILE)
        save_csv(cancellation_log, CANCELLATION_LOG)
        _mark_token_used(request.token)

    return {"status": "success", "message": f"Processed appointment {appointment_id} as {actor}:{decision}"}

# -----------------------
# Demo helper: generate a token for testing
# -----------------------
@app.get("/generate_token_demo")
def generate_token_demo(appointment_id: int, actor: str = "patient", waitlist_id: Optional[int] = None):
    """
    Create a signed token for manual testing.
    - actor: 'patient' or 'waitlist'
    - if actor == 'waitlist', provide waitlist_id (index of row in waitlist.csv)
    """
    payload = {"appointment_id": int(appointment_id), "actor": actor}
    if actor == "waitlist":
        if waitlist_id is None:
            raise HTTPException(status_code=400, detail="waitlist_id required for waitlist actor")
        payload["waitlist_id"] = int(waitlist_id)

    token = serializer.dumps(payload, salt=TOKEN_SALT)
    link = f"{WEBHOOK_URL}/confirm?token={token}"
    return {"token": token, "link": link}

# Healthcare Appointment Automation System  
Automated reminders, cancellations, and waitlist management  
Built with Python, FastAPI, pandas, itsdangerous, and cron-based orchestration.

---

## 📌 Overview

This project simulates an automation layer that sits between a clinic's EHR and its
patient scheduling operations. It processes daily appointment exports, sends reminders,
handles real-time responses through secure links, and automatically fills cancelled
slots using an intelligent waitlist engine.

The system is fully demo-ready and ideal for automation engineering portfolios.

---

## 🎯 Core Components

### **1. reminders.py (Morning Job)**
- Sends reminders to all *scheduled* patients.
- Detects *cancelled* slots and notifies the most suitable waitlist candidate.
- Generates secure confirmation links using signed, timed tokens.

### **2. webserver.py (FastAPI Service)**
Handles all patient and waitlist responses:
- YES → confirms and logs.
- NO → cancels and backfills from waitlist.
- Enforces token expiry and single-use protection.
- Writes updates to CSV datasets.

### **3. main.py (Nightly Orchestration)**
- Cleans expired waitlist offers.
- Prepares summary reports for administrators.
- Refreshes next-day reminder queue.
- Optional: imports new CSVs from an EHR export.

---

## 🛡 Security & Token Handling
- Tokens encoded using `itsdangerous.URLSafeTimedSerializer`
- Expire automatically after configurable minutes
- Single-use enforced via state management
- No PHI stored — demo-safe structure

---

## 🚀 Running the Project

### 1. Install Dependencies
```bash
pip install -r requirements.txt

---

### 2. Start the Webserver
```bash
uvicorn webserver:app --reload --port 8000
```

The FastAPI webserver exposes endpoints for handling:

* Secure confirmation links
* Waitlist acceptance/decline
* Automatic slot reassignment
* Token validation and single-use enforcement
* Real-time updates to `appointments.csv`, `waitlist.csv`, and `cancellation_log.csv`

Once running, you can test the server at:

```
http://localhost:8000/docs
```

---

### 3. Run Morning Reminders (`reminders.py`)

This script is intended to be executed first thing in the morning (e.g., via cron at 7 AM).
It performs **two distinct operations**:

### **A. Send reminders for scheduled appointments**

It loads all appointments where:

```
status = "scheduled"
```

and sends reminder SMS or email containing:

* Appointment date/time
* Provider
* YES/NO confirmation links with signed tokens

### **B. Handle overnight cancellations**

If any appointment already has:

```
status = "cancelled"
```

then **reminders.py** selects the **best matching waitlist candidate** and sends:

```
Waitlist offer → secure YES/NO link
```

Once this first offer is sent, the **webserver takes over** for all subsequent responses and cascading offers.

---

# 4. Run Nightly Orchestration (`main.py`)

This script is meant to run once each night (e.g., 11:59 PM). It serves as the system’s “daily brain”:

### Responsibilities

* Generate summary reports of:

  * Confirmations
  * Declines
  * Waitlist offers
  * No-responses and expired offers

* Clean expired waitlist offers

* Reset system state for the next day

* Import fresh CSV exports from the EHR (if applicable)

* Prepare any next-day batch notifications

* Run analytics (appointment fill rate, waitlist performance, etc.)

`main.py` does **no real-time work** — it’s purely batch and cleanup.

---

# 5. Architecture Overview

## High-Level Workflow Diagram (ASCII)

```
                 ┌─────────────────┐
                 │     EHR CSV     │
                 │  (Night Export) │
                 └────────┬────────┘
                          │
                          ▼
                  ┌────────────┐
                  │  main.py   │   (Nightly Orchestration)
                  │  - import  │
                  │  - cleanup │
                  │  - reports │
                  └──────┬─────┘
                         │
      ┌──────────────────┼──────────────────┐
      ▼                  ▼                  ▼
┌────────────┐    ┌──────────────┐   ┌───────────────┐
│appointments│    │waitlist.csv  │   │cancellation_log│
└─────┬──────┘    └──────┬───────┘   └─────────┬─────┘
      │                   │                     │
      │ (Morning)         │                     │
      ▼                   ▼                     ▼
┌──────────────┐   ┌──────────────┐     ┌──────────────┐
│ reminders.py │ → │ First WL Offer│ →  │  Logging      │
└──────┬───────┘   └──────────────┘     └──────────────┘
       │
       ▼  (Patient or Waitlist Responds via Token)
┌──────────────────────────┐
│      webserver.py        │
│ - Token validation       │
│ - YES/NO decisions       │
│ - Auto-refill from WL    │
│ - Write CSV updates      │
└──────────────────────────┘
```

---

# 6. Key System Responsibilities

### `reminders.py` — Morning Trigger

* Sends reminders to scheduled patients
* Detects cancelled slots and sends **first waitlist offer**
* Does NOT handle second/third offers
* Hands everything to `webserver.py`

### `webserver.py` — Real-Time Engine

* Processes YES/NO decisions
* Moves slots between scheduled/cancelled/offered/confirmed
* Cascades down the waitlist until someone accepts
* Enforces single-use tokens
* Logs all activity

### `main.py` — Nightly Automation

* Cleans expired offers
* Generates daily reporting
* Prepares tomorrow’s jobs
* Optionally loads EHR CSV exports
* Computes analytics

---

# 7. Data Model (CSV Format)

## **appointments.csv**

| appointment_id | patient_name | provider | appt_datetime | status    |
| -------------- | ------------ | -------- | ------------- | --------- |
| 10             | John Doe     | Dr. A    | 2025-01-03…   | scheduled |

Statuses:

* `scheduled`
* `cancelled`
* `offered` (slot temporarily held for waitlist candidate)
* `confirmed` (scheduled & confirmed)

---

## **waitlist.csv**

| patient_name | provider_requested | urgency | status  |
| ------------ | ------------------ | ------- | ------- |
| Jane Smith   | Dr. A              | 5       | waiting |

Statuses:

* `waiting`
* `offered`
* `confirmed`
* `declined`

---

## **cancellation_log.csv**

Full audit of everything: confirmations, declines, offers, timestamps.

---

# 8. Security Model

### **Token Security**

* Uses `itsdangerous.URLSafeTimedSerializer`
* Enforces:

  * Token expiry (default 24h)
  * Single-use (decision written to CSV — token unusable afterward)
  * Integrity protection

### **Data Safety**

* All CSV writes are protected with `threading.Lock`
* Prevents race conditions under concurrent webhooks

---

# 9. Demo Video Script (For Portfolio)

### **Duration: 2–3 minutes**

**Opening (5 seconds)**
“Hi, I’m Temi, and this is a healthcare appointment automation system I built.”

---

### **Scene 1 — Overview (20 sec)**

Show architecture diagram:

* Automated reminders
* Live confirmation links
* Instant waitlist refills
* Analytics & nightly cleanup

Explain:
“This simulates how clinics manage daily cancellations and waitlists without staff intervention.”

---

### **Scene 2 — Start the webserver (10 sec)**

Show `uvicorn` running.

---

### **Scene 3 — Morning reminders (30 sec)**

Run:

```bash
python reminders.py
```

Show SMS/email printout with secure token links.

---

### **Scene 4 — Patient declines via secure link (30 sec)**

Demonstrate:

* Opening the decline link
* Webserver logs
* Waitlist automatically receiving an offer

---

### **Scene 5 — Waitlist accepts the slot (30 sec)**

Click YES link for waitlist patient.

Show:

* appointments.csv updated
* waitlist.csv updated
* cancellation_log.csv updated

---

### **Scene 6 — Nightly orchestration (20 sec)**

Run:

```bash
python main.py
```

Show:

* Report generated
* Expired offers cleaned up

---

### **Closing (10 sec)**

“This project demonstrates healthcare automation, tokenized secure workflows, and real-time cascade scheduling.”

---

# 10. Limitations

* CSV-based storage (no DB)
* Single clinic, single provider-per-patient match
* No timezone normalization
* No email/SMS provider abstraction layer

---

# 11. Future Improvements (Version 2.0+)

### **Infrastructure**

* Move from CSV to PostgreSQL
* Add Alembic migrations
* Host FastAPI on Docker / Kubernetes

### **Workflow**

* Multi-provider matching rules
* Max-offer-count per patient
* Priority tiers (insurance, condition severity)

### **Security**

* Full login-protected admin dashboard
* Encrypted PHI fields
* Audit trails with hash signing

### **Integrations**

* Direct EHR API (Epic, Cerner, AthenaHealth)
* Twilio production SMS sender
* SendGrid or email-service abstraction

### **User Experience**

* Self-service waitlist portal
* Patient-facing mobile UI
* Real-time clinic dashboard

---





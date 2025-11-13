# 🩺 Medical Device Maintenance & Compliance Automation

**Overview**

This project demonstrates an **end-to-end workflow** for tracking, 
logging, and managing maintenance schedules of critical clinical devices, 
while ensuring operational compliance. It combines staff-driven form 
submissions, automated vendor email intake, processing logic, and 
reporting—all orchestrated in **Make (formerly Integromat)** with Google 
Sheets and Fillout forms.

The automation ensures clinics or healthcare organizations can maintain 
**device uptime**, track compliance, and generate actionable reports 
without manual effort, moving away from error-prone spreadsheets.

---

## ✨ Features

* **Device Maintenance Logging:** Staff submit maintenance data for 
existing or new devices via Fillout forms. Automatically updates the 
central Devices Sheet.
* **Vendor Email Intake:** Monitors vendor emails for device reports. 
**Parses CSV or plain-text reports** and logs them to the Maintenance Logs 
Sheet.
* **Automated Maintenance Status Checks:** Daily scheduled workflow 
evaluates overdue maintenance based on `NextDueDate`. Updates status and 
sends alerts if required.
* **Monthly Summary Reports:** Aggregates usage and maintenance data. 
Prepares dashboards or email summaries for operational review.
* **Data Consistency & Synchronization:** Handles new device IDs versus 
existing devices and ensures processed entries are only updated once.

---

## ⚙️ Tech Stack

| Component | Purpose |
| :--- | :--- |
| **Make (Integromat)** | Orchestration and automation of workflows |
| **Google Sheets** | Central data repository for devices and maintenance 
logs |
| **Fillout Forms** | Staff-facing forms for maintenance logging |
| **Gmail** | Vendor email intake |
| **Google Data Studio / Looker Studio (optional)** | Dashboards and 
reporting |

---

## 📂 Project Structure

| Scenario | Trigger | Description |
| :--- | :--- | :--- |
| **Scenario 1 — Vendor Email Intake** | `Gmail` → Watch Emails | Parses 
emails (plain text or CSV) and routes data to the Maintenance Logs Sheet. 
Supports multiple vendor formats via Router paths. |
| **Scenario 2 — Daily Maintenance Operations** | Scheduled (every 12 
hours) | Processes Maintenance Logs → Updates Devices Sheet → Checks 
overdue maintenance → Sends alerts. Marks processed rows to avoid 
duplicates. |
| **Scenario 3 — Monthly Reporting** | Scheduled monthly | Aggregate 
device usage and maintenance data to generate summary reports for 
operational review. |

---

## 💡 How It Works

1.  **Data Ingestion:** Staff submit maintenance logs through Fillout 
forms. Vendor reports are automatically collected from Gmail.
2.  **Daily Processing:** The daily scenario consolidates all incoming 
logs and updates the central **Devices Sheet**:
    * Updates last serviced date for existing devices.
    * Adds new devices when needed.
    * Checks for overdue maintenance.
    * Sends alerts via email/Slack (optional).
3.  **Reporting:** The monthly scenario aggregates this consolidated data 
and creates summary reports.

> **Note:** For demo purposes, the workflow is scheduled once daily. In 
production, it would be run more frequently or trigger automatically on 
new vendor email arrival for near real-time processing.

---

## 🛠️ Setup Instructions

### Google Sheets

Create two sheets:

* **`Devices`**: Stores all device info (ID, name, type, department, 
vendor, **last serviced**, **next due**, status, notes).
* **`Maintenance Logs`**: Records all maintenance entries (including a 
**`Processed`** column).

### Fillout Forms

* Set up forms for new and existing devices.
* *Pro-Tip:* Use URL parameters to prefill device data for existing 
devices, improving staff efficiency.

### Make Scenarios

1.  **Scenario 1:** `Gmail Watch` → `Parse` → `Maintenance Logs`.
2.  **Scenario 2:** Scheduled daily → `Process logs` → `Update devices`.
3.  **Scenario 3:** Scheduled monthly → `Aggregate reports`.

### Optional Dashboards

Connect the `Devices` Sheet to **Google Data Studio / Looker Studio** for 
visual compliance summaries.

---

## 📝 Demo Notes

* The workflow is designed to be easily **customizable** for frequency, 
vendors, and alerts.
* For production, workflows could be triggered in **real-time** when new 
vendor emails arrive.
* Device compliance and PHI considerations can be incorporated as needed.

## 🖼️ Sample Screenshots

(Include screenshots of Fillout form, Google Sheets, and Make scenario 
here)

---



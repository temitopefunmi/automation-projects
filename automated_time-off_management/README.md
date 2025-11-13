# ☀️ ZENITH PTO AUTOMATION

## Automated Leave and Attendance Management for Small Teams

**Overview**

Zenith PTO Automation is a lightweight HR automation system built to 
streamline leave requests, approvals, notifications, and monthly 
reminders. It integrates **Airtable**, **Zapier**, **Gmail (or Outlook)**, 
and **Fillout** to automate the entire leave management cycle—from 
employee request submission to HR tracking—without coding or manual 
follow-up.

---

## 🔑 Key Features

* **Multi-step leave approval and tracking** (Employee → Manager → HR).
* Automated email notifications for approvals and reminders.
* Leave balance calculation and reset logic.
* Manager proxy submission for staff without system access.
* Centralized **Airtable database** for employee and leave records.
* **Google Calendar integration** (optional) for visibility of approved 
leaves.
* HR monthly summary reminders sent automatically.
* Audit-safe records for reporting and compliance.

---

## ⚙️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Automation Platform** | Zapier |
| **Database** | Airtable |
| **Forms** | Fillout |
| **Communication** | Gmail or Outlook |
| **Scheduling** | Google Calendar (optional) |
| **Documentation** | Google Docs / Notion |

---

## 💼 Use Cases

* HR teams needing a simple, scalable PTO tracker.
* Companies managing hybrid or multi-location staff.
* Managers handling manual leave approval via email or spreadsheets.
* Small teams (20–50 employees) that require centralized reporting without 
an HRMS license.

---

## 📈 Value Proposition

This system **eliminates repetitive HR admin work**, ensures transparent 
leave tracking, and gives managers and HR real-time visibility over 
employee availability. The average setup saves **6–10 hours monthly** for 
HR and admin teams by reducing manual email handling, balance tracking, 
and report preparation.

---

## 🚧 Known Constraints

* Data accuracy depends on completeness of Airtable records.
* Limited to approved integrations and API access within Zapier’s scope.
* Static logic—adjustments require manual edits to workflow rules.

---

## 🚀 Deployment Guide

1.  Create **Airtable bases** for Employees, Leave Requests, Departments, 
and Holidays.
2.  Set up **Fillout form** linked to the `Leave Requests` table for staff 
submission.
3.  Configure **Zapier workflows**:
    * New request submission → Manager approval request.
    * Manager approval → HR notification and leave balance update.
    * Approved leave → Calendar event (optional).
    * Monthly scheduler → HR summary email.
4.  Test the workflow using sample requests.
5.  Document and hand over access credentials securely.

---

## 🔒 Security & Compliance

No sensitive medical or payroll data is stored. The system handles 
business contact and leave data only. Airtable encryption and Zapier’s 
HTTPS protocols ensure secure transmission.

---

## 🔄 Version & Updates

* **Current Version:** 1.0
* **Future plans** include Slack integration, attendance tracking, and 
dynamic accrual logic.

---


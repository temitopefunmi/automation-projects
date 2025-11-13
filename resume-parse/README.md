# Automated Resume Parsing Workflow

An end-to-end automated resume parsing workflow built with **Zapier**, 
integrating **Airtable**, **Slack**, **Monday.com**, and email 
notifications. This system extracts structured candidate data from 
resumes, scores candidates based on configurable criteria, and 
automatically routes them to relevant platforms, minimizing manual HR 
work.

---

## Features

- **Resume Parsing**: Extracts full name, contact info, work experience, 
education, skills, and certifications.
- **Candidate Scoring**: Computes a score based on experience, skills, 
education, and certifications.
- **Automated Routing**:
  - Sends rejection or next-step emails to candidates.
  - Posts notifications in Slack for team review.
  - Moves qualified candidates to Monday.com boards.
- **Multi-format Support**: Handles PDFs, DOCX, and text resumes, 
including multi-page documents.
- **Edge Case Handling**: Deals with missing fields, duplicates, or parser 
errors.
- **Audit & Logs**: Stores raw parser output for manual review and 
debugging.

---

## Tech Stack

- **Automation Platform**: Zapier
- **Resume Parsers**: Affinda, Rchilli, Sovren, or OpenAI GPT (AI-based 
fallback)
- **Database / Source**: Airtable
- **Collaboration & Notification**: Slack, Monday.com, Gmail/SMTP
- **Optional Internal Storage**: Supabase for structured candidate data
- **Scripting & Data Transformation**: Code by Zapier (JavaScript)

---

---

## Getting Started

### 1. Set up Airtable
- Create a table `Resumes` with the following fields:
  - `Resume ID`, `Uploaded At`, `Resume File`, `Full Name`, `Email`, 
`Phone`
  - `Parsed Raw`, `Work Experience`, `Education`, `Skills`, 
`Certifications`
  - `Score`, `Decision`, `Monday Item ID`, `Slack Notified`, `Parse 
Status`, `Notes`

### 2. Set up Zapier Workflow
- Trigger: New record or updated record in Airtable
- Parse resumes using your chosen parser (Affinda / Rchilli / OpenAI GPT)
- Normalize and validate output using `normalizer.js`
- Score candidates using `scoring.js`
- Route results: Slack, Monday.com, Gmail/SMTP

### 3. Configure Notifications
- Update Slack message templates in `templates/slack-messages.md`
- Update email templates in `templates/email-rejection.md` and 
`templates/email-next-step.md`

### 4. Testing
- Use sample resumes in `sample-data/`
- Run Zapier test workflow and verify Airtable updates, Slack 
notifications, and Monday.com items

---

## Optional Enhancements

- Integrate Supabase for persistent storage and reporting.
- Add duplicate detection to prevent multiple entries for the same 
candidate.
- Use AI prompt engineering to fine-tune OpenAI parsing outputs.
- Implement automated retries for failed parsing steps.

---

## Contributing

1. Fork the repository.
2. Make changes in a feature branch.
3. Update documentation as needed.
4. Submit a pull request for review.

---



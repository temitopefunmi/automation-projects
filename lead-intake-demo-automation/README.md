# Lead Intake & Demo Requests Automation (HealthTech Customization)

## Overview
This automation streamlines the capture, enrichment, and routing of 
**incoming leads and demo requests** for a HealthTech company. Using 
**n8n**, the system orchestrates multiple APIs and services to ensure 
every lead is logged, enriched, assigned, and followed up automatically.

**Key Objectives:**
- Capture Typeform submissions in real-time
- Enrich lead data via Apollo.io
- Log activity in Airtable (active leads + workflow logs)
- Assign leads to sales reps in Trello based on company size
- Sync leads to HubSpot CRM
- Automate follow-up emails (Day 0 & Day 3)
- Notify teams via Slack alerts and daily digest
- Reduce manual work and improve operational visibility

---

## Customization for HealthTech Demo Requests
This project includes a HealthTech-specific workflow for **demo 
requests**:
- Demo submissions are routed with priority
- Email sequences and Slack alerts are customized for demo follow-ups
- HubSpot contacts are tagged appropriately
- Managers receive daily metrics for demo request intake and completion

---

## Architecture
**Workflow Components:**
1. **Main Lead Routing Workflow**  
   - Trigger: Typeform submission  
   - Enrichment: Apollo.io API  
   - Logging: Airtable (Leads + Lead Logs)  
   - Notifications: Slack alerts  
   - CRM Sync: HubSpot  
   - Assignment: Trello based on company size  
   - Email: Day 0 sequence (demo vs general)

2. **Daily Digest & Day 3 Reminder Workflow**  
   - Trigger: Scheduled daily  
   - Aggregates lead outcomes (created, updated, duplicate, error)  
   - Sends Slack digest to managers  
   - Sends Day 3 reminder emails if no response

**Diagram:** *(insert architecture-diagram.png or Mermaid diagram here)*

---

## Tools & Services
- **n8n** (automation orchestration)
- **Typeform** (lead intake)
- **Apollo.io** (data enrichment)
- **Airtable** (Leads + Logs)
- **Slack** (alerts + daily digest)
- **HubSpot** (CRM sync)
- **Trello** (task assignment)
- **Gmail** (Day 0 & Day 3 emails)
- **Docker** (containerization)
- Optional: Node.js / Python scripts for custom logic

---

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/lead-intake-demo-automation.git
cd lead-intake-demo-automation

2. Copy and configure your .env file:
cp .env.example .env
# Fill in your API keys and credentials

3. Start the automation stack:
docker-compose up -d

4. Import workflows into n8n:

✔️pen n8n (http://localhost:5678)
✔mport JSON files from workflows/

5. Verify connections and test a Typeform submission.

## Expected Outcomes

- Saves 10–15 hours/week of manual work

- Ensures every lead/demo request is captured

- Automates follow-ups and notifications

- Provides manager visibility via Slack digest

- Reduces errors and duplicate entries

## Known Limitations

- Apollo enrichment may fail for unrecognized domains

- HubSpot free tier has API rate limits

- Day 3 reminders rely on Airtable timestamps (future version could 
integrate HubSpot Activity)

## Version & Updates

v1.0 – Initial setup: Lead intake, enrichment, Slack alerts, Day 0 email

v1.1 – Trello assignment & Day 3 email

v1.2 – Error handling branches added

v1.3 (planned) – Global error workflow & HubSpot Activity sync

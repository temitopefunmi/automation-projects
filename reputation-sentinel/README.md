# 🛡️ Reputation Sentinel

## Automated Sentiment & Compliance Monitoring System (n8n + Azure 
Functions)

Reputation Sentinel is an **intelligent workflow** designed to 
continuously monitor brand mentions, analyze sentiment, and alert teams 
about reputation-sensitive updates.

It runs autonomously every 15 minutes, fetching the latest mentions from 
trusted sources, evaluating their tone, and recording actionable 
insights—ensuring teams always stay ahead of the narrative.

---

## ⚙️ Features

* **Real-Time Monitoring:** Automatically fetches news mentions from 
**SerpAPI** on a 15-minute interval.
* **AI-Powered Sentiment Analysis:** Uses a lightweight, private **Azure 
Function API** (built with Python + VADER) to classify tone as Positive, 
Negative, or Neutral.
* **Smart Deduplication:** Compares new mentions with existing sheet data 
to avoid duplicates.
* **Data Logging:** Stores results in **Google Sheets** and **Airtable** 
for analytics, dashboards, or archiving.
* **Alerting System:** Sends **Slack** notifications when negative or 
sensitive news is detected.
* **Compliance-Friendly Design:** Entirely self-contained—no external AI 
services or data sharing. Ideal for regulated industries.

---

## 🧠 Tech Stack

| Category | Tools & Services |
| :--- | :--- |
| **Automation** | n8n (Cloud or Self-Hosted) |
| **Sentiment Engine** | Azure Function (Python + VADER) |
| **APIs** | SerpAPI, Slack, Google Sheets, Airtable |
| **Deduplication** | n8n Merge Node (Google Sheets + API Feed) |
| **Notifications** | Slack Bot Integration |

---

## 🧩 Workflow Overview

1.  **Trigger:** Scheduled every 15 minutes via n8n Cron node.
2.  **Fetch Mentions:** Collects the latest news articles or brand 
mentions using **SerpAPI**.
3.  **Data Formatting:** Cleans text and standardizes structure for 
sentiment input.
4.  **Sentiment Analysis:** Passes each mention through the **Azure 
Function API** for tone detection.
5.  **Deduplication:** Uses **Merge node** to exclude already-logged items 
from Google Sheets.
6.  **Storage:** Adds new, unique records to both **Google Sheets** and 
**Airtable**.
7.  **Alerts:** Sends **Slack** messages for any entries with negative 
sentiment.

---

## 🚀 Deployment Guide

### Step 1 — Prerequisites

Before setting up the system, ensure you have the following:

* A running **n8n** instance (Cloud or Docker Self-Hosted).
* A **SerpAPI** key for fetching mentions.
* A Google Cloud project connected to your **Google Sheets**.
* An **Airtable** base and API key.
* A **Slack** workspace with a webhook URL or bot token.
* An **Azure Function App** to host your sentiment analysis logic.

### Step 2 — Clone and Prepare Repository

```bash
git clone 
[https://github.com/yourusername/reputation-sentinel.git](https://github.com/yourusername/reputation-sentinel.git)
cd reputation-sentinel

### Step 3 — Deploy the Azure Function

1.  Inside the `azure-function` folder: Open `sentimentanalyzer.py` and 
confirm your environment has the following libraries: **`vaderSentiment`** 
and **`azure-functions`**.
2.  Install dependencies locally:
    ```bash
    pip install -r requirements.txt
    ```
3.  Deploy to Azure using the **CLI or portal**.
4.  **Copy the function’s public endpoint URL**—you’ll need it for the n8n 
HTTP Request node.

---

### Step 4 — Import Workflow into n8n

1.  Open your **n8n instance**.
2.  Click **Import Workflow** and select 
`workflow/reputation-sentinel.json`.
3.  Configure credentials for: **SerpAPI**, **Google Sheets**, 
**Airtable**, and **Slack**.
4.  In the **HTTP Request node** for sentiment analysis, replace the 
placeholder URL with your **Azure Function endpoint**.

---

### Step 5 — Test the Flow

1.  **Trigger manually** from the n8n editor.
2.  Check your **Google Sheet** for new records.
3.  Confirm your **Slack channel** receives alerts for negative results.

---

### Step 6 — Automate

Once verified, **enable the schedule trigger** to run automatically every 
**15 minutes**. Your system will now continuously scan for new mentions, 
log insights, and notify your team.

---

## 🔒 Known Limitations

* Works best with structured text data such as RSS or SerpAPI responses.
* Sentiment model uses **VADER**; domain-specific language (e.g., medical 
or legal) may need tuning.
* API rate limits apply depending on your SerpAPI plan.
* Slack notifications assume a single workspace webhook setup.

---

## 🧭 Future Enhancements

* Custom lexicons per industry (e.g., Healthcare, SaaS, Finance).
* Dashboard integration with Retool or Metabase.
* Multi-language sentiment support.
* Optional compliance tagging (e.g., GDPR flags).

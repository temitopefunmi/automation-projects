# 🧠 Compliance Assistant System

**Intelligent monitoring and classification system for compliance-related 
news and policy updates.**

This workflow automates the process of ingesting, deduplicating, 
classifying, and storing regulatory news while enabling contextual 
AI-powered chat retrieval using Supabase and LLMs.

---

## 🚀 Overview

The system automatically:
1. Fetches and classifies compliance-related news from RSS and Google News 
feeds.  
2. Extracts and embeds policy documents from Google Drive into a Supabase 
vector database.  
3. Enables AI chat and search over the combined context of news and 
policies.  
4. Deduplicates and caches processed items to ensure efficiency and 
scalability.

---

## 🏗️ Architecture

**Core components:**
- **n8n** — orchestration of all workflows (news ingestion, embeddings, 
chat).  
- **Supabase** — vector database for semantic search and context 
retrieval.  
- **OpenAI / Cohere API** — classification and embedding generation.  
- **Google Drive API** — fetches internal compliance or policy documents.  
- **Custom Frontend (optional)** — lightweight chat interface with RAG 
context.  

---

## ⚙️ Workflows

| Workflow | Purpose |
|-----------|----------|
| **News Ingestion** | Pulls RSS/Google News feeds, filters duplicates, 
and classifies content. |
| **Document Embedding** | Extracts text from policy PDFs, generates 
embeddings, and stores them in Supabase. |
| **Chat Workflow** | Responds to user queries using context from Supabase 
and LLM completions. |

---

## 🧩 Supabase Schema

File: `/sql/supabase_schema.sql`

Key columns:
- `id`: Primary key  
- `title`: News or document title  
- `content`: Extracted text  
- `metadata`: JSON object (includes hash, drive_id, category, date)  
- `embedding`: `vector(1024)`  
- `date`: Timestamp  

Search function:
```sql
select * from match_documents(
  query_embedding := <embedding>,
  match_count := 5
);

Metadata includes file hashes, drive IDs, and classification categories 
for flexible querying.


---

### 🔐 **7. Security & Reliability**

```markdown
## 🔐 Security & Reliability

- **Secret Management:** API keys isolated in environment variables and 
Docker configs.  
- **Credential Isolation:** Each service (Google, OpenAI, Supabase) uses 
scoped credentials.  
- **Rate Limiting:** Configurable API throttling via n8n + Express 
middleware.  
- **Deduplication:** Implemented via text hashing (`hash_documents.js`).  
- **Error Handling:** Retry + fallback logic in all HTTP nodes.  
- **Secure Data Flow:** HTTPS enforced on all inbound/outbound webhooks.  

## ⚡ Performance Enhancements

### 🧮 Caching
Prevents repeated AI classification or embedding requests for identical 
text content.  
Implemented via Supabase table checks or in-memory Redis cache (optional).

### 🧱 Batch Processing
Processes large feed batches efficiently using the `batch_processing.js` 
script — ensuring each batch is throttled and checkpointed before the next 
run.

## 💬 Chat Interface

The **Chat Interface** allows users to query the compliance knowledge base 
and receive AI-generated, context-aware responses.  
It works either through a simple **HTTP endpoint** or a **frontend chat 
UI**.

### 🔗 Endpoint
`POST https://your-n8n-domain/webhook/compliance-chat`

### 🧠 Example Request
```json
{
  "message": "What are the new GDPR updates this week?"
}

{
  "answer": "The European Data Protection Board released new guidance on 
cross-border data transfers on Oct 14, 2025..."
}


---

### 🧠 **10. AI Prompt Structure**

```markdown
## 🧠 AI Prompt Structure

```text
System: You are a compliance assistant. Use the provided documents and 
news summaries to answer accurately.
Context:
{{ matched_documents }}

User Query:
{{ message }}

Instruction:
Provide a concise, human-readable answer with regulatory references where 
relevant.

## Frontend (Optional)

A lightweight web-based chat interface is provided in the /frontend 
folder.
You can customize its branding, add authentication, or embed it in your 
internal dashboard.


---

## 🧠 AI Prompt Structure
```markdown
## 🧠 AI Prompt Structure

The AI model uses a structured prompt to ensure responses are factual, 
concise, and context-driven.  
This design combines system-level guidance with the user’s message and 
matched document embeddings.

### Prompt Template
```text
System: You are a compliance assistant. Use the provided documents and 
news summaries to answer accurately.

Context:
{{ matched_documents }}

User Query:
{{ message }}

Instruction:
Provide a concise, human-readable answer with regulatory references where 
relevant.

This structure ensures:

High relevance — by grounding responses in matched documents.

Consistency — uniform tone and factual accuracy.

Transparency — responses include context sources when possible.


---

## 🧰 Local Setup
```markdown
## 🧰 Local Setup

Follow these steps to set up and run the project locally.

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/automation-projects.git
cd compliance-news-ai
### 2️⃣  Configure Environment Variables

Create a .env file in the root directory:
OPENAI_API_KEY=
SUPABASE_URL=
SUPABASE_KEY=
GOOGLE_API_CREDENTIALS=

### 3️⃣  Launch via Docker

docker compose up -d

This starts:

n8n (workflow automation)

Supabase (database + embeddings)

Chat endpoint

###4️⃣ Import Workflows

Import the .json workflow files in the /workflows directory into your n8n 
instance.

###5️⃣ Test the Chat Endpoint

Use curl, Postman, or the web UI to test:
curl -X POST https://your-n8n-domain/webhook/compliance-chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What’s new in HIPAA compliance?"}'


---

## 📊 Example Use Cases

This system can serve as the backbone for several real-world compliance 
and research tools.

### 🏢 Enterprise Applications
- **Regulatory Intelligence Dashboard** – continuous tracking of global 
policy updates.  
- **Internal Compliance Chatbot** – employees can query company or 
industry regulations.  

### 💼 Industry-Specific
- **Fintech (KYC/AML)** – monitor updates to anti-money-laundering 
frameworks.  
- **Healthcare** – keep up with HIPAA or GDPR compliance changes.  

### 📚 Knowledge Management
- **Policy Knowledgebase** – create a searchable library of internal 
documents.  
- **Compliance Training Assistant** – interactive learning tool powered by 
your organization’s own materials.


## ☁️ Future Improvements

- Integration with **Azure OpenAI** for enterprise-grade deployments.  
- Redis caching for embeddings and LLM responses.  
- Workflow-based automated retraining (weekly vector refresh).  
- CloudWatch / Grafana integration for uptime and performance metrics.
- Full System Hosting (on Azure)😎

# 🌌 AgentVerse

> 🚀 Deploy AI Agents effortlessly — automate tasks, boost productivity, and transform workflows with intelligent automation.  
> We also use **[n8n-search-engine](https://github.com/AzamAliCodes/n8n-search-engine)** (custom workflow search with indexing & descriptions) inside AgentVerse workflows.

---

## ✨ One-liner
AgentVerse: Build, customize and deploy reliable AI agents (no-code friendly) that stick to the facts and automate everyday workflows.

---

## 🔍 Features

- 🤖 **AI-Powered Agents** — Automate bookings, reviews, customer support, coding tasks, finance, and more.  
- 📚 **Agent Library** — 100+ pre-built automation tasks and templates ready to use.  
- ⚡ **High Reliability** — Designed to minimize hallucinations and keep responses grounded.  
- 🧭 **No-code Friendly** — Simple UI for non-technical users; create agents without knowing n8n or automation internals.  
- 🕒 **24/7 Availability** — Agents run continuously to complete scheduled or on-demand tasks.  
- 🎨 **Modern UI/UX** — Clean, futuristic interface built for usability.

---

## 📸 Screenshots

**Dashboard**  
![Dashboard](./pic/WhatsApp%20Image%202025-09-07%20at%203.38.17%20PM.jpeg)

**AI Agents Library**  
![AI Agents](./pic/WhatsApp%20Image%202025-09-07%20at%203.38.31%20PM.jpeg)

**Agent Cards**  
![Agent Cards](./pic/WhatsApp%20Image%202025-09-07%20at%203.38.55%20PM.jpeg)

---

## 🛠️ Tech Stack

- **Frontend:** React.js + TailwindCSS  
- **Backend:** Python 
- **Automation / Orchestration:** n8n (workflows embedded via our `n8n-search-engine`)  
- **LLM / AI APIs:** Gemini / OpenAI / other LLM providers (via API keys) — we here used Gemini API key usage.  
- **Database:** MongoDB  

---

## 🧭 Why AgentVerse + n8n-search-engine?
We use our `n8n-search-engine` to index and surface pre-built workflows by description and intent — this makes it fast to discover, reuse, or wire-up automation templates inside AgentVerse. Link: https://github.com/AzamAliCodes/n8n-search-engine

---

## 🚦 Built for humans — Prompting & Safety

AgentVerse prioritizes reliability and clarity:

- **Prompt design:** Agents are shipped with carefully crafted prompts that instruct models to cite sources, refuse hallucinations, and answer concisely.  
- **Grounding layers:** Agents prefer structured data (APIs, DB results) and use retrieval/verification steps before responding.  
- **User-facing simplicity:** Non-technical users can build agents using guided forms — no knowledge of n8n or automation required.  
- **Fallbacks & audits:** Each agent logs decisions and can be audited or tuned if it produces unexpected output.

---




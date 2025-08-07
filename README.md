# 👁️ EyeOn AI – Agentic AI-Powered Smart Surveillance

**EyeOn AI** is an agentic, intelligent surveillance system that empowers users to define custom monitoring tasks via natural language. It uses large language models (LLMs), video vision-language models (VLMs), and a modular agent-based workflow to observe, reason, and alert based on visual input from CCTV cameras.

---

## 📌 Features

* 🧠 **Agentic Architecture** powered by LangGraph and LangChain
* 🎥 **Video Surveillance with VLMs** for high-level scene understanding
* 💬 **Chat Interface** to define and manage custom surveillance events
* ⚡ **Realtime Alerts** via phone, email, or push notifications
* 🧩 **Modular Agents**: `chatAgent`, `monitorAgent`, and `alertAgent`
* 🗃️ **Shared Memory State** updated across all agents
* 🚀 **FastAPI Backend** for orchestration, state updates, and frontend interaction
* 📱 **Flutter Frontend App** (coming soon)

---

## 🧠 System Architecture

* `chatAgent`: Interfaces with user, refines and registers surveillance tasks/events.
* `monitorAgent`: Periodically processes video input using a VLM or video-VLM, logs observations in shared state.
* `alertAgent`: Monitors the shared state and sends alerts when surveillance rules are matched.
* All agents operate independently but share a synchronized **memory state**.
* FastAPI acts as the external interface for API communication, authentication, and integration with the frontend app.

---

## 🧪 Tech Stack

| Component       | Tech                            |
| --------------- | ------------------------------- |
| Backend API     | FastAPI                         |
| Agent Framework | LangChain + LangGraph           |
| LLMs            | Open-source LLMs (e.g. Mixtral) |
| VLMs            | Video-LLaVA, Flamingo, etc.     |
| Database        | Firebase / Firestore            |
| Frontend        | Flutter                         |
| Deployment      | Docker, GPU-backed servers      |



5. **Connect to Cameras & Define Events**

Use the chat interface (or frontend when available) to register surveillance tasks.

---

## 📈 Roadmap

* [x] MVP Architecture Finalization
* [x] LangGraph-based Agent Workflows
* [ ] Full Integration of VLM for Video Processing
* [ ] State Persistence with Firestore
* [ ] Push & Voice Alert Integrations
* [ ] Flutter Frontend for Real-time Control
* [ ] Multi-user Support and Authentication
* [ ] Dockerized Deployment

---

## 🤖 Example Use Case

> "I'm not at home tonight. Alert me if anyone is near the main door."

**Workflow:**

* `chatAgent` registers a new event tied to the outdoor camera.
* `monitorAgent` watches and writes frame-based observations every 10 seconds.
* `alertAgent` detects suspicious activity and triggers a phone call.

---

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.

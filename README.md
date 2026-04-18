# RAG Conversational AI Agent with Lead Capture

## 🚀 Overview

This project is a production-ready conversational AI system built using Retrieval-Augmented Generation (RAG).

It intelligently:

* Understands user intent
* Answers queries strictly from context
* Captures leads for high-intent users

---

## 🧠 Key Features

### 1. Intent Classification

* Greeting → Natural response
* Query → Answer from retrieved context only
* High Intent → Trigger lead capture flow

### 2. RAG-based Response System

* Retrieves relevant context using embeddings
* Ensures responses are grounded (no hallucination)

### 3. Lead Capture System

* Collects user details (email, platform)
* Stores data for follow-up

---

## 🏗️ Architecture

User Input → Intent Detection →
→ (Query → RAG Retrieval → Response)
→ (High Intent → Lead Capture Flow)

---

## 🛠️ Tech Stack

* Python
* FastAPI (backend ready)
* NLP (intent classification)
* Embeddings
* FAISS-ready architecture

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
python main.py
```

---

## 💬 Example Interaction

User: "What's your pricing?"
→ Intent: QUERY
→ Response: Based on retrieved context

User: "I want to collaborate"
→ Intent: HIGH_INTENT
→ Lead capture initiated

---

## 📂 Project Structure

* `core/` → types and base logic
* `intent/` → intent detection
* `rag/` → retrieval system
* `memory/` → conversation memory
* `tools/` → lead capture
* `tests/` → unit tests

---

## 🎯 Why This Project Matters

This project simulates a real-world AI assistant used in:

* Sales automation
* Customer support bots
* Lead generation systems

It demonstrates practical ML system design, not just models.

---

## 👨‍💻 Author

Suryabhan Patel

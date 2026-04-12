# 🧠 Ollama Agent with SQLite Memory

## 📌 Overview

This project demonstrates a **simple Agentic AI system** built using:

* Local LLM via Ollama
* Persistent memory using SQLite
* Modular Python architecture

The agent maintains **conversation context across interactions**, making it stateful and closer to real-world AI agents.

---

## 🚀 Features

* ✅ Local LLM inference using Ollama (`gemma3:4b`)
* ✅ Persistent memory with SQLite
* ✅ Context-aware responses
* ✅ Clean modular design (LLM + Memory + Agent loop)
* ✅ Beginner-friendly implementation

---

## 🏗️ Project Structure

```
ollama_context_store/
│
├── main.py              # Agent loop (orchestrator)
├── ollama_client.py    # Handles LLM calls
├── memory_store.py     # Handles SQLite memory
├── agent_memory.db     # SQLite database (auto-created)
```

---

## ⚙️ Installation

### 1️⃣ Install Dependencies

```bash
pip install ollama
```

### 2️⃣ Start Ollama Server

```bash
ollama serve
```

### 3️⃣ Pull Model

```bash
ollama pull gemma3:4b
```

---

## ▶️ Run the Project

```bash
python main.py
```

---

## 🧠 How It Works

### 🔁 Agent Flow

1. User inputs a query
2. Past conversation is fetched from SQLite
3. Context + user input → sent to LLM
4. LLM generates response
5. Both user input & response are stored in DB

---

## 📂 File Breakdown

---

### 📄 `main.py` — Agent Controller

**Responsibility:**

* Controls the agent loop
* Connects memory + LLM
* Builds prompt with context

**Key Logic:**

```python
context = memory.get_recent()
```

Fetches previous conversation

```python
response = llm.call_ollama(prompt)
```

Calls LLM with context-aware prompt

```python
memory.store("User", user_input)
memory.store("Assistant", response)
```

Stores interaction

---

### 📄 `ollama_client.py` — LLM Interface

**Responsibility:**

* Handles communication with Ollama
* Abstracts LLM API calls

**Key Logic:**

```python
response = self.client.generate(
    model="gemma3:4b",
    prompt=prompt
)
```

👉 Acts as the **"Brain" of the agent**

---

### 📄 `memory_store.py` — Memory Layer

**Responsibility:**

* Stores conversation in SQLite
* Retrieves recent context
* Initializes database

**Database Schema:**

```
memory(
    id INTEGER,
    role TEXT,
    content TEXT,
    timestamp TEXT
)
```

**Key Methods:**

#### Store Memory

```python
memory.store(role, content)
```

#### Retrieve Context

```python
memory.get_recent(limit=5)
```

👉 Acts as the **"Memory" of the agent**

---

## 🧠 Key Learning Concepts

---

### 🔹 1. Agent Architecture

This project demonstrates a basic agent composed of:

| Component | Role               |
| --------- | ------------------ |
| LLM       | Reasoning (Ollama) |
| Memory    | Context (SQLite)   |
| Loop      | Control flow       |

---

### 🔹 2. Context Injection

Instead of stateless queries:

```python
prompt = f"...{context}..."
```

👉 The model becomes **stateful**

---

### 🔹 3. Separation of Concerns

* `ollama_client.py` → LLM logic
* `memory_store.py` → storage
* `main.py` → orchestration

👉 Clean, scalable design

---

### 🔹 4. Persistent Memory

Unlike chat APIs:

* Memory survives restarts
* Stored locally in SQLite

---

### 🔹 5. Agent Loop

```python
while True:
```

👉 Enables continuous interaction like real agents

---

## 🔥 Why This Is an Agent

This qualifies as an agent because:

* Maintains internal state (memory)
* Uses LLM for reasoning
* Operates in a loop
* Adapts responses based on past interactions

---

## 🚀 Future Improvements

* 🔹 Add tool usage (calculator, APIs)
* 🔹 Implement vector memory (RAG)
* 🔹 Add session-based memory
* 🔹 Multi-agent system (CrewAI)
* 🔹 Streaming responses

---

## 🧾 Interview Explanation

> "I built a modular agent system using Ollama for local inference and SQLite for persistent memory. The agent retrieves past context, injects it into prompts, and continuously updates its state through a loop."

---

## ⚠️ Troubleshooting

### Issue: ImportError (MemoryStore not found)

* Delete `__pycache__`
* Ensure file name is `memory_store.py`
* Restart environment

### Issue: Ollama not responding

* Run: `ollama serve`
* Check model: `ollama list`

---

## 📌 Conclusion

This project demonstrates how to build a **minimal yet powerful agentic system** from scratch without relying on heavy frameworks.

It is ideal for:

* Beginners learning Agentic AI
* Interview demonstrations
* Building foundation for advanced agents

---

## 👨‍💻 Author

Rahul Adagale
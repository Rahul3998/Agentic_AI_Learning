# 🤖 Multi-Agent System (Math + System Info)

This project is a simple **AI-powered multi-agent system** that routes user queries to the correct agent and returns a clear, human-friendly response.

It includes:

* 🧮 Math Agent (for calculations)
* 💻 System Agent (for system information)
* 🧠 LLM-based Router (decides which agent to use)
* ✨ Response Generator (explains results in simple English)

---

## 🚀 Features

* Intelligent query routing using prompt-based LLM
* Safe math execution (no `eval`)
* System information retrieval (CPU, RAM, Disk, OS, Network)
* Simple English explanations with reasoning
* Modular and extendable architecture

---

## 📁 Project Structure

```
Project_01_System_and_Calculator/
│── math_agent.py        # Handles math operations
│── system_agent.py      # Handles system info
│── main.py              # Entry point (multi-agent controller)
│── readme.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Rahul3998/Agentic_AI_Learning.git
cd Agentic_AI_Learning
```

### 2. Install dependencies

```bash
pip install psutil
```

> `math`, `platform`, and `socket` are built-in modules.

---

## ▶️ Usage

Run the main file:

```bash
python .\Project_01_System_and_Calculator\main.py
```

---

## 💡 Example Queries

### 🧮 Math

```
Solve 5*10
sqrt 25
sin 30
```

### 💻 System

```
What is my system config?
Check RAM
Show CPU usage
```

### 🌐 General

```
What is Python?
Explain AI
```

---

## 🔄 How It Works

1. **User Input**

   * User enters a query

2. **Router Prompt (LLM)**

   * Decides:

     * Math → `mul 5 10`
     * System → `ram`
     * Other → normal AI response

3. **Agent Execution**

   * MathAgent or SystemAgent processes the query

4. **Response Generator**

   * Converts raw output into simple English explanation

---

## 🧠 Agents Overview

### 🧮 Math Agent

Supports:

* add, sub, mul, div
* sqrt, pow
* log, log10
* sin, cos, tan
* factorial

---

### 💻 System Agent

Provides:

* OS details
* CPU usage
* RAM usage
* Disk usage
* Network info

---

## 🔐 Safety

* No use of `eval()` (prevents code injection)
* Controlled function mapping
* Input parsing with validation

---

## ⚡ Future Improvements

* 🔗 Integrate with Ollama / local LLM


* 🧠 Better NLP parsing (no strict format needed)
* 🌐 FastAPI / Web UI
* 📊 Pretty output (tables / dashboards)
* 🗂️ Logging and monitoring

---

## 🤝 Contributing

Feel free to fork this project and improve:

* Add new agents
* Improve routing logic
* Enhance UI/UX

---

## 📜 License

This project is open-source and free to use.

---

## 🙌 Author

Built as a simple **Agentic AI system** for learning and experimentation.

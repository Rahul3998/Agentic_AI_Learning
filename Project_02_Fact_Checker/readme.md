# 🧠 Fact Checker Agent (Ollama-based)

A simple **AI Fact Checker Agent** built using Python and a local LLM (via Ollama).
This project verifies the accuracy of statements and provides a concise verdict.

---

## 🚀 Features

* ✅ Uses a **local LLM (Ollama)** — no external API required
* ✅ Simple and lightweight **custom Agent architecture**
* ✅ Handles **streamed JSON responses** safely
* ✅ Clean and reusable code structure
* ✅ Easy to extend into a **multi-agent system**

---

## 🧪 Example

**Input:**

```
The Great Wall of China is visible from space with the naked eye.
```

**Output:**

```
❌ FALSE: The Great Wall is generally not visible to the naked eye from space.
```

---

## 🧩 How It Works

1. The **Agent** combines:

   * Instructions (prompt)
   * User input (statement)

2. Sends request to Ollama API

3. Parses **streamed JSON response**

4. Returns:

   * ✅ TRUE / ❌ FALSE
   * One-line explanation

---

## 🔧 Tech Stack

* Python
* Requests
* Python-dotenv
* Ollama (Local LLM)

---

## ⚠️ Notes

* Ensure Ollama is running before executing the script
* The model must be pulled beforehand
* Handles both **single JSON and streamed responses**

---

## 👨‍💻 Author

Rahul Adagale

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!

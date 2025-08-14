# Observable AI Agent with Langfuse and Agents (BeeAI)

This project demonstrates how to build **observable AI agents** using the **BeeAI framework**, **Langfuse for observability and tracing**, and **IBM Watsonx** as the LLM provider.  
The agent is equipped with Wikipedia, DuckDuckGo search, and weather tools, and supports interactive conversations from the terminal.

---

## 📖 Blog Reference
This implementation is explained in detail in my blog post:  
[**Building Observable AI Agents with Langfuse and BeeAI Framework**](https://medium.com/@SuryaDeepSingh/building-observable-ai-agents-with-langfuse-and-beeai-framework-33e2991b0bf9)

---

## 🚀 Features
- **Watsonx Integration** – Uses IBM Watsonx Granite model for LLM responses.
- **Observability with Langfuse** – Monitor performance, trace executions, and debug.
- **Interactive CLI Interface** – Console-based reader for real-time queries.
- **Multiple Tools**:
  - Wikipedia search
  - DuckDuckGo search
  - Weather information (OpenMeteo)

---

## 📂 Project Structure
```

.
├── beeio.py                  # Console I/O helper for interactive sessions
├── main.py                   # Main agent implementation
├── requirements.txt          # Project dependencies
├── .env                      # Environment variables
└── README.md                 # Documentation

````

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
````

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root with the following keys:

```env
LANGFUSE_PUBLIC_KEY=""
LANGFUSE_SECRET_KEY=""
LANGFUSE_HOST=""

WATSONX_API_KEY=""
WATSONX_PROJECT_ID=""
WATSONX_MODEL_ID="ibm/granite-3-3-8b-instruct"
WATSONX_URL=""
```

> 💡 Get Langfuse credentials from your Langfuse dashboard and Watsonx API keys from IBM Cloud.

---

## 📦 Requirements

**requirements.txt**

```
beeai-framework[all]
termcolor==3.1.0
langfuse==3.2.6
openinference-instrumentation-beeai==0.1.8
ibm-watsonx-ai>=1.0.0
ibm-cloud-sdk-core>=3.16.0
```

---

## ▶️ Running the Agent

Start the agent in interactive mode:

```bash
python main.py
```

You'll see:

```
Interactive session has started. To escape, input 'q' and submit.
🛠️ System: Agent initialized with Wikipedia, DuckDuckGo, and Weather tools.
🔁 Now you can ask your own questions.
```

Example queries:

```
#Latest news about artificial intelligence in 2025
#What is the current weather in Chandigarh?
```

To exit, type:

```
q
```

---

## 📊 Observability & Tracing with Langfuse

* Every agent execution is traced with **Langfuse**.
* You can view step-by-step reasoning, tool usage, and performance metrics.
* More on setting up Langfuse: [Langfuse Self-Hosting Guide](https://langfuse.com/self-hosting/docker-compose)

---

## 🛠 Tech Stack

* **[BeeAI Framework](https://pypi.org/project/beeai-framework/)**
* **[Langfuse](https://langfuse.com/)**
* **[IBM Watsonx](https://www.ibm.com/watsonx)**
* **Python 3.10+**

---

## 📄 License

MIT License

---

## ✍️ Author

**Surya Deep Singh**
[Medium](https://medium.com/@SuryaDeepSingh)

```



# Week 2 — Memory-Enabled GenAI App

**Skills covered:** Claude API · Function Calling · Short & Long-Term Memory Systems

---

## What this project does

A terminal chatbot that:
- **Remembers you** across sessions (long-term memory → `memory.json`)
- **Tracks the conversation** within a session (short-term memory → messages list)
- **Calls real tools** when needed (date/time, calculator, weather, unit converter)
- **Tracks token usage** so you understand API costs

---

## Project structure

```
week2_memory_app/
├── chatbot.py        ← main app — the agentic loop
├── tools.py          ← tool definitions + implementations
├── memory.py         ← ShortTermMemory + LongTermMemory classes
├── requirements.txt  ← dependencies
├── .env.example      ← copy this to .env and add your key
├── .gitignore        ← protects your .env from being committed
└── README.md         ← you are here
```

---

## Setup (5 minutes)

**1. Clone / download the project**
```bash
cd week2_memory_app
```

**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your API key**
```bash
cp .env.example .env
# Open .env and replace "your_api_key_here" with your real key
# Get it from: https://console.anthropic.com/
```

**5. Run the chatbot**
```bash
python chatbot.py
```

---

## Try these prompts to test all features

| What to type | What it tests |
|---|---|
| `My name is Vidhya` | long-term memory save |
| `What's my name?` | long-term memory recall |
| `What time is it?` | function calling (get_datetime) |
| `What's 15% of 847?` | function calling (calculator) |
| `Weather in Mumbai` | function calling (get_weather) |
| `Convert 100 km to miles` | function calling (convert_units) |
| `memory` | show all saved facts |
| `clear` | reset conversation |
| `quit` | exit |

---

## Key concepts learned

### 1. Function Calling
The model reads tool descriptions and decides when to call them.
You never hardcode "if user asks about weather → call weather API."
The model figures that out from the tool description.

### 2. Short-Term Memory
The full conversation history (`messages` list) is passed on every API call.
The model has no built-in memory — WE provide context.

### 3. Long-Term Memory
Important facts saved to `memory.json` and injected into the system prompt.
This is why the bot remembers your name even after restarting.

### 4. The Agentic Loop
```
User message
    ↓
Call Claude API (with tools + history)
    ↓
Claude returns tool_use? ──YES──→ Run tool → Send result back → repeat
    ↓ NO
Final text reply
```

### 5. Token Management
Every response shows token counts and estimated cost.
In production: cache responses, trim history, use cheaper models for simple tasks.

---

## How to extend this project

- Add a **web search tool** (use `requests` + DuckDuckGo or SerpAPI)
- Add a **note-taking tool** (save/retrieve notes from a file)
- Replace `memory.json` with **SQLite** for structured storage
- Add a **Streamlit** frontend (Week 3 prep)
- Switch between **Claude and OpenAI** models with a flag

---

## Submission checklist

- [ ] App runs without errors
- [ ] Chatbot remembers name/info after restart
- [ ] At least 3 tools work (datetime, calculator, one more)
- [ ] Code is commented and readable
- [ ] `.env` is in `.gitignore` (API key not exposed)
- [ ] Project pushed to GitHub

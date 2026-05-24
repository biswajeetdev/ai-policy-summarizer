# AI Policy Summarizer

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?style=flat&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white)

Turn dense policy PDFs into structured plain-language summaries in seconds.

Built with **Groq** (free LLM API) + **Streamlit**. No OpenAI key required.

## What it does

- **Summarize** — extracts key points, required actions, affected roles, deadlines, and defines jargon
- **Compare** — side-by-side diff of two or more policy documents, highlighting conflicts and differences
- **Download** — export any summary as Markdown

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # add your Groq key
streamlit run app.py
```

Get a free Groq API key (no credit card) at [console.groq.com/keys](https://console.groq.com/keys).

## Tech stack

| Layer | Choice | Why |
|---|---|---|
| LLM | Groq / Llama 3.3 70B | Free tier, 14,400 req/day, fast inference |
| UI | Streamlit | Rapid prototyping, PDF upload built-in |
| PDF parsing | pypdf | Pure Python, no system deps |
| Alt provider | OpenAI (optional) | Switchable via sidebar dropdown |

## Use cases

- HR teams reviewing updated employment policies
- Legal and compliance teams comparing contract versions
- Students and researchers digesting academic regulations
- Ops teams translating vendor SLAs into action items

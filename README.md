# AI Policy Summarizer

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?style=flat&logoColor=white)
![LLM](https://img.shields.io/badge/LLM-llama--3.3--70b-blueviolet?style=flat)

Turn dense policy PDFs into structured plain-language summaries in seconds.

Built with **Groq** (free LLM API) + **Streamlit**. No OpenAI key required.

## What it does

- **Summarize mode** — extracts key points, required actions, affected roles, deadlines, and a jargon glossary
- **Compare mode** — diffs two policy documents side by side, highlights what changed and which is more restrictive
- **Download** — export any result as a Markdown file

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # add your Groq key
streamlit run app.py
```

Get a free Groq API key (no credit card) at [console.groq.com/keys](https://console.groq.com/keys).

## Tech stack

| Layer | Technology |
|-------|-----------|
| UI | Streamlit |
| LLM | Groq — `llama-3.3-70b-versatile` (free tier) |
| PDF parsing | pypdf |
| Alt provider | OpenAI-compatible (swap key + model) |

## Use cases

- HR teams reviewing benefits policy changes
- Legal reviewing contract terms
- Students parsing dense academic regulations
- Anyone who needs to understand a document fast

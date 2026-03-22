# 🤖 GenAI Metadata Manager

> Auto-generate business-friendly database documentation using
> Claude (Anthropic) and Gemini (Google) — the AI-powered solution
> to the #1 most-hated data engineering task.

## 🎯 Problem Solved
Data engineers spend hours writing column descriptions nobody reads.
This tool introspects your database schema and generates rich,
business-friendly documentation in seconds using GenAI.

## ✨ Features
- Connects to any SQL database (SQLite, PostgreSQL, MySQL)
- Introspects schema: columns, types, PKs, FKs, sample data
- Generates docs with Claude Sonnet or Gemini Flash
- Human-in-the-loop: review, edit, and approve before saving
- Exports to Markdown and JSON
- Ships with a realistic healthcare RCM demo database

## 🏗️ Architecture
```
DB Schema Introspection (SQLAlchemy)
        ↓
Rich Context Builder (column types, nullability, sample rows)
        ↓
AI Prompt Engineering (Claude or Gemini)
        ↓
Structured JSON Response (table desc, column defs, glossary)
        ↓
Human Review & Approval (Streamlit UI)
        ↓
Metadata Store (JSON → exportable to Unity Catalog / OpenMetadata)
```

## 🚀 Quick Start
```bash
git clone https://github.com/yourusername/genai-metadata-manager
cd genai-metadata-manager
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
streamlit run app.py
```

## 🔑 API Keys Required
- **Anthropic API key**: console.anthropic.com (free tier available)
- **Google API key**: aistudio.google.com (free tier: 15 RPM)

## 🛠️ Tech Stack
Python · Streamlit · SQLAlchemy · Anthropic SDK · Google Generative AI

## 📄 License
MIT
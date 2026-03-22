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
```mermaid
flowchart LR
    subgraph DB["🗄️ Data Source"]
        A1[SQLite / PostgreSQL\nMySQL / Any SQL DB]
    end

    subgraph INSPECT["🔍 Schema Introspection"]
        B1[SQLAlchemy Inspector]
        B2[Context Builder\ncolumns · types · samples]
        B1 --> B2
    end

    subgraph AI["🤖 AI Generation"]
        C1[Prompt Engineering]
        C2[Claude Sonnet\nAnthropic]
        C3[Gemini Flash\nGoogle]
        C1 --> C2
        C1 --> C3
    end

    subgraph UI["🎯 Streamlit App"]
        D1[Table Browser]
        D2[Human Review & Edit]
        D3[Approve & Save]
        D1 --> D2 --> D3
    end

    subgraph OUT["📤 Output"]
        E1[JSON Metadata Store]
        E2[Markdown Export]
        E3[JSON Export]
    end

    DB --> INSPECT --> AI --> UI --> OUT
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
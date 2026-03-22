import os, json
import anthropic
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def _build_prompt(ctx: dict) -> str:
    cols = "\n".join([
        f"  - {c['name']} ({c['type']})"
        f"{'  [PK]' if c['is_pk'] else ''}"
        f"{'  [NOT NULL]' if not c['nullable'] else ''}"
        for c in ctx["columns"]
    ])
    sample = json.dumps(ctx["sample_rows"], indent=2, default=str)
    fks = "\n".join(ctx["foreign_keys"]) or "None"

    return f"""You are a senior data engineer documenting a database schema.
Analyze the table below and generate clear, business-friendly documentation.

TABLE: {ctx['table']}
ROW COUNT: {ctx['row_count']:,}
PRIMARY KEY: {ctx['primary_key']}

COLUMNS:
{cols}

FOREIGN KEYS:
{fks}

SAMPLE DATA (first 3 rows):
{sample}

Generate documentation in this EXACT JSON format (no markdown, no preamble):
{{
  "table_description": "2-3 sentence plain-English description of what this table stores and its business purpose",
  "columns": [
    {{
      "name": "column_name",
      "description": "clear business-friendly description",
      "example_value": "realistic example value"
    }}
  ],
  "business_glossary": [
    {{
      "term": "key business term from this table",
      "definition": "plain English definition for non-technical stakeholders"
    }}
  ],
  "data_quality_notes": "brief notes on nullability, data patterns, or quality observations",
  "suggested_tags": ["tag1", "tag2", "tag3"]
}}"""

def generate_with_claude(ctx: dict) -> dict:
    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"))
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        messages=[{"role":"user","content":_build_prompt(ctx)}]
    )
    raw = msg.content[0].text.strip()
    return json.loads(raw)

def generate_with_gemini(ctx: dict) -> dict:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    resp = model.generate_content(_build_prompt(ctx))
    raw = resp.text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())
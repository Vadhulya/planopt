import json
from typing import List
import google.generativeai as genai
import config
from rag_pipeline import retrieve_docs


MODEL_NAME = "models/gemini-2.5-flash"
  


def build_prompt(user_plan: str, retrieved_docs: List[str]) -> str:
    """
    retrieved_docs is a FLAT LIST now.
    Example: ["doc1...", "doc2...", "doc3..."]
    """

    knowledge_context = "\n".join(retrieved_docs)

    prompt = f"""
You are an AI Plan Optimiser.

USER PLAN:
{user_plan}

KNOWLEDGE CONTEXT:
{knowledge_context}

TASK:
1. Identify all influencing factors.
2. Create timeline, checklist, risks.
3. Return ONLY JSON in the following exact structure:

{{
  "summary": "...",
  "factors": [
    {{
      "category": "...",
      "description": "...",
      "importance": "...",
      "recommendation": "..."
    }}
  ],
  "timeline": {{
    "before": ["..."],
    "during": ["..."],
    "after": ["..."]
  }},
  "checklist": ["..."],
  "risks": [
    {{
      "risk": "...",
      "probability": "...",
      "impact": "...",
      "mitigation": "..."
    }}
  ]
}}
"""
    return prompt


def optimise_plan(user_plan: str):

    # retrieved_docs is already a flat list
    retrieved_docs = retrieve_docs(user_plan, k=3)

    prompt = build_prompt(user_plan, retrieved_docs)

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)

    raw_text = response.text

    # Try to parse strict JSON
    try:
        return json.loads(raw_text)

    except Exception:
        # Fallback: attempt to extract JSON block
        start = raw_text.find("{")
        end = raw_text.rfind("}")

        if start != -1 and end != -1 and start < end:
            try:
                return json.loads(raw_text[start:end + 1])
            except Exception:
                pass

        return {"raw_response": raw_text}
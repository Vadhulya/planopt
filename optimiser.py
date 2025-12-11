import json
from typing import List
import google.generativeai as genai
from rag_pipeline import retrieve_docs
from config import API_KEY  # ensures config runs

MODEL_NAME = "models/gemini-2.5-pro"
  # or gemini-1.0-pro


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

    # FIX: retrieved_docs is a flat list, not nested
    retrieved_docs = retrieve_docs(user_plan, k=3)

    prompt = build_prompt(user_plan, retrieved_docs)

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)

    raw_text = response.text

    # Try parse JSON
    try:
        return json.loads(raw_text)
    except:
        s = raw_text.find("{")
        e = raw_text.rfind("}")
        if s != -1 and e != -1:
            try:
                return json.loads(raw_text[s:e+1])
            except:
                return {"raw_response": raw_text}

    return {"raw_response": raw_text}

import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def generate_teardown(app_name, research_text):

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
You are a senior product analyst with 15 years of experience doing product teardowns for top-tier VC firms and consulting firms. You are rigorous, evidence-driven, and direct. You do not use filler language or vague generalities.

You have been given live research about a digital product called {app_name}. Your job is to produce a sharp, specific product teardown using only what the research supports.

RESEARCH:
{research_text}

RULES:
1. Every claim must be grounded in the research above. Do not invent facts.
2. Be specific — name actual features, actual failure modes, actual user behaviors.
3. Description - One crisp paragraph. What the product is, who it serves, and what problem it was built to solve. No fluff.
4. Root cause must be structural or strategic, not surface-level. "Poor execution" is not a root cause. "Misaligned incentive structure between delivery partners and platform" is.
5. Business cost must name a specific business metric at risk — retention rate, CAC, LTV, NPS, market share.
6. Recommendation must be a concrete product or strategy change — name the mechanism, not just the direction.
7. If research is thin on a specific field, say so honestly in confidence_note instead of padding with generic statements.
7. Write like you are presenting to a board. No fluff. No hedging. No marketing language.

Return a JSON object with exactly these fields:
- app_name
- description
- problem
- root_cause  
- user_impact
- business_cost
- recommendation
- confidence_note

Each field: 2-4 sharp sentences maximum.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1200,
        response_format={"type": "json_object"}
    )

    raw = response.choices[0].message.content.strip()
    teardown = json.loads(raw)
    return teardown
 # AI Product Teardown Generator

Type any digital product. Get a structured teardown backed by live research —
not guesswork.

Built for product analysts and APMs who want to understand why a product is 
winning or failing, fast.

**Live demo:** [your-streamlit-url-here]

---

## How it works

1. Verifies the product exists before generating anything
2. Runs 4 targeted searches via Tavily — complaints, business model, competitors, news
3. Feeds research into LLaMA 3.3 70B via Groq
4. Returns: Overview → Problem → Root Cause → User Impact → Business Cost → Recommendation

Every output is grounded in sources you can verify. No hallucinated confidence.

---

## Stack

Python · Streamlit · Groq API (LLaMA 3.3 70B) · Tavily API · python-dotenv

---

## Run locally

```bash
git clone https://github.com/Deepak-Sekar-01/ai-teardown-generator
cd ai-teardown-generator
pip install -r requirements.txt
```

Add a `.env` file:
```
GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

```bash
streamlit run app.py
```

---

## Built by

**Deepak Sekar** — AI Product Analyst, Bangalore

[LinkedIn](https://linkedin.com/in/deepaksekar-) · [Portfolio](https://deepaksekar.netlify.app) · [Project 1 — Swiggy AI Support Agent](https://github.com/Deepak-Sekar-01/Swiggy-Support-Agent)

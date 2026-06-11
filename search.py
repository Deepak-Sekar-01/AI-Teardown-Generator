import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

def verify_entity(app_name, client):
    try:
        response = client.search(
            f"{app_name} company product official",
            max_results=5
        )
        results = response.get("results", [])
        high_confidence = [
            r for r in results
            if r.get("score", 0) >= 0.25
        ]
        return len(high_confidence) >= 2

    except Exception as e:
        print(f"verify_entity error: {e}")
        return False


def get_research(app_name):
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    if not verify_entity(app_name, client):
        return None, []

    queries = [
        f"{app_name} user complaints problems issues",
        f"{app_name} business model revenue strategy",
        f"{app_name} product features competitors alternatives",
        f"{app_name} news updates 2024 2025"
    ]

    all_results = []

    for query in queries:
        try:
            response = client.search(query, max_results=3)
            for result in response["results"]:
                all_results.append({
                    "title":   result["title"],
                    "url":     result["url"],
                    "content": result["content"],
                    "score":   result.get("score", 0)
                })
        except Exception as e:
            print(f"Search failed for query '{query}': {e}")
            continue

    research_text = ""
    sources = []

    for i, result in enumerate(all_results):
        research_text += f"\n\nSOURCE {i+1}: {result['title']}\n"
        research_text += result["content"]
        sources.append({
            "title": result["title"],
            "url":   result["url"]
        })

    return research_text, sources
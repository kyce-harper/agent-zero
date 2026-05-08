import time

SCHEMA = {
    "name": "search_web",
    "description": (
        "Search the web using DuckDuckGo. "
        "Returns the top 3 results with title, URL, and a short snippet. "
        "Use this for current events, facts, or anything that requires up-to-date information."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query string.",
            },
        },
        "required": ["query"],
    },
}


def run(input: dict) -> str:
    from ddgs import DDGS

    query: str = input["query"]
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=3):
                results.append(
                    f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}"
                )
        if not results:
            return "No results found."
        return "\n---\n".join(results)
    except Exception as e:
        return f"Search failed: {e}"

import os
import json
import re

from dotenv import load_dotenv
from tavily import TavilyClient


load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

client = TavilyClient(api_key=api_key)


# Domains that are clearly not useful for our investigation
BLOCKED_DOMAINS = {
    "spotify.com",
    "imdb.com",
    "rottentomatoes.com",
    "youtube.com",
    "facebook.com",
    "instagram.com",
    "x.com",
    "twitter.com"
}


def normalize(text):
    """Convert text into simple lowercase words."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return set(text.split())


def is_relevant_result(result, app_name, query):
    """
    Decide whether a Tavily result is actually relevant
    to the loan app being investigated.
    """

    title = result.get("title", "") or ""
    content = result.get("content", "") or ""
    url = result.get("url", "") or ""

    combined_text = f"{title} {content} {url}".lower()

    app_name_lower = app_name.lower()

    # --------------------------------------------------
    # 1. Reject obviously unrelated domains
    # --------------------------------------------------

    for domain in BLOCKED_DOMAINS:
        if domain in url.lower():
            return False


    # --------------------------------------------------
    # 2. Check whether the app name appears
    # --------------------------------------------------

    exact_app_match = app_name_lower in combined_text

    # Also use meaningful words from the app name
    app_words = normalize(app_name)

    # Ignore very common words
    ignored_words = {
        "loan",
        "app",
        "personal",
        "instant",
        "online",
        "and",
        "the",
        "for",
        "upi"
    }

    important_words = {
        word
        for word in app_words
        if len(word) >= 4 and word not in ignored_words
    }

    matched_words = sum(
        1
        for word in important_words
        if word in combined_text
    )


    # --------------------------------------------------
    # 3. Query-specific relevance
    # --------------------------------------------------

    query_lower = query.lower()

    query_keywords = []

    if "rbi" in query_lower:
        query_keywords = [
            "rbi",
            "reserve bank",
            "nbfc",
            "regulated",
            "digital lending",
            "lending"
        ]

    elif "complaint" in query_lower:
        query_keywords = [
            "complaint",
            "complaints",
            "consumer",
            "customer",
            "issue",
            "problem",
            "harassment",
            "repayment"
        ]

    elif "scam" in query_lower:
        query_keywords = [
            "scam",
            "fraud",
            "complaint",
            "harassment",
            "fake",
            "debt",
            "recovery"
        ]


    keyword_matches = sum(
        1
        for keyword in query_keywords
        if keyword in combined_text
    )


    # --------------------------------------------------
    # 4. Tavily relevance score
    # --------------------------------------------------

    tavily_score = result.get("score", 0) or 0


    # --------------------------------------------------
    # 5. Calculate our relevance score
    # --------------------------------------------------

    relevance_score = 0


    # Exact app name is a strong signal
    if exact_app_match:
        relevance_score += 5

    # Meaningful app-name words
    relevance_score += min(
        matched_words,
        3
    )

    # Query-specific evidence
    relevance_score += min(
        keyword_matches,
        2
    )

    # Tavily's own ranking
    if tavily_score >= 0.5:
        relevance_score += 2

    elif tavily_score >= 0.35:
        relevance_score += 1


    # --------------------------------------------------
    # 6. Final decision
    # --------------------------------------------------

    return relevance_score >= 4


def search_web(query, max_results=5):

    response = client.search(
        query=query,
        search_depth="basic",
        max_results=max_results
    )

    return response["results"]


if __name__ == "__main__":

    with open(
        "data/raw/playstore_apps.json",
        "r",
        encoding="utf-8"
    ) as f:

        apps = json.load(f)


    all_evidence = []


    for i, app in enumerate(apps, start=1):

        app_name = app["title"]
        developer = app["developer"]

        print(
            f"\n[{i}/{len(apps)}] Searching: {app_name}"
        )


        queries = [
            f'"{app_name}" RBI',
            f'"{app_name}" complaint',
            f'"{app_name}" scam'
        ]


        app_evidence = []


        for query in queries:

            try:

                results = search_web(
                    query,
                    max_results=5
                )


                accepted = 0


                for result in results:

                    if is_relevant_result(
                        result,
                        app_name,
                        query
                    ):

                        app_evidence.append({
                            "query": query,
                            "title": result.get(
                                "title",
                                ""
                            ),
                            "url": result.get(
                                "url",
                                ""
                            ),
                            "content": result.get(
                                "content",
                                ""
                            ),
                            "tavily_score": result.get(
                                "score",
                                0
                            )
                        })

                        accepted += 1


                print(
                    f"  {query} → "
                    f"{accepted} relevant results"
                )


            except Exception as e:

                print(
                    f"  Error searching "
                    f"'{query}': {e}"
                )


        # Remove duplicate URLs
        unique_evidence = {}

        for item in app_evidence:

            url = item["url"]

            if url and url not in unique_evidence:
                unique_evidence[url] = item


        app_evidence = list(
            unique_evidence.values()
        )


        # Keep maximum 6 strongest results per app
        app_evidence.sort(
            key=lambda x: x.get(
                "tavily_score",
                0
            ),
            reverse=True
        )

        app_evidence = app_evidence[:6]


        all_evidence.append({

            "app_id": app["app_id"],

            "app_name": app_name,

            "developer": developer,

            "evidence": app_evidence

        })


    os.makedirs(
        "data/raw",
        exist_ok=True
    )


    with open(
        "data/raw/web_evidence.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            all_evidence,
            f,
            indent=4,
            ensure_ascii=False
        )


    print(
        f"\nWeb research completed for "
        f"{len(all_evidence)} apps."
    )
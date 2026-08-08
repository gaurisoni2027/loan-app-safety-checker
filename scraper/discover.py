from google_play_scraper import search
import json


def discover_loan_apps(query="loan app", limit=20):
    results = search(
        query,
        lang="en",
        country="in",
        n_hits=limit
    )

    apps = []

    for app in results:
        apps.append({
            "app_id": app.get("appId"),
            "title": app.get("title"),
            "developer": app.get("developer"),
            "score": app.get("score"),
            "ratings": app.get("ratings"),
            "icon": app.get("icon")
        })

    return apps


if __name__ == "__main__":
    apps = discover_loan_apps(limit=20)

    print(f"\nFound {len(apps)} apps:\n")

    for app in apps:
        print(
            f"{app['title']} | "
            f"{app['developer']} | "
            f"{app['app_id']}"
        )

    with open("data_discovered.json", "w", encoding="utf-8") as f:
        json.dump(apps, f, indent=4, ensure_ascii=False)
from google_play_scraper import app
import json
import os


def get_app_details(app_id):
    details = app(
        app_id,
        lang="en",
        country="in"
    )

    return {
        "app_id": details.get("appId"),
        "title": details.get("title"),
        "developer": details.get("developer"),
        "description": details.get("description"),
        "score": details.get("score"),
        "ratings": details.get("ratings"),
        "reviews": details.get("reviews"),
        "installs": details.get("installs"),
        "genre": details.get("genre"),
        "updated": details.get("updated"),
        "privacy_policy": details.get("privacyPolicy")
    }


if __name__ == "__main__":

    with open("data_discovered.json", "r", encoding="utf-8") as f:
        apps = json.load(f)

    all_details = []

    for i, app_data in enumerate(apps, start=1):

        print(f"[{i}/{len(apps)}] Fetching: {app_data['title']}")

        try:
            details = get_app_details(app_data["app_id"])
            all_details.append(details)

        except Exception as e:
            print(f"Error fetching {app_data['title']}: {e}")

    os.makedirs("data/raw", exist_ok=True)

    with open("data/raw/playstore_apps.json", "w", encoding="utf-8") as f:
        json.dump(
            all_details,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nSuccessfully collected details for {len(all_details)} apps.")
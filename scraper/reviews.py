from google_play_scraper import reviews, Sort
import json
import os


def get_reviews(app_id, count=30):
    result, _ = reviews(
        app_id,
        lang="en",
        country="in",
        sort=Sort.NEWEST,
        count=count
    )

    return result


if __name__ == "__main__":

    with open("data_discovered.json", "r", encoding="utf-8") as f:
        apps = json.load(f)

    all_reviews = []

    for i, app_data in enumerate(apps, start=1):

        print(f"[{i}/{len(apps)}] Fetching reviews: {app_data['title']}")

        try:
            app_reviews = get_reviews(
                app_data["app_id"],
                count=30
            )

            for review in app_reviews:
                all_reviews.append({
                    "app_id": app_data["app_id"],
                    "app_name": app_data["title"],
                    "developer": app_data["developer"],
                    "rating": review.get("score"),
                    "review": review.get("content"),
                    "date": review.get("at")
                })

        except Exception as e:
            print(f"Error fetching {app_data['title']}: {e}")

    os.makedirs("data/raw", exist_ok=True)

    with open("data/raw/reviews.json", "w", encoding="utf-8") as f:
        json.dump(
            all_reviews,
            f,
            indent=4,
            ensure_ascii=False,
            default=str
        )

    print(f"\nSuccessfully collected {len(all_reviews)} reviews.")
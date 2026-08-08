import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


COMPLAINT_KEYWORDS = {
    "privacy": [
        "privacy", "data", "contacts", "permission",
        "photos", "personal information"
    ],
    "harassment": [
        "harass", "harassment", "threat", "threaten",
        "abuse", "calling", "call my contacts"
    ],
    "hidden_fees": [
        "hidden fee", "extra charge", "extra fee",
        "hidden charge", "high interest", "interest"
    ],
    "repayment": [
        "repayment", "repay", "payment", "recovery",
        "collection", "due date"
    ],
    "fraud": [
        "scam", "fraud", "fake", "cheating"
    ]
}


def load_reviews(path="data/raw/reviews.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def analyze_reviews(reviews_data):

    df = pd.DataFrame(reviews_data)

    df = df.dropna(subset=["review"])
    df["review"] = df["review"].astype(str)

    # TF-IDF
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=100
    )

    tfidf_matrix = vectorizer.fit_transform(df["review"])
    words = vectorizer.get_feature_names_out()

    # Sentiment
    analyzer = SentimentIntensityAnalyzer()

    def get_sentiment(text):

        score = analyzer.polarity_scores(text)["compound"]

        if score >= 0.05:
            return "positive"
        elif score <= -0.05:
            return "negative"
        else:
            return "neutral"

    df["sentiment"] = df["review"].apply(get_sentiment)

    # Complaint detection
    def detect_complaints(text):

        text = text.lower()
        categories = []

        for category, keywords in COMPLAINT_KEYWORDS.items():

            for keyword in keywords:

                if keyword in text:
                    categories.append(category)
                    break

        return categories

    df["complaints"] = df["review"].apply(detect_complaints)

    return df, tfidf_matrix, words


def create_app_analysis(df):

    app_results = []

    for app_id, group in df.groupby("app_id"):

        total_reviews = len(group)

        sentiment_counts = group["sentiment"].value_counts()

        positive = sentiment_counts.get("positive", 0)
        neutral = sentiment_counts.get("neutral", 0)
        negative = sentiment_counts.get("negative", 0)

        complaint_counts = {}

        for complaints in group["complaints"]:

            for complaint in complaints:

                complaint_counts[complaint] = (
                    complaint_counts.get(complaint, 0) + 1
                )

        app_results.append({
            "app_id": app_id,
            "app_name": group["app_name"].iloc[0],
            "developer": group["developer"].iloc[0],

            "total_reviews": total_reviews,

            "sentiment": {
                "positive": positive,
                "neutral": neutral,
                "negative": negative
            },

            "complaints": complaint_counts
        })

    return app_results


if __name__ == "__main__":

    reviews_data = load_reviews()

    df, tfidf_matrix, words = analyze_reviews(reviews_data)

    app_results = create_app_analysis(df)

    with open("data/analysis.json", "w", encoding="utf-8") as f:
        json.dump(
            app_results,
            f,
            indent=4,
            ensure_ascii=False,
            default=int
        )

    print(f"Total reviews analyzed: {len(df)}")
    print(f"Apps analyzed: {len(app_results)}")

    print("\nAPP ANALYSIS:\n")

    for app in app_results:

        print("-" * 60)

        print("App:", app["app_name"])
        print("Reviews:", app["total_reviews"])

        print("Sentiment:")
        print("  Positive:", app["sentiment"]["positive"])
        print("  Neutral:", app["sentiment"]["neutral"])
        print("  Negative:", app["sentiment"]["negative"])

        print("Complaints:")
        print(" ", app["complaints"])
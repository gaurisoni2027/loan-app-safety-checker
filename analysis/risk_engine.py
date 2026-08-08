import json


def calculate_risk(app, playstore_data):

    score = 0
    risk_factors = []
    positive_signals = []

    # =========================
    # REVIEW SIGNALS
    # =========================

    total_reviews = app["total_reviews"]
    negative = app["sentiment"]["negative"]
    complaints = app["complaints"]

    if total_reviews > 0:

        negative_percentage = (
            negative / total_reviews
        ) * 100

        if negative_percentage >= 40:
            score += 30
            risk_factors.append(
                "High negative review sentiment"
            )

        elif negative_percentage >= 25:
            score += 20
            risk_factors.append(
                "Moderately high negative review sentiment"
            )

        elif negative_percentage >= 15:
            score += 10
            risk_factors.append(
                "Some negative review sentiment"
            )

    # Fraud
    fraud = complaints.get("fraud", 0)

    if fraud >= 5:
        score += 20
        risk_factors.append(
            f"{fraud} reviews mention fraud or scam"
        )

    elif fraud >= 2:
        score += 10
        risk_factors.append(
            f"{fraud} reviews mention fraud or scam"
        )

    # Privacy
    privacy = complaints.get("privacy", 0)

    if privacy >= 5:
        score += 15
        risk_factors.append(
            f"{privacy} privacy-related complaints"
        )

    elif privacy >= 2:
        score += 8
        risk_factors.append(
            f"{privacy} privacy-related complaints"
        )

    # Harassment
    harassment = complaints.get("harassment", 0)

    if harassment >= 5:
        score += 15
        risk_factors.append(
            f"{harassment} harassment-related complaints"
        )

    elif harassment >= 2:
        score += 8
        risk_factors.append(
            f"{harassment} harassment-related complaints"
        )

    # Hidden fees
    hidden_fees = complaints.get("hidden_fees", 0)

    if hidden_fees >= 5:
        score += 10
        risk_factors.append(
            f"{hidden_fees} hidden-fee complaints"
        )

    elif hidden_fees >= 2:
        score += 5
        risk_factors.append(
            f"{hidden_fees} hidden-fee complaints"
        )

    # =========================
    # PLAY STORE SIGNALS
    # =========================

    rating = playstore_data.get("score")
    ratings_count = playstore_data.get("ratings", 0)
    privacy_policy = playstore_data.get("privacy_policy")

    # Rating
    if rating is not None:

        if rating < 2.5:
            score += 15
            risk_factors.append(
                f"Very low Play Store rating ({rating:.1f})"
            )

        elif rating < 3.2:
            score += 8
            risk_factors.append(
                f"Low Play Store rating ({rating:.1f})"
            )

        elif rating >= 4.0:
            positive_signals.append(
                f"Strong Play Store rating ({rating:.1f})"
            )

    # Number of ratings
    if ratings_count is not None:

        if ratings_count < 100:
            score += 5
            risk_factors.append(
                "Limited number of Play Store ratings"
            )

        elif ratings_count >= 10000:
            positive_signals.append(
                "Large number of Play Store ratings"
            )

    # Privacy policy
    if not privacy_policy:

        score += 10
        risk_factors.append(
            "No privacy policy listed on Play Store"
        )

    else:

        positive_signals.append(
            "Privacy policy is listed"
        )

    # =========================
    # FINAL SCORE
    # =========================

    score = min(score, 100)

    if score >= 60:
        risk_level = "HIGH RISK"

    elif score >= 30:
        risk_level = "CAUTION"

    else:
        risk_level = "LOW RISK"

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
        "positive_signals": positive_signals
    }


if __name__ == "__main__":

    # Review analysis
    with open(
        "data/analysis.json",
        "r",
        encoding="utf-8"
    ) as f:
        review_analysis = json.load(f)

    # Play Store data
    with open(
        "data/raw/playstore_apps.json",
        "r",
        encoding="utf-8"
    ) as f:
        playstore_apps = json.load(f)

    # Create lookup by app ID
    playstore_lookup = {
        app["app_id"]: app
        for app in playstore_apps
    }

    results = []

    for app in review_analysis:

        playstore_data = playstore_lookup.get(
            app["app_id"],
            {}
        )

        risk = calculate_risk(
            app,
            playstore_data
        )

        result = {
            **app,
            **playstore_data,
            **risk
        }

        results.append(result)

    with open(
        "data/risk_results.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            indent=4,
            ensure_ascii=False,
            default=int
        )

    print(f"Analyzed {len(results)} apps\n")

    for result in results:

        print("-" * 60)

        print("App:", result["app_name"])
        print("Rating:", result.get("score"))
        print("Risk Score:", result["risk_score"])
        print("Risk Level:", result["risk_level"])

        print("\nRisk Factors:")

        for factor in result["risk_factors"]:
            print(" -", factor)

        print("\nPositive Signals:")

        for signal in result["positive_signals"]:
            print(" +", signal)
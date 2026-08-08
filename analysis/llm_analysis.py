import os
import json
from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def analyze_app(app_data, web_data):

    evidence = {
        "app_information": app_data,
        "web_evidence": web_data
    }

    prompt = f"""
You are analyzing an Indian loan app for a consumer safety
research project.

Your job is to SYNTHESIZE the provided evidence.

Do NOT claim that an app is a scam unless the evidence clearly
supports that conclusion.

Do NOT invent facts.

IMPORTANT:
- Search results are evidence to evaluate, not automatically true.
- Social media or promotional claims should not be treated as
  authoritative regulatory proof.
- Distinguish between reported complaints and verified facts.
- The rule-based risk score is a signal, not an absolute truth.
- Do not make regulatory claims unless they are supported by
  the provided evidence.

EVIDENCE:

{json.dumps(evidence, indent=2, ensure_ascii=False, default=str)}

Return ONLY a JSON object with exactly these fields:

{{
    "verdict": "HIGH RISK | CAUTION | LOW RISK",
    "confidence": 0.0,
    "summary": "Short evidence-based explanation",
    "major_concerns": [],
    "positive_signals": []
}}

Confidence must be between 0 and 1.

Focus on:
- negative review sentiment
- repeated complaint categories
- fraud/scam mentions
- privacy concerns
- harassment concerns
- hidden fee concerns
- Play Store rating and scale
- privacy policy availability
- quality and relevance of web evidence
- regulatory claims

Do not treat a search result as verified regulatory evidence
unless the provided source clearly supports it.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    return json.loads(response.text)


if __name__ == "__main__":

    with open(
        "data/risk_results.json",
        "r",
        encoding="utf-8"
    ) as f:
        apps = json.load(f)

    with open(
        "data/raw/web_evidence.json",
        "r",
        encoding="utf-8"
    ) as f:
        web_evidence = json.load(f)

    web_lookup = {
        item["app_id"]: item
        for item in web_evidence
    }

    # Load existing Gemini results if available
    results_path = "data/llm_results.json"

    if os.path.exists(results_path):

        with open(
            results_path,
            "r",
            encoding="utf-8"
        ) as f:
            results = json.load(f)

    else:
        results = []

    # Apps already analyzed
    completed_ids = {
        result["app_id"]
        for result in results
    }

    remaining_apps = [
        app
        for app in apps
        if app["app_id"] not in completed_ids
    ]

    print(
        f"Already completed: {len(completed_ids)}"
    )

    print(
        f"Remaining: {len(remaining_apps)}"
    )

    for i, app in enumerate(
        remaining_apps,
        start=1
    ):

        print(
            f"\n[{i}/{len(remaining_apps)}] "
            f"Analyzing: {app['app_name']}"
        )

        app_web_evidence = web_lookup.get(
            app["app_id"],
            {}
        )

        try:

            result = analyze_app(
                app,
                app_web_evidence
            )

            results.append({
                "app_id": app["app_id"],
                "app_name": app["app_name"],
                "analysis": result
            })

            # Save after EVERY successful request
            with open(
                results_path,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    results,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            print("✓ Analysis saved")

        except Exception as e:

            print(
                f"✗ Error analyzing "
                f"{app['app_name']}: {e}"
            )

    print(
        f"\nTotal Gemini results: "
        f"{len(results)}"
    )
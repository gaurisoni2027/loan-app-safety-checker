import json
import os


RISK_FILE = "data/risk_results.json"
LLM_FILE = "data/llm_results.json"
WEB_FILE = "data/raw/web_evidence.json"

OUTPUT_FILE = "data/frontend_data.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# Load existing analysis
risk_results = load_json(RISK_FILE)
llm_results = load_json(LLM_FILE)
web_results = load_json(WEB_FILE)


# Create quick lookup dictionaries
llm_lookup = {
    item["app_id"]: item
    for item in llm_results
}

web_lookup = {
    item["app_id"]: item
    for item in web_results
}


frontend_data = []


for app in risk_results:

    app_id = app["app_id"]

    llm_data = llm_lookup.get(app_id, {})
    web_data = web_lookup.get(app_id, {})

    llm_analysis = llm_data.get(
        "analysis",
        {}
    )

    evidence = web_data.get(
        "evidence",
        []
    )


    # Keep only useful evidence fields
    clean_evidence = []

    for item in evidence:

        clean_evidence.append({
            "query": item.get("query", ""),
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "content": item.get("content", "")
        })


    combined = {

        # Basic app information
        "app_id": app_id,

        "app_name": app.get(
            "app_name",
            ""
        ),

        "developer": app.get(
            "developer",
            ""
        ),


        # Rule-based analysis
        "risk_score": app.get(
            "risk_score",
            0
        ),

        "risk_level": app.get(
            "risk_level",
            "LOW RISK"
        ),

        "risk_factors": app.get(
            "risk_factors",
            []
        ),


        # Review intelligence
        "sentiment": app.get(
            "sentiment",
            {}
        ),


        # Gemini analysis
        "llm": {

            "verdict": llm_analysis.get(
                "verdict",
                ""
            ),

            "confidence": llm_analysis.get(
                "confidence",
                0
            ),

            "summary": llm_analysis.get(
                "summary",
                ""
            ),

            "major_concerns":
                llm_analysis.get(
                    "major_concerns",
                    []
                ),

            "positive_signals":
                llm_analysis.get(
                    "positive_signals",
                    []
                )
        },


        # Web evidence
        "web_evidence": clean_evidence
    }


    frontend_data.append(
        combined
    )


# Save final frontend dataset
os.makedirs(
    "data",
    exist_ok=True
)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        frontend_data,
        f,
        indent=4,
        ensure_ascii=False
    )


print(
    f"Created {OUTPUT_FILE}"
)

print(
    f"Apps included: {len(frontend_data)}"
)
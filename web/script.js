let apps = [];
let currentFilter = "ALL";


// =========================
// LOAD DATA
// =========================
async function loadData() {

    try {

        const response = await fetch(
            "frontend_data.json"
        );

        apps = await response.json();

        updateMetrics();
        renderRiskDistribution();
        renderApps();

    } catch (error) {

        console.error(
            "Error loading frontend data:",
            error
        );

    }
}



// =========================
// METRICS
// =========================

function updateMetrics() {

    const total = apps.length;

    const high = apps.filter(
        app => app.risk_level === "HIGH RISK"
    ).length;

    const caution = apps.filter(
        app => app.risk_level === "CAUTION"
    ).length;

    document.getElementById(
        "totalApps"
    ).textContent = total;

    document.getElementById(
        "highRisk"
    ).textContent = high;

    document.getElementById(
        "cautionRisk"
    ).textContent = caution;

}


// =========================
// RISK DISTRIBUTION
// =========================

function renderRiskDistribution() {

    const container =
        document.getElementById(
            "riskDistribution"
        );

    const high = apps.filter(
        app => app.risk_level === "HIGH RISK"
    ).length;

    const caution = apps.filter(
        app => app.risk_level === "CAUTION"
    ).length;

    const low = apps.filter(
        app => app.risk_level === "LOW RISK"
    ).length;


    container.innerHTML = `

        <div class="risk-block">

            <span>HIGH RISK</span>

            <strong>
                ${high}
            </strong>

        </div>


        <div class="risk-block">

            <span>CAUTION</span>

            <strong>
                ${caution}
            </strong>

        </div>


        <div class="risk-block">

            <span>LOWER RISK</span>

            <strong>
                ${low}
            </strong>

        </div>

    `;
}


// =========================
// APP CARDS
// =========================

function renderApps() {

    const grid =
        document.getElementById(
            "appGrid"
        );

    const searchValue =
        document.getElementById(
            "searchInput"
        ).value.toLowerCase();


    const filteredApps = apps.filter(app => {

        const matchesFilter =
            currentFilter === "ALL" ||
            app.risk_level === currentFilter;


        const matchesSearch =
            app.app_name
                .toLowerCase()
                .includes(searchValue);


        return (
            matchesFilter &&
            matchesSearch
        );

    });


    grid.innerHTML = "";


    filteredApps.forEach(app => {

        const card =
            document.createElement("div");

        card.className =
            "app-card";


        const riskClass =
            getRiskClass(
                app.risk_level
            );


        const reason =
            getMainReason(app);


        card.innerHTML = `

            <div class="app-card-header">

                <div>

                    <div class="app-name">
                        ${app.app_name}
                    </div>

                    <div class="app-developer">
                        ${app.developer || "Unknown developer"}
                    </div>

                </div>


                <div class="risk-score">
                    ${app.risk_score}
                </div>

            </div>


            <span class="risk-label ${riskClass}">
                ${app.risk_level}
            </span>


            <div class="card-reason">
                ${reason}
            </div>

        `;


        card.addEventListener(
            "click",
            () => openDetails(app)
        );


        grid.appendChild(card);

    });


    if (filteredApps.length === 0) {

        grid.innerHTML = `
            <p style="
                color: #8b909c;
                font-size: 12px;
                padding: 30px 0;
            ">
                No apps match your search.
            </p>
        `;

    }

}


// =========================
// RISK CLASS
// =========================

function getRiskClass(level) {

    if (level === "HIGH RISK") {
        return "risk-high";
    }

    if (level === "CAUTION") {
        return "risk-caution";
    }

    return "risk-low";
}


// =========================
// MAIN REASON
// =========================

function getMainReason(app) {

    if (
        app.risk_factors &&
        app.risk_factors.length > 0
    ) {

        return app.risk_factors[0];

    }


    if (
        app.llm &&
        app.llm.major_concerns &&
        app.llm.major_concerns.length > 0
    ) {

        return app.llm.major_concerns[0];

    }


    return "No major risk signals detected.";
}

function truncateText(text, maxLength) {

    if (!text) {
        return "";
    }

    if (text.length <= maxLength) {
        return text;
    }

    return text.substring(0, maxLength) + "...";
}


// =========================
// DETAIL DRAWER
// =========================

function openDetails(app) {

    const overlay =
        document.getElementById(
            "detailOverlay"
        );

    const content =
        document.getElementById(
            "detailContent"
        );


    const llm =
        app.llm || {};


    const concerns =
        llm.major_concerns || [];


    const positives =
        llm.positive_signals || [];


    const riskFactors =
        app.risk_factors || [];

    const webEvidence =
        app.web_evidence || [];


    const reviewStats =
        app.sentiment || {};


    content.innerHTML = `

        <div class="detail-header">

            <span class="section-kicker">
                APP INVESTIGATION
            </span>

            <h2 style="
                margin-top: 10px;
                font-size: 32px;
                letter-spacing: -1.5px;
            ">
                ${app.app_name}
            </h2>

            <p style="
                color: #8b909c;
                font-size: 11px;
                margin-top: 5px;
            ">
                ${app.developer || ""}
            </p>

        </div>


        <div style="
            display: flex;
            align-items: center;
            gap: 25px;
            margin-top: 35px;
        ">

            <div>

                <div style="
                    font-family: 'DM Mono';
                    font-size: 10px;
                    color: #8b909c;
                ">
                    RISK SCORE
                </div>

                <strong style="
                    display: block;
                    font-size: 52px;
                    letter-spacing: -3px;
                ">
                    ${app.risk_score}
                </strong>

            </div>


            <span class="
                risk-label
                ${getRiskClass(app.risk_level)}
            ">
                ${app.risk_level}
            </span>

        </div>


        <div style="
            margin-top: 35px;
            padding: 20px;
            background: #101217;
            border: 1px solid #242833;
            border-radius: 10px;
        ">

            <span class="section-kicker">
                AI ASSESSMENT
            </span>

            <p style="
                margin-top: 12px;
                color: #d2d5da;
                font-size: 12px;
                line-height: 1.7;
            ">
                ${llm.summary || "No AI assessment available."}
            </p>

            ${
                llm.confidence !== undefined
                ? `
                    <div style="
                        margin-top: 15px;
                        color: #8b909c;
                        font-family: 'DM Mono';
                        font-size: 9px;
                    ">
                        AI CONFIDENCE:
                        ${Math.round(
                            llm.confidence * 100
                        )}%
                    </div>
                `
                : ""
            }

        </div>


        <div style="
            margin-top: 25px;
        ">

            <span class="section-kicker">
                RISK SIGNALS
            </span>

            <div style="
                margin-top: 12px;
            ">

                ${
                    riskFactors.length
                    ? riskFactors.map(
                        factor => `
                            <div style="
                                padding: 11px 0;
                                border-bottom: 1px solid #20242c;
                                color: #c7cad0;
                                font-size: 11px;
                            ">
                                ⚠ ${factor}
                            </div>
                        `
                    ).join("")
                    : `
                        <p style="
                            color: #8b909c;
                            font-size: 11px;
                        ">
                            No major rule-based concerns.
                        </p>
                    `
                }

            </div>

        </div>


        <div style="
            margin-top: 25px;
        ">

            <span class="section-kicker">
                REVIEW INTELLIGENCE
            </span>

            <div style="
                display: grid;
                grid-template-columns:
                    repeat(3, 1fr);
                gap: 8px;
                margin-top: 12px;
            ">

                ${reviewBox(
                    "POSITIVE",
                    reviewStats.positive || 0
                )}

                ${reviewBox(
                    "NEUTRAL",
                    reviewStats.neutral || 0
                )}

                ${reviewBox(
                    "NEGATIVE",
                    reviewStats.negative || 0
                )}

            </div>

        </div>


        <div style="
            margin-top: 25px;
        ">

            <span class="section-kicker">
                AI CONCERNS
            </span>

            <div style="
                margin-top: 12px;
            ">

                ${
                    concerns.length
                    ? concerns.map(
                        item => `
                            <div style="
                                color: #c7cad0;
                                font-size: 11px;
                                padding: 8px 0;
                            ">
                                • ${item}
                            </div>
                        `
                    ).join("")
                    : `
                        <p style="
                            color: #8b909c;
                            font-size: 11px;
                        ">
                            No major concerns identified.
                        </p>
                    `
                }

            </div>

        </div>


        <div style="
            margin-top: 25px;
        ">

            <span class="section-kicker">
                POSITIVE SIGNALS
            </span>

            <div style="
                margin-top: 12px;
            ">

                ${
                    positives.length
                    ? positives.map(
                        item => `
                            <div style="
                                color: #62d99b;
                                font-size: 11px;
                                padding: 8px 0;
                            ">
                                ✓ ${item}
                            </div>
                        `
                    ).join("")
                    : `
                        <p style="
                            color: #8b909c;
                            font-size: 11px;
                        ">
                            No positive signals recorded.
                        </p>
                    `
                }

            </div>

        </div>

                <div style="
            margin-top: 30px;
        ">

            <span class="section-kicker">
                WEB EVIDENCE
            </span>

            <p style="
                color: #8b909c;
                font-size: 10px;
                margin-top: 8px;
            ">
                External sources found during targeted research.
            </p>


            <div style="
                margin-top: 15px;
            ">

                ${
                    webEvidence.length
                    ? webEvidence.slice(0, 5).map(
                        source => `

                            <div style="
                                background: #101217;
                                border: 1px solid #242833;
                                border-radius: 9px;
                                padding: 15px;
                                margin-bottom: 9px;
                            ">

                                <div style="
                                    color: #b7f34a;
                                    font-family: 'DM Mono';
                                    font-size: 8px;
                                    letter-spacing: 0.7px;
                                ">
                                    ${source.query || "WEB SEARCH"}
                                </div>


                                <div style="
                                    margin-top: 7px;
                                    color: #e1e3e7;
                                    font-size: 11px;
                                    font-weight: 700;
                                    line-height: 1.4;
                                ">
                                    ${source.title || "Untitled source"}
                                </div>


                                <p style="
                                    margin-top: 8px;
                                    color: #8b909c;
                                    font-size: 10px;
                                    line-height: 1.5;
                                ">
                                    ${truncateText(
                                        source.content || "",
                                        180
                                    )}
                                </p>


                                ${
                                    source.url
                                    ? `
                                        <a
                                            href="${source.url}"
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            style="
                                                display: inline-block;
                                                margin-top: 10px;
                                                color: #b7f34a;
                                                font-family: 'DM Mono';
                                                font-size: 9px;
                                                text-decoration: none;
                                            "
                                        >
                                            VIEW SOURCE →
                                        </a>
                                    `
                                    : ""
                                }

                            </div>

                        `
                    ).join("")
                    : `
                        <p style="
                            color: #8b909c;
                            font-size: 11px;
                        ">
                            No external evidence found.
                        </p>
                    `
                }

            </div>

        </div>

    `;


    overlay.classList.add("open");
}


// =========================
// REVIEW BOX
// =========================

function reviewBox(label, value) {

    return `

        <div style="
            background: #101217;
            border: 1px solid #242833;
            border-radius: 8px;
            padding: 12px;
        ">

            <div style="
                color: #8b909c;
                font-family: 'DM Mono';
                font-size: 8px;
            ">
                ${label}
            </div>

            <strong style="
                display: block;
                margin-top: 6px;
                font-size: 20px;
            ">
                ${value}
            </strong>

        </div>

    `;
}


// =========================
// SEARCH
// =========================

document
    .getElementById("searchInput")
    .addEventListener(
        "input",
        renderApps
    );


// =========================
// FILTERS
// =========================

document
    .querySelectorAll(".filter")
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                document
                    .querySelectorAll(".filter")
                    .forEach(
                        btn =>
                            btn.classList.remove(
                                "active"
                            )
                    );


                button.classList.add(
                    "active"
                );


                currentFilter =
                    button.dataset.filter;


                renderApps();

            }
        );

    });


// =========================
// CLOSE DRAWER
// =========================

document
    .getElementById("closeDrawer")
    .addEventListener(
        "click",
        () => {

            document
                .getElementById(
                    "detailOverlay"
                )
                .classList.remove(
                    "open"
                );

        }
    );


document
    .getElementById("detailOverlay")
    .addEventListener(
        "click",
        event => {

            if (
                event.target.id ===
                "detailOverlay"
            ) {

                event.currentTarget
                    .classList.remove(
                        "open"
                    );

            }

        }
    );


// =========================
// START
// =========================

loadData();
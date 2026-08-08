# 🛡️ LoanGuard — Evidence-Driven AI Loan App Risk Intelligence

LoanGuard is an evidence-driven system that analyzes loan applications listed on the Google Play Store and generates an explainable safety/risk assessment.

It combines **Play Store metadata, user review intelligence, web research, rule-based risk scoring, and Gemini-based analysis** to help users understand potential risks before using a loan app.

> **Know the risk before you borrow.**

---

## 🚀 Live Demo

Live Application: https://loan-app-safety-checker-kappa.vercel.app/

Demo Video: https://drive.google.com/file/d/19Am1jVffVd4K56w68pVmgMwPa6WD0pJY/view?usp=sharing

---

## 📌 Problem Statement

Loan applications can appear trustworthy because of high download counts or ratings, while user experiences may reveal issues such as:

- Fraud or scam complaints
- Privacy concerns
- Repayment problems
- Hidden fees
- Poor customer support
- Delayed loan approvals or disbursements
- Negative user experiences

Manually checking all of these signals across different sources is time-consuming.

LoanGuard automates this process by collecting and combining multiple evidence sources into one explainable risk assessment.

---

## 🎯 Assignment Objective

The system was built to:

- Discover loan apps available on Google Play Store
- Collect Play Store metadata
- Collect and analyze user reviews
- Search the web for additional information
- Identify common complaints and positive signals
- Generate a risk score and risk level
- Provide a short explanation for the verdict
- Present the results through an interactive web interface
- Deploy the final application publicly

---

## ✨ Key Features

### 1. Play Store App Discovery

LoanGuard discovers loan applications and collects information such as:

- App name
- Developer
- Description
- Rating
- Number of ratings
- Review count
- Install count
- Category
- Last updated date
- Privacy policy

The current analysis contains **20 loan applications**.

---

### 2. User Review Intelligence

The system analyzes collected Play Store reviews using NLP techniques.

It performs:

- Sentiment analysis
- Complaint categorization
- TF-IDF analysis
- Identification of important review patterns

Current review dataset:

**600 reviews**

Sentiment distribution:

| Sentiment | Count |
|-----------|------:|
| Positive | 438 |
| Neutral | 86 |
| Negative | 76 |

Complaint categories currently include:

- Fraud / Scam
- Privacy
- Repayment
- Hidden Fees

---

### 3. Web Evidence Collection

LoanGuard uses web search to gather additional evidence about each application.

Search queries include:

- `"App Name" RBI`
- `"App Name" complaint`
- `"App Name" scam`

The collected evidence can include information from:

- News
- Public websites
- Forums
- Other web sources

This helps the system go beyond Play Store reviews and consider external signals.

---

### 4. Rule-Based Risk Engine

A rule-based risk engine combines signals from the collected data.

Risk factors can include:

- High negative review sentiment
- Fraud/scam mentions
- Privacy complaints
- Hidden-fee complaints
- Other negative review signals

The system generates:

- Risk Score
- Risk Level
- Risk Factors

Example:

**Buddy Loan — Personal Loan App**

- Risk Score: **70**
- Risk Level: **HIGH RISK**
- High negative review sentiment
- 9 reviews mentioning fraud/scam
- 5 privacy-related complaints
- 2 hidden-fee complaints

---

### 5. Gemini AI Analysis

The system also uses Gemini to provide a higher-level interpretation of the collected evidence.

The AI analysis produces:

- Verdict
- Confidence score
- Summary
- Major concerns
- Positive signals

The LLM does not replace the rule-based analysis. Instead, it helps convert the collected signals into an understandable explanation.

---

### 6. Evidence-Based Investigation

Each application can be opened in the web interface to view its detailed investigation.

The investigation includes:

- Risk score
- Risk level
- AI assessment
- AI confidence
- Risk signals
- Review intelligence
- AI concerns
- Positive signals
- Supporting web evidence

This makes the final verdict more explainable instead of presenting only a single risk number.

---

## 🧠 System Workflow

```text
                 Google Play Store
                        │
                        ▼
                 App Discovery
                        │
                        ▼
              Play Store Metadata
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
        User Reviews          Web Research
             │                     │
             ▼                     ▼
      NLP / Sentiment        External Evidence
      Complaint Analysis
             │                     │
             └──────────┬──────────┘
                        ▼
                Risk Rule Engine
                        │
                        ▼
                  Gemini Analysis
                        │
                        ▼
             Explainable Risk Result
                        │
                        ▼
                LoanGuard Dashboard
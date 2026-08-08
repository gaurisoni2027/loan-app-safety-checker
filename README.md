# 🛡️ LoanGuard — Evidence-Driven AI Loan App Risk Intelligence

> An AI-powered system for analyzing Indian loan applications using Google Play Store data, review intelligence, rule-based risk scoring, web research, and Gemini-powered analysis.

---

## 📌 Overview

LoanGuard is an AI/data product designed to help users understand potential risk signals associated with digital loan applications before using them.

Instead of simply asking an LLM:

> "Is this loan app safe?"

LoanGuard follows an **evidence-first approach**.

It collects and analyzes multiple signals from:

- Google Play Store metadata
- User reviews
- Sentiment analysis
- TF-IDF based review analysis
- Complaint patterns
- Rule-based risk scoring
- Targeted web research
- Gemini LLM analysis

These signals are then combined into an explainable assessment that shows **why an application may require caution**.

---

## 🎯 Problem Statement

The growth of digital lending applications makes it difficult for users to distinguish between applications with strong trust signals and applications that may require additional caution.

A simple Play Store rating is not enough, and asking an LLM to directly classify an application as "safe" or "unsafe" can produce unreliable conclusions.

LoanGuard addresses this by combining:

```text
Real Application Data
        ↓
User Review Intelligence
        ↓
ML / NLP Signals
        ↓
Rule-Based Risk Engine
        ↓
Web Evidence
        ↓
Gemini AI Synthesis
        ↓
Explainable Risk Assessment
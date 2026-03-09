# AI‑Driven Adaptive Diagnostic Engine (Internship Project Guide)

## Overview

This project implements a **1‑Dimensional Adaptive Testing System** that
dynamically adjusts question difficulty based on a student's previous
answers. The system estimates a student's ability score and selects
questions accordingly.

The system architecture includes: - FastAPI backend - MongoDB database -
Adaptive algorithm (IRT-inspired) - LLM-based personalized study plan
generator

------------------------------------------------------------------------

# System Architecture

    Student
       ↓
    FastAPI Backend
       ↓
    Adaptive Engine (Python)
       ↓
    MongoDB (Questions + Sessions)
       ↓
    LLM Study Plan Generator

------------------------------------------------------------------------

# Tech Stack

  Component               Technology
  ----------------------- --------------------
  Backend                 FastAPI
  Database                MongoDB Atlas
  Language                Python
  AI Integration          OpenAI / Anthropic
  Deployment (optional)   Render / Railway

------------------------------------------------------------------------

# Project Folder Structure

    adaptive-diagnostic-engine
    │
    ├── app
    │   ├── main.py
    │   ├── database.py
    │   ├── models.py
    │   ├── adaptive_engine.py
    │   ├── routes.py
    │   └── ai_service.py
    │
    ├── data
    │   └── seed_questions.py
    │
    ├── requirements.txt
    ├── README.md
    └── .env

------------------------------------------------------------------------

# Phase 1 --- Data Modeling

## Questions Collection

Example document

``` json
{
  "_id": "q101",
  "question": "Solve: 2x + 5 = 11",
  "options": ["2", "3", "4", "5"],
  "correct_answer": "3",
  "difficulty": 0.4,
  "topic": "Algebra",
  "tags": ["linear equations"]
}
```

Required fields:

  Field            Description
  ---------------- ---------------------------
  question         Question text
  options          Multiple choice options
  correct_answer   Correct option
  difficulty       Value between 0.1 and 1.0
  topic            Subject area
  tags             Subtopics

Minimum requirement: **20 GRE-style questions**

------------------------------------------------------------------------

## UserSession Collection

Example document

``` json
{
  "_id": "session123",
  "ability_score": 0.5,
  "questions_answered": 3,
  "correct_answers": 2,
  "history": [
    {
      "question_id": "q1",
      "difficulty": 0.5,
      "correct": true
    }
  ]
}
```

Fields:

  Field                Description
  -------------------- -------------------------------
  ability_score        Current ability estimate
  questions_answered   Number of questions attempted
  correct_answers      Number answered correctly
  history              Log of responses

------------------------------------------------------------------------

# Phase 2 --- Adaptive Algorithm

## Starting Ability

    ability = 0.5

## Ability Update Rule

    if correct:
        ability += 0.07
    else:
        ability -= 0.07

Clamp ability between 0.1 and 1.0

    ability = max(0.1, min(1.0, ability))

## Question Selection

Select the question whose difficulty is closest to the current ability.

Example:

  Ability   Selected Question Difficulty
  --------- ------------------------------
  0.50      0.52
  0.57      0.60
  0.64      0.65

------------------------------------------------------------------------

# API Endpoints

## Start Session

    POST /start-session

Creates a new session

Response:

    {
    "session_id": "abc123",
    "ability": 0.5
    }

------------------------------------------------------------------------

## Get Next Question

    GET /next-question/{session_id}

Returns the question closest to the student's ability level.

------------------------------------------------------------------------

## Submit Answer

    POST /submit-answer

Example payload

    {
    "session_id": "abc123",
    "question_id": "q10",
    "answer": "B"
    }

Updates:

-   ability score
-   session history
-   question count

------------------------------------------------------------------------

# Phase 3 --- AI Study Plan (Bonus)

After **10 questions**, generate a personalized learning plan.

Input to LLM

    {
    "weak_topics": ["Algebra", "Probability"],
    "accuracy": 60,
    "max_difficulty": 0.7
    }

Prompt example

    Generate a 3 step GRE study plan for a student weak in Algebra and Probability.
    Student accuracy is 60%.
    Maximum difficulty reached is 0.7.

Example Output

1.  Review algebra fundamentals and formulas.
2.  Practice medium difficulty GRE probability problems.
3.  Take timed mixed-topic practice tests.

------------------------------------------------------------------------

# Environment Variables

Create a `.env` file

    MONGO_URI=your_mongodb_connection_string
    OPENAI_API_KEY=your_api_key

------------------------------------------------------------------------

# Running the Project

Install dependencies

    pip install -r requirements.txt

Run server

    uvicorn app.main:app --reload

API docs automatically available at

    http://localhost:8000/docs

------------------------------------------------------------------------

# Evaluation Criteria

  Criteria        What Reviewers Look For
  --------------- ------------------------------------
  System Design   Clean MongoDB schema
  Algorithm       Logical difficulty progression
  AI Usage        Proper prompt design
  Code Quality    Modular, typed, error-handled code

------------------------------------------------------------------------

# AI Log (Example)

AI tools used:

-   ChatGPT → architecture planning
-   Cursor → code generation
-   Copilot → autocomplete

Challenges:

-   Selecting the best difficulty matching strategy
-   Designing a clean session tracking schema

Solutions:

-   Used ability‑difference sorting
-   Implemented modular backend structure

------------------------------------------------------------------------

# Submission Checklist

Before submitting ensure:

-   GitHub repository created
-   README included
-   MongoDB schema documented
-   API endpoints working
-   Adaptive algorithm explained
-   AI usage documented

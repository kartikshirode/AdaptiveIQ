<div align="center">

# 🧠 AdaptiveIQ — Adaptive Diagnostic Engine

**An AI-driven adaptive testing system that dynamically adjusts question difficulty based on student performance.**

Built with **FastAPI** · **MongoDB Atlas** · **Google Gemini**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?logo=mongodb&logoColor=white)](https://www.mongodb.com/atlas)
[![Gemini](https://img.shields.io/badge/Gemini-2.0_Flash-4285F4?logo=google&logoColor=white)](https://ai.google.dev)

</div>

---

## 📌 Overview

AdaptiveIQ implements a **1-Dimensional Adaptive Testing System** inspired by Item Response Theory (IRT). It estimates a student's ability in real time and selects GRE-style questions that match their current level — making every test session unique and personalized.

```
Student  →  FastAPI Backend  →  Adaptive Engine  →  MongoDB
                                                       ↓
                                              Gemini Study Plan
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Adaptive Question Selection** | Picks the question whose difficulty is closest to the student's current ability |
| **Real-time Ability Tracking** | Ability updates after every answer (`+0.07` correct, `−0.07` incorrect), clamped to `[0.1, 1.0]` |
| **Session Management** | Tracks answer history, accuracy, and ability progression per session |
| **AI Study Plans** | Generates personalized 3-step study plans via Google Gemini after 10+ questions |
| **Duplicate Prevention** | No question is repeated within the same session |
| **Input Validation** | Session IDs are validated; malformed requests return clear error messages |

---

## 🛠 Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Backend | FastAPI | Async REST API framework |
| Database | MongoDB Atlas (M0 Free) | Cloud-hosted document store |
| Async Driver | Motor | Non-blocking MongoDB operations |
| Data Validation | Pydantic v2 | Request/response schemas |
| AI Integration | Google Gemini (`2.0-flash`) | Study plan generation |
| Environment | python-dotenv | Secrets management |

---

## 📁 Project Structure

```
AdaptiveIQ/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI app, lifespan, CORS
│   ├── database.py           # Motor async MongoDB connection
│   ├── models.py             # Pydantic schemas & response models
│   ├── adaptive_engine.py    # Ability update & question selection logic
│   ├── routes.py             # All API endpoints
│   └── ai_service.py         # Gemini study plan generation
│
├── data/
│   ├── __init__.py
│   └── seed_questions.py     # 22 GRE-style seed questions + CLI seeder
│
├── .env                      # Environment variables (git-ignored)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [MongoDB Atlas account](https://www.mongodb.com/atlas) (free M0 tier)
- [Google Gemini API key](https://aistudio.google.com/apikey)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AdaptiveIQ.git
cd AdaptiveIQ
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file in the project root:

```env
MONGO_URI=mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Seed the Database

```bash
python -m data.seed_questions
```

> Seeds 22 GRE-style questions across Algebra, Arithmetic, Geometry, Probability, and Number Properties.

### 5. Start the Server

```bash
uvicorn app.main:app --reload
```

### 6. Open API Docs

Navigate to **http://localhost:8000/docs** — interactive Swagger UI is auto-generated.

---

## 📡 API Reference

### `POST /start-session`

Creates a new adaptive testing session.

**Response** `200 OK`
```json
{
  "session_id": "65f1a2b3c4d5e6f7a8b9c0d1",
  "ability": 0.5
}
```

---

### `GET /next-question/{session_id}`

Returns the next question matched to the student's ability. Correct answer is **not** exposed.

**Response** `200 OK`
```json
{
  "_id": "q4",
  "question": "Simplify: (2x³)(3x²)",
  "options": ["5x⁵", "6x⁵", "6x⁶", "5x⁶"],
  "difficulty": 0.5,
  "topic": "Algebra",
  "tags": ["exponents"]
}
```

---

### `POST /submit-answer`

Submits an answer and updates the ability score.

**Request**
```json
{
  "session_id": "65f1a2b3c4d5e6f7a8b9c0d1",
  "question_id": "q4",
  "answer": "6x⁵"
}
```

**Response** `200 OK`
```json
{
  "correct": true,
  "correct_answer": "6x⁵",
  "new_ability": 0.57,
  "questions_answered": 1
}
```

---

### `GET /study-plan/{session_id}`

Generates a personalized study plan via Gemini. **Requires 10+ answered questions.**

**Response** `200 OK`
```json
{
  "session_id": "65f1a2b3c4d5e6f7a8b9c0d1",
  "accuracy": 60.0,
  "max_difficulty": 0.75,
  "weak_topics": ["Algebra", "Probability"],
  "study_plan": "1. Review algebra fundamentals and core formulas.\n2. Practice medium-difficulty probability problems.\n3. Take timed mixed-topic practice tests."
}
```

---

## 🧮 Adaptive Algorithm

The engine uses a simplified IRT-inspired approach:

```
Initial ability = 0.5

For each answer:
    if correct  → ability += 0.07
    if wrong    → ability -= 0.07

    ability = clamp(ability, 0.1, 1.0)

Next question = argmin |question.difficulty − ability|
                where question not already answered
```

**Example progression:**

| Step | Answer  | Ability | Next Question Difficulty |
|------|---------|---------|------------------------|
| 1    | —       | 0.50    | 0.50                   |
| 2    | Correct | 0.57    | 0.55                   |
| 3    | Correct | 0.64    | 0.65                   |
| 4    | Wrong   | 0.57    | 0.55                   |

---

## 🗃 MongoDB Schema

### `questions` Collection

| Field | Type | Description |
|-------|------|-------------|
| `_id` | String | Unique question ID (e.g., `"q1"`) |
| `question` | String | Question text |
| `options` | Array\<String\> | Multiple choice options |
| `correct_answer` | String | Correct option value |
| `difficulty` | Float | Difficulty level `[0.1 – 1.0]` |
| `topic` | String | Subject area |
| `tags` | Array\<String\> | Subtopic tags |

### `sessions` Collection

| Field | Type | Description |
|-------|------|-------------|
| `_id` | ObjectId | Auto-generated session ID |
| `ability_score` | Float | Current ability estimate |
| `questions_answered` | Int | Total questions attempted |
| `correct_answers` | Int | Total correct responses |
| `history` | Array\<Object\> | Per-question response log |

---

## 🤖 AI Usage Log

| Tool | Usage |
|------|-------|
| **Google Gemini** (`gemini-2.0-flash`) | Generates personalized 3-step GRE study plans from weak topics, accuracy, and max difficulty |
| **GitHub Copilot** | Code generation and autocomplete assistance during development |

### Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Best difficulty matching strategy | Sorted unanswered questions by absolute distance from ability score |
| Clean session tracking schema | Modular Pydantic models with embedded history array |
| Robust error handling | ObjectId validation helper + try/except on Gemini API calls |

---

## 📋 Submission Checklist

- [x] GitHub repository created
- [x] README with full documentation
- [x] MongoDB schema documented
- [x] API endpoints working (4 endpoints)
- [x] Adaptive algorithm explained
- [x] 22 GRE-style seed questions (5 topics)
- [x] AI-powered study plan generation
- [x] AI usage documented
- [x] Error handling & input validation
- [x] `.gitignore` configured

---

## 📄 License

This project is for educational and internship evaluation purposes.

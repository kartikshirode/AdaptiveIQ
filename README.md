# 🧠 AdaptiveIQ — Adaptive Diagnostic Engine

**An AI-driven adaptive testing system that dynamically adjusts question difficulty based on student performance.**

Built with **FastAPI** · **MongoDB Atlas** · **NVIDIA Kimi K2**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?logo=mongodb&logoColor=white)](https://www.mongodb.com/atlas)
[![NVIDIA](https://img.shields.io/badge/NVIDIA-Kimi_K2-76B900?logo=nvidia&logoColor=white)](https://build.nvidia.com)

---

## 📌 Overview

AdaptiveIQ implements a **1-Dimensional Adaptive Testing System** inspired by Item Response Theory (IRT). It estimates a student's ability in real time and selects GRE-style questions that match their current level — making every test session unique and personalized.

```
Student  →  FastAPI Backend  →  Adaptive Engine  →  MongoDB
                                                       ↓
                                              NVIDIA Kimi K2 Study Plan
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Adaptive Question Selection** | Picks questions whose difficulty is closest to the student's current ability |
| **Randomized Selection** | Adds unpredictability by selecting from top 5 closest questions |
| **Real-time Ability Tracking** | Ability updates after every answer (+0.07 correct, −0.07 incorrect), clamped to [0.1, 1.0] |
| **Session Management** | Tracks answer history, accuracy, and ability progression per session |
| **AI Study Plans** | Generates personalized 3-step study plans via NVIDIA Kimi K2 after 10 questions |
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
| AI Integration | NVIDIA Kimi K2 (via OpenAI-compatible API) | Study plan generation |
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
│   ├── ai_service.py         # NVIDIA Kimi K2 study plan generation
│   └── static/
│       └── index.html        # Beautiful dark-themed UI
│
├── data/
│   ├── __init__.py
│   └── seed_questions.py     # 50 GRE-style seed questions
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
- [NVIDIA API Key](https://build.nvidia.com) (free tier available)

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
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxx
```

### 4. Seed the Database

```bash
python -m data.seed_questions
```

> Seeds 50 GRE-style questions across Algebra and Arithmetic topics.

### 5. Start the Server

```bash
uvicorn app.main:app --reload
```

### 6. Open the Application

Navigate to **http://localhost:8000** — Beautiful dark-themed UI with adaptive testing!

---

## 📡 API Documentation

> Interactive docs available at **http://localhost:8000/docs** (Swagger UI) and **http://localhost:8000/redoc** (ReDoc) when the server is running.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/start-session` | Create a new adaptive testing session |
| `GET` | `/next-question/{session_id}` | Get next question matched to student's ability |
| `POST` | `/submit-answer` | Submit an answer and update ability score |
| `GET` | `/study-plan/{session_id}` | Generate AI study plan (after 10 questions) |

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
  "_id": "alg_4",
  "question": "Simplify: x + x + x",
  "options": ["3x", "x³", "x + 3", "x"],
  "difficulty": 0.1,
  "topic": "Algebra",
  "tags": ["simplification"]
}
```

---

### `POST /submit-answer`

Submits an answer and updates the ability score.

**Request**
```json
{
  "session_id": "65f1a2b3c4d5e6f7a8b9c0d1",
  "question_id": "alg_4",
  "answer": "3x"
}
```

**Response** `200 OK`
```json
{
  "correct": true,
  "correct_answer": "3x",
  "new_ability": 0.57,
  "questions_answered": 1
}
```

---

### `GET /study-plan/{session_id}`

Generates a personalized study plan via NVIDIA Kimi K2. **Requires 10 answered questions.**

**Response** `200 OK`
```json
{
  "session_id": "65f1a2b3c4d5e6f7a8b9c0d1",
  "accuracy": 60.0,
  "max_difficulty": 0.75,
  "weak_topics": ["Algebra", "Arithmetic"],
  "study_plan": "1. Reset foundations: complete one focused Algebra module...\n2. Daily 15-minute micro-drills...\n3. Week-end 30-minute mixed sets..."
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

Next question = random.choice(top 5 closest questions by |difficulty − ability|)
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
| `_id` | String | Unique question ID (e.g., `"alg_1"`) |
| `question` | String | Question text |
| `options` | Array\<String\> | Multiple choice options |
| `correct_answer` | String | Correct option value |
| `difficulty` | Float | Difficulty level [0.1 – 1.0] |
| `topic` | String | Subject area (Algebra/Arithmetic) |
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
| **NVIDIA Kimi K2** | Generates personalized 3-step GRE study plans from weak topics, accuracy, and max difficulty |
| **GitHub Copilot** | Code generation and autocomplete assistance during development |

### Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Best difficulty matching strategy | Sorted unanswered questions by absolute distance from ability score, then randomly select from top 5 |
| Clean session tracking schema | Modular Pydantic models with embedded history array |
| Initial question predictability | Added 10+ questions near difficulty 0.5 for balanced start |
| API quota limits | Switched from Gemini to NVIDIA Kimi K2 which has generous free tier |



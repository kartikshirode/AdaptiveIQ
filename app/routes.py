from collections import defaultdict

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException

from app.adaptive_engine import select_next_question, update_ability
from app.ai_service import generate_study_plan
from app.database import get_questions_collection, get_sessions_collection
from app.models import QuestionOut, StudyPlanResponse, SubmitAnswerRequest

router = APIRouter()

MAX_QUESTIONS = 10


def get_valid_object_id(session_id: str) -> ObjectId:
    """Validate and convert session_id to ObjectId."""
    try:
        return ObjectId(session_id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Invalid session ID format")


# ── POST /start-session ──────────────────────────────────────────────
@router.post("/start-session")
async def start_session():
    """Create a new adaptive testing session."""
    session_doc = {
        "ability_score": 0.5,
        "questions_answered": 0,
        "correct_answers": 0,
        "history": [],
    }
    result = await get_sessions_collection().insert_one(session_doc)
    return {"session_id": str(result.inserted_id), "ability": 0.5}


# ── GET /next-question/{session_id} ──────────────────────────────────
@router.get("/next-question/{session_id}")
async def next_question(session_id: str):
    """Return the question closest to the student's current ability level."""
    oid = get_valid_object_id(session_id)
    session = await get_sessions_collection().find_one({"_id": oid})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session["questions_answered"] >= MAX_QUESTIONS:
        raise HTTPException(status_code=400, detail=f"Test completed ({MAX_QUESTIONS} questions)")

    answered_ids = [h["question_id"] for h in session["history"]]
    question = await select_next_question(
        session["ability_score"], answered_ids, get_questions_collection()
    )

    if not question:
        raise HTTPException(status_code=404, detail="No more questions available")

    return QuestionOut(**question)


# ── POST /submit-answer ──────────────────────────────────────────────
@router.post("/submit-answer")
async def submit_answer(payload: SubmitAnswerRequest):
    """Submit an answer, update ability score, and return feedback."""
    oid = get_valid_object_id(payload.session_id)
    session = await get_sessions_collection().find_one({"_id": oid})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    question = await get_questions_collection().find_one({"_id": payload.question_id})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Check if question was already answered in this session
    answered_ids = [h["question_id"] for h in session["history"]]
    if payload.question_id in answered_ids:
        raise HTTPException(status_code=400, detail="Question already answered in this session")

    is_correct = payload.answer == question["correct_answer"]
    new_ability = update_ability(session["ability_score"], is_correct)

    record = {
        "question_id": payload.question_id,
        "difficulty": question["difficulty"],
        "correct": is_correct,
        "topic": question["topic"],
    }

    await get_sessions_collection().update_one(
        {"_id": oid},
        {
            "$set": {"ability_score": new_ability},
            "$inc": {
                "questions_answered": 1,
                "correct_answers": 1 if is_correct else 0,
            },
            "$push": {"history": record},
        },
    )

    return {
        "correct": is_correct,
        "correct_answer": question["correct_answer"],
        "new_ability": new_ability,
        "questions_answered": session["questions_answered"] + 1,
    }


# ── GET /study-plan/{session_id} ─────────────────────────────────────
@router.get("/study-plan/{session_id}", response_model=StudyPlanResponse)
async def study_plan(session_id: str):
    """Generate a personalized study plan (available after completing test)."""
    oid = get_valid_object_id(session_id)
    session = await get_sessions_collection().find_one({"_id": oid})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session["questions_answered"] < MAX_QUESTIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Complete all {MAX_QUESTIONS} questions first ({session['questions_answered']}/{MAX_QUESTIONS} completed)",
        )

    # Compute per-topic accuracy
    topic_stats: dict[str, dict] = defaultdict(lambda: {"correct": 0, "total": 0})
    max_diff = 0.0
    for h in session["history"]:
        topic = h.get("topic", "Unknown")
        topic_stats[topic]["total"] += 1
        if h["correct"]:
            topic_stats[topic]["correct"] += 1
        max_diff = max(max_diff, h["difficulty"])

    weak_topics = [
        topic
        for topic, stats in topic_stats.items()
        if stats["total"] > 0 and (stats["correct"] / stats["total"]) < 0.5
    ]

    overall_accuracy = (
        (session["correct_answers"] / session["questions_answered"]) * 100
        if session["questions_answered"] > 0
        else 0
    )

    plan_text = await generate_study_plan(weak_topics, overall_accuracy, max_diff)

    return StudyPlanResponse(
        session_id=session_id,
        accuracy=round(overall_accuracy, 1),
        max_difficulty=round(max_diff, 2),
        weak_topics=weak_topics,
        study_plan=plan_text,
    )

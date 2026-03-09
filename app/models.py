from pydantic import BaseModel, Field
from typing import Optional


class Question(BaseModel):
    id: str = Field(alias="_id")
    question: str
    options: list[str]
    correct_answer: str
    difficulty: float = Field(ge=0.1, le=1.0)
    topic: str
    tags: list[str] = []

    model_config = {"populate_by_name": True}


class AnswerRecord(BaseModel):
    question_id: str
    difficulty: float
    correct: bool


class UserSession(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    ability_score: float = 0.5
    questions_answered: int = 0
    correct_answers: int = 0
    history: list[AnswerRecord] = []

    model_config = {"populate_by_name": True}


class SubmitAnswerRequest(BaseModel):
    session_id: str
    question_id: str
    answer: str


class QuestionOut(BaseModel):
    """Question response without the correct answer exposed."""
    id: str = Field(alias="_id")
    question: str
    options: list[str]
    difficulty: float
    topic: str
    tags: list[str] = []

    model_config = {"populate_by_name": True}


class StudyPlanResponse(BaseModel):
    session_id: str
    accuracy: float
    max_difficulty: float
    weak_topics: list[str]
    study_plan: str

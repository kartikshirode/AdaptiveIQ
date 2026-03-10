import random

def update_ability(current: float, correct: bool) -> float:
    """Update ability score based on whether the answer was correct."""
    if correct:
        current += 0.07
    else:
        current -= 0.07
    return max(0.1, min(1.0, round(current, 4)))


async def select_next_question(ability: float, answered_ids: list[str], questions_collection):
    """Select a random unanswered question near current ability, with preference for closer difficulty."""
    cursor = questions_collection.find({"_id": {"$nin": answered_ids}})
    questions = await cursor.to_list(length=None)

    if not questions:
        return None

    random.shuffle(questions)
    
    questions.sort(key=lambda q: abs(q["difficulty"] - ability))
    
    top_candidates = questions[:min(5, len(questions))]
    
    selected = random.choice(top_candidates)
    return selected

import random

def update_ability(current: float, correct: bool) -> float:
    """Update ability score based on whether the answer was correct."""
    if correct:
        current += 0.07
    else:
        current -= 0.07
    return max(0.1, min(1.0, round(current, 4)))


async def select_next_question(ability: float, answered_ids: list[str], questions_collection):
    """Select a random unanswered question near current ability, with preference for closer difficulty.
    
    Uses efficient MongoDB query with projection to minimize data transfer.
    """
    # Use projection to only fetch needed fields (reduces data transfer)
    cursor = questions_collection.find(
        {"_id": {"$nin": answered_ids}},
        {"_id": 1, "question": 1, "options": 1, "difficulty": 1, "topic": 1, "tags": 1}
    )
    questions = await cursor.to_list(length=None)

    if not questions:
        return None

    # Shuffle for randomness first
    random.shuffle(questions)
    
    # Sort by difficulty proximity to current ability
    questions.sort(key=lambda q: abs(q["difficulty"] - ability))
    
    # Select from top 5 closest questions
    top_candidates = questions[:min(5, len(questions))]
    
    selected = random.choice(top_candidates)
    return selected

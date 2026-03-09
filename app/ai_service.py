import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))


async def generate_study_plan(
    weak_topics: list[str],
    accuracy: float,
    max_difficulty: float,
) -> str:
    """Call Google Gemini to generate a personalized GRE study plan."""
    topics_str = ", ".join(weak_topics) if weak_topics else "general topics"

    prompt = (
        f"Generate a concise 3-step GRE study plan for a student weak in {topics_str}. "
        f"Student accuracy is {accuracy:.0f}%. "
        f"Maximum difficulty reached is {max_difficulty:.2f} (on a 0–1 scale). "
        "Return only the numbered steps, each on its own line."
    )

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        return f"Error generating study plan: {str(e)}"

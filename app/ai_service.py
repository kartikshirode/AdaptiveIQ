import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()


async def generate_study_plan(
    weak_topics: list[str],
    accuracy: float,
    max_difficulty: float,
) -> str:
    """Call NVIDIA Kimi K2 model to generate a personalized GRE study plan."""
    topics_str = ", ".join(weak_topics) if weak_topics else "general topics"

    prompt = (
        f"Generate a concise 3-step GRE study plan for a student weak in {topics_str}. "
        f"Student accuracy is {accuracy:.0f}%. "
        f"Maximum difficulty reached is {max_difficulty:.2f} (on a 0–1 scale). "
        "Return only the numbered steps, each on its own line. Keep it brief and actionable."
    )

    try:
        client = AsyncOpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv("NVIDIA_API_KEY", ""),
        )

        response = await client.chat.completions.create(
            model="moonshotai/kimi-k2-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful GRE test preparation assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip() if response.choices[0].message.content else "Study plan unavailable"
    except Exception as e:
        return f"Error generating study plan: {str(e)}"

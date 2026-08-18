import os
import json

from dotenv import load_dotenv
from google import genai

from scoring import calculate_score, rank_reels


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)


def recommend_reel(interest_profile, tech_reels):

    candidates = json.dumps(tech_reels, indent=2)

    prompt = f"""
You are an AI technology Reel recommendation agent.

Student interest profile:

{json.dumps(interest_profile, indent=2)}

Available technology Reels:

{candidates}

For EVERY Reel, evaluate:

1. relevance
2. difficulty_match

Use values between 0 and 1.

Relevance means how strongly the Reel connects
to the student's broader underlying interests.

Difficulty match means how suitable the difficulty
is for the student.

Do NOT recommend based only on keywords.

Avoid hype-driven career claims.

Return ONLY valid JSON:

{{
    "evaluations": [
        {{
            "id": "",
            "relevance": 0.0,
            "difficulty_match": 0.0
        }}
    ]
}}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    result = json.loads(text)

    evaluations = result["evaluations"]

    scored_reels = []

    for reel in tech_reels:

        evaluation = next(
            (
                item
                for item in evaluations
                if item["id"] == reel["id"]
            ),
            None
        )

        if evaluation is None:
            continue

        score = calculate_score(
            evaluation["relevance"],
            reel["educational_value"],
            evaluation["difficulty_match"],
            reel["hype_score"]
        )

        scored_reels.append({
            **reel,
            "relevance": evaluation["relevance"],
            "difficulty_match": evaluation["difficulty_match"],
            "score": score
        })

    ranked = rank_reels(scored_reels)

    if not ranked:
        raise ValueError("No reels were successfully scored")

    best = ranked[0]

    return {
        "recommended_reel_id": best["id"],
        "recommended_title": best["title"],
        "category": best["category"],
        "why_recommended": (
            "This Reel has the strongest combination of "
            "interest relevance, educational value, "
            "difficulty suitability, and low hype."
        ),
        "difficulty": best["difficulty"],
        "confidence": (
            "High" if best["score"] >= 75
            else "Medium" if best["score"] >= 50
            else "Low"
        ),
        "score": best["score"],
        "ranking": ranked
    }
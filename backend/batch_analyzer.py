import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def analyze_reels_batch(reels):

    reels_text = []

    for index, reel in enumerate(reels, start=1):

        reels_text.append(f"""
REEL {index}

ID:
{reel.get("id", "")}

TITLE:
{reel.get("title", "")}

CAPTION:
{reel.get("caption", "")}

TRANSCRIPT:
{reel.get("transcript", "")}

VISUAL DESCRIPTION:
{reel.get("visual_description", "")}
""")

    prompt = f"""
You are an AI recommendation agent for college students.

Analyze ALL the Reels below in ONE request.

Your goal is to understand the student's broader interests.

IMPORTANT:

Do NOT rely only on keywords.

For example:

Java meme
+ coding interview joke
+ software engineer lifestyle
+ laptop comparison

should NOT simply produce:

"Java"

Instead, infer a broader interest such as:

"Software Engineering and Technology"

Consider:

- topic
- context
- concepts
- relationship between concepts
- programming culture
- career intent
- technology interests

Analyze every Reel separately.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "analyses": [
        {{
            "id": "",
            "main_topic": "",
            "subtopics": [],
            "context": "",
            "apparent_interest": "",
            "difficulty": "",
            "confidence": "",
            "reason": ""
        }}
    ],

    "overall_interest": {{
        "primary_interest": "",
        "secondary_interests": [],
        "evidence": [],
        "confidence": ""
    }}
}}

Difficulty must be one of:

Beginner
Intermediate
Advanced

Confidence must be one of:

High
Medium
Low

Here are the Reels:

{''.join(reels_text)}
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

    return json.loads(text)
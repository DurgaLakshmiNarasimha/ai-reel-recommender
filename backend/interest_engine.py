import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)


def infer_interest(analyzed_reels):

    reels_text = json.dumps(analyzed_reels, indent=2)

    prompt = f"""
You are an intelligent student-interest inference engine.

Analyze the student's Reel interaction history.

Your goal is NOT to find repeated keywords.

Instead, infer the student's broader underlying
technology/career interest from the combination of Reels.

For example:

Java meme
+ coding interview joke
+ software engineer lifestyle
+ laptop comparison

should NOT produce:

"Java"

Instead, infer something broader such as:

"Software Engineering and Technology"

Consider:

1. Repeated concepts
2. Related concepts
3. Career intent
4. Technical intent
5. Technology domain
6. Context
7. Relationship between different topics

Here are the analyzed Reels:

{reels_text}

Return ONLY valid JSON:

{{
    "primary_interest": "",
    "secondary_interests": [],
    "interest_summary": "",
    "evidence": [],
    "confidence": ""
}}

Confidence must be:

High
Medium
Low
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
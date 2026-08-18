import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def analyze_reel(reel):

    prompt = f"""
You are an AI recommendation agent for college students.

Your task is to understand what a Reel is REALLY about
and infer the broader underlying interest of the student.

Do NOT rely only on keywords.

Consider:
- title
- caption
- transcript
- visual description
- context
- relationship between concepts

A Reel mentioning Java does NOT automatically mean the
student only wants Java content.

For example:

Java meme
+ coding interview joke
+ software engineer lifestyle
+ laptop comparison

may indicate a broader interest in Software Engineering
and Technology.

Analyze the following Reel:

TITLE:
{reel.get("title", "")}

CAPTION:
{reel.get("caption", "")}

TRANSCRIPT:
{reel.get("transcript", "")}

VISUAL DESCRIPTION:
{reel.get("visual_description", "")}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "main_topic": "",
    "subtopics": [],
    "context": "",
    "apparent_interest": "",
    "difficulty": "",
    "confidence": "",
    "reason": ""
}}

Difficulty must be one of:

Beginner
Intermediate
Advanced

Confidence must be one of:

High
Medium
Low
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown code fences if Gemini returns them
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)
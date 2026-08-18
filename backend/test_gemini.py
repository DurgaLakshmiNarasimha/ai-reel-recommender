import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(
    api_key=api_key
)

try:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Say exactly: Gemini connection successful."
    )

    print("\nGEMINI RESPONSE:")
    print(response.text)

except Exception as e:
    print("\nGEMINI ERROR:")
    print(type(e).__name__)
    print(e)
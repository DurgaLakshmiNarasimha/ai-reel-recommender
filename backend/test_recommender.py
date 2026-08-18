import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from recommender import recommend_reel


with open(
    "backend/data/tech_reels.json",
    "r",
    encoding="utf-8"
) as file:
    tech_reels = json.load(file)


# Temporary interest profile
# This represents the interest profile Gemini already detected.
interest_profile = {
    "primary_interest": "Software Engineering and Technology",
    "secondary_interests": [
        "Programming",
        "DSA",
        "Software Development",
        "Technology"
    ],
    "interest_summary": (
        "The student shows a broad interest in software "
        "engineering, programming and technology."
    ),
    "evidence": [
        "Java developer meme",
        "Coding interview joke",
        "Software engineer lifestyle",
        "Laptop comparison"
    ],
    "confidence": "High"
}


recommendation = recommend_reel(
    interest_profile,
    tech_reels
)


print("\n" + "=" * 60)
print("FINAL AI RECOMMENDATION")
print("=" * 60)

print("\nINTEREST DETECTED:")
print(interest_profile["primary_interest"])

print("\nRECOMMENDED TECH REEL:")
print(recommendation["recommended_title"])

print("\nCATEGORY:")
print(recommendation["category"])

print("\nWHY THIS RECOMMENDATION:")
print(recommendation["why_recommended"])

print("\nDIFFICULTY:")
print(recommendation["difficulty"])

print("\nCONFIDENCE:")
print(recommendation["confidence"])

print("\nSCORE:")
print(recommendation["score"])
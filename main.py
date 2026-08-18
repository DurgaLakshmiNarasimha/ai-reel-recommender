import json
import sys
import os

# Allow Python to import files from backend
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "backend"
    )
)

from ai_analyzer import analyze_reel
from interest_engine import infer_interest
from recommender import recommend_reel
from final_output import display_recommendation


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

with open(
    "backend/data/input_reels.json",
    "r",
    encoding="utf-8"
) as file:
    input_reels = json.load(file)


with open(
    "backend/data/tech_reels.json",
    "r",
    encoding="utf-8"
) as file:
    tech_reels = json.load(file)


print("\n" + "=" * 70)
print("        AI REEL RECOMMENDATION AGENT")
print("=" * 70)

print("\nInput Reels:", len(input_reels))
print("Tech Reels:", len(tech_reels))


# --------------------------------------------------
# STEP 1: ANALYZE REELS
# --------------------------------------------------

print("\n[1/3] Analyzing student Reels...")

analyzed_reels = []

for reel in input_reels:

    print("Analyzing:", reel["title"])

    analysis = analyze_reel(reel)

    analyzed_reels.append({
        "title": reel["title"],
        "analysis": analysis
    })


# --------------------------------------------------
# STEP 2: INFER OVERALL INTEREST
# --------------------------------------------------

print("\n[2/3] Inferring overall student interest...")

interest_profile = infer_interest(
    analyzed_reels
)


print("\nPrimary Interest:")
print(interest_profile["primary_interest"])

print("\nConfidence:")
print(interest_profile["confidence"])


# --------------------------------------------------
# STEP 3: RECOMMEND TECH REEL
# --------------------------------------------------

print("\n[3/3] Ranking technology Reels...")

recommendation = recommend_reel(
    interest_profile,
    tech_reels
)


# --------------------------------------------------
# FINAL OUTPUT
# --------------------------------------------------

display_recommendation(
    input_reels[-1],
    interest_profile,
    recommendation
)
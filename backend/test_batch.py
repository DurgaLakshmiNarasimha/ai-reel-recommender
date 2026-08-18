import json
import sys
import os

sys.path.append(
    os.path.dirname(os.path.abspath(__file__))
)

from batch_analyzer import analyze_reels_batch


with open(
    "backend/data/input_reels.json",
    "r",
    encoding="utf-8"
) as file:
    reels = json.load(file)


print("=" * 60)
print("BATCH ANALYSIS TEST")
print("=" * 60)

print("\nNumber of reels:", len(reels))

print("\nCalling Gemini ONE TIME...")

result = analyze_reels_batch(reels)

print("\nBATCH ANALYSIS SUCCESSFUL")

print("\nOVERALL INTEREST:")
print(result["overall_interest"]["primary_interest"])

print("\nCONFIDENCE:")
print(result["overall_interest"]["confidence"])

print("\nREEL ANALYSES:")

for analysis in result["analyses"]:

    print("\n" + "-" * 50)

    print("ID:", analysis["id"])
    print("Topic:", analysis["main_topic"])
    print("Interest:", analysis["apparent_interest"])
    print("Difficulty:", analysis["difficulty"])
    print("Confidence:", analysis["confidence"])
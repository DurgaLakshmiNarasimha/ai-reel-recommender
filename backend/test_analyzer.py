import json

from ai_analyzer import analyze_reel


with open("backend/data/input_reels.json", "r", encoding="utf-8") as file:
    reels = json.load(file)


for reel in reels:

    result = analyze_reel(reel)

    print("\n" + "=" * 60)

    print("CURRENT REEL:")
    print(reel["title"])

    print("\nINTEREST DETECTED:")
    print(result["apparent_interest"])

    print("\nMAIN TOPIC:")
    print(result["main_topic"])

    print("\nSUBTOPICS:")
    print(result["subtopics"])

    print("\nCONTEXT:")
    print(result["context"])

    print("\nDIFFICULTY:")
    print(result["difficulty"])

    print("\nCONFIDENCE:")
    print(result["confidence"])

    print("\nWHY:")
    print(result["reason"])
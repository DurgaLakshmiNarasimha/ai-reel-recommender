def display_recommendation(
    current_reel,
    interest_profile,
    recommendation
):

    print("\n")
    print("=" * 70)
    print("              AI REEL RECOMMENDATION")
    print("=" * 70)

    print("\nCURRENT REEL:")
    print(current_reel["title"])

    print("\nINTEREST DETECTED:")
    print(interest_profile["primary_interest"])

    print("\nWHY:")
    for evidence in interest_profile["evidence"]:
        print("-", evidence)

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

    print("\nRECOMMENDATION SCORE:")
    print(recommendation["score"])

    print("\n" + "=" * 70)
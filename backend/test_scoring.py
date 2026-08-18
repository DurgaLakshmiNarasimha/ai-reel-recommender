from scoring import calculate_score, rank_reels


reels = [
    {
        "id": "tech_01",
        "title": "DSA Patterns Every Software Engineer Should Know",
        "relevance": 0.95,
        "educational_value": 0.95,
        "difficulty_match": 0.90,
        "hype_score": 0.05
    },
    {
        "id": "tech_07",
        "title": "10 AI Tools That Will Definitely Get You a Job",
        "relevance": 0.70,
        "educational_value": 0.30,
        "difficulty_match": 0.90,
        "hype_score": 0.95
    }
]


for reel in reels:

    reel["score"] = calculate_score(
        reel["relevance"],
        reel["educational_value"],
        reel["difficulty_match"],
        reel["hype_score"]
    )


ranked = rank_reels(reels)


print("\n" + "=" * 60)
print("RECOMMENDATION RANKING")
print("=" * 60)


for index, reel in enumerate(ranked, start=1):

    print(f"\nRank {index}")
    print("Title:", reel["title"])
    print("Score:", reel["score"])
    print("Hype:", reel["hype_score"])
    print("Educational:", reel["educational_value"])
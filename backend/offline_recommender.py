import json
import sys
import os

sys.path.append(
    os.path.dirname(os.path.abspath(__file__))
)

from scoring import calculate_score, rank_reels


# --------------------------------------------------
# LOAD JSON
# --------------------------------------------------

def load_json(filename):

    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    path = os.path.join(
        base_dir,
        "data",
        filename
    )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# --------------------------------------------------
# LOAD ALL REELS
# --------------------------------------------------

def load_all_reels():

    static_reels = load_json(
        "tech_reels.json"
    )

    dynamic_reels = load_json(
        "dynamic_reels.json"
    )

    # Combine both datasets
    all_reels = (
        static_reels
        + dynamic_reels
    )

    return all_reels


# --------------------------------------------------
# CALCULATE RELEVANCE
# --------------------------------------------------

def calculate_relevance(reel, interest):

    category = reel.get(
        "category",
        ""
    ).lower()

    software_categories = [
        "dsa",
        "java",
        "career",
        "hld",
        "cloud",
        "hardware",
        "python"
    ]

    if "software engineering" in interest:

        if category in software_categories:
            return 0.95

        if category == "ai":
            return 0.85

    if "artificial intelligence" in interest:

        if category == "ai":
            return 0.98

    return 0.50


# --------------------------------------------------
# CALCULATE DIFFICULTY MATCH
# --------------------------------------------------

def calculate_difficulty_match(
    reel_difficulty,
    user_difficulty="Intermediate"
):

    reel_difficulty = str(
        reel_difficulty
    ).lower()

    user_difficulty = str(
        user_difficulty
    ).lower()

    if reel_difficulty == user_difficulty:
        return 1.00

    if (
        reel_difficulty == "beginner"
        and user_difficulty == "intermediate"
    ):
        return 0.80

    if (
        reel_difficulty == "intermediate"
        and user_difficulty == "beginner"
    ):
        return 0.75

    if (
        reel_difficulty == "intermediate"
        and user_difficulty == "advanced"
    ):
        return 0.80

    if (
        reel_difficulty == "advanced"
        and user_difficulty == "intermediate"
    ):
        return 0.80

    if (
        reel_difficulty == "beginner"
        and user_difficulty == "advanced"
    ):
        return 0.55

    if (
        reel_difficulty == "advanced"
        and user_difficulty == "beginner"
    ):
        return 0.55

    return 0.70


# --------------------------------------------------
# MAIN RECOMMENDATION FUNCTION
# --------------------------------------------------

def generate_offline_recommendation():

    # Load AI analysis
    analysis_data = load_json(
        "analysis_result.json"
    )

    # Load static + dynamic reels
    tech_reels = load_all_reels()

    # Get user interest
    interest_profile = analysis_data[
        "overall_interest"
    ]

    interest = interest_profile[
        "primary_interest"
    ].lower()

    user_difficulty = "Intermediate"

    scored_reels = []

    # --------------------------------------------------
    # SCORE EVERY REEL
    # --------------------------------------------------

    for reel in tech_reels:

        relevance = calculate_relevance(
            reel,
            interest
        )

        difficulty_match = calculate_difficulty_match(
            reel.get(
                "difficulty",
                "Intermediate"
            ),
            user_difficulty
        )

        educational_value = float(
            reel.get(
                "educational_value",
                0.50
            )
        )

        hype_score = float(
            reel.get(
                "hype_score",
                0.00
            )
        )

        score = calculate_score(
            relevance,
            educational_value,
            difficulty_match,
            hype_score
        )

        scored_reels.append({

            **reel,

            "relevance":
                relevance,

            "difficulty_match":
                difficulty_match,

            "score":
                score
        })

    # --------------------------------------------------
    # RANK ALL REELS
    # --------------------------------------------------

    ranked = rank_reels(
        scored_reels
    )

    # --------------------------------------------------
    # API RESULT
    # --------------------------------------------------

    result = {

        "status":
            "success",

        "total_reels":
            len(ranked),

        "interest_detected":
            interest_profile[
                "primary_interest"
            ],

        "confidence":
            interest_profile[
                "confidence"
            ],

        "recommended_reel": {

            "id":
                ranked[0]["id"],

            "title":
                ranked[0]["title"],

            "description":
                ranked[0].get(
                    "description",
                    ""
                ),

            "category":
                ranked[0]["category"],

            "difficulty":
                ranked[0]["difficulty"],

            "educational_value":
                ranked[0].get(
                    "educational_value",
                    0
                ),

            "hype_score":
                ranked[0].get(
                    "hype_score",
                    0
                ),

            "score":
                ranked[0]["score"],

            "source":
                ranked[0].get(
                    "source",
                    "Static Dataset"
                ),

            "url":
                ranked[0].get(
                    "url",
                    ""
                )
        },

        "ranking": [

            {

                "rank":
                    index,

                "id":
                    reel["id"],

                "title":
                    reel["title"],

                "category":
                    reel["category"],

                "difficulty":
                    reel["difficulty"],

                "score":
                    reel["score"],

                "hype_score":
                    reel.get(
                        "hype_score",
                        0
                    ),

                "educational_value":
                    reel.get(
                        "educational_value",
                        0
                    ),

                "source":
                    reel.get(
                        "source",
                        "Static Dataset"
                    )

            }

            for index, reel
            in enumerate(
                ranked,
                start=1
            )
        ]
    }

    return result


# --------------------------------------------------
# TERMINAL TEST
# --------------------------------------------------

if __name__ == "__main__":

    result = generate_offline_recommendation()

    print(
        "\n" + "=" * 60
    )

    print(
        "DYNAMIC AI REEL RECOMMENDATION"
    )

    print(
        "=" * 60
    )

    print(
        "\nTotal Reels:",
        result["total_reels"]
    )

    print(
        "Interest:",
        result["interest_detected"]
    )

    print(
        "Confidence:",
        result["confidence"]
    )

    print(
        "\nRecommended Reel:"
    )

    print(
        result[
            "recommended_reel"
        ]["title"]
    )

    print(
        "Category:",
        result[
            "recommended_reel"
        ]["category"]
    )

    print(
        "Difficulty:",
        result[
            "recommended_reel"
        ]["difficulty"]
    )

    print(
        "Score:",
        result[
            "recommended_reel"
        ]["score"]
    )

    print(
        "Source:",
        result[
            "recommended_reel"
        ]["source"]
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "RANKING"
    )

    print(
        "=" * 60
    )

    for reel in result["ranking"]:

        print(
            f'{reel["rank"]}. '
            f'{reel["title"]} '
            f'| Score: {reel["score"]} '
            f'| Source: {reel["source"]}'
        )
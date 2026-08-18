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

    return static_reels + dynamic_reels


# --------------------------------------------------
# LOAD USER BEHAVIOR PROFILE
# --------------------------------------------------

def load_user_behavior_profile():

    try:

        from user_interest import UserInterestProfile

        profile = UserInterestProfile()

        return profile.get_profile()

    except Exception as e:

        print(
            "User behavior profile error:",
            e
        )

        return {}


# --------------------------------------------------
# CALCULATE BASE RELEVANCE
# --------------------------------------------------

def calculate_relevance(
    reel,
    interest
):

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
# CALCULATE BEHAVIOR MATCH
# --------------------------------------------------

def calculate_behavior_match(
    reel,
    user_interest_profile
):

    if not user_interest_profile:
        return 0.0

    scores = user_interest_profile.get(
        "scores",
        {}
    )

    category = str(
        reel.get(
            "category",
            ""
        )
    ).lower()

    behavior_score = float(
        scores.get(
            category,
            0
        )
    )

    return min(
        behavior_score / 100.0,
        1.0
    )


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

def generate_offline_recommendation(
    user_interest_profile=None
):

    # --------------------------------------------------
    # LOAD AI ANALYSIS
    # --------------------------------------------------

    analysis_data = load_json(
        "analysis_result.json"
    )

    # --------------------------------------------------
    # LOAD ALL REELS
    # --------------------------------------------------

    tech_reels = load_all_reels()

    # --------------------------------------------------
    # LOAD USER BEHAVIOR AUTOMATICALLY
    # --------------------------------------------------

    if user_interest_profile is None:

        user_interest_profile = (
            load_user_behavior_profile()
        )

    # --------------------------------------------------
    # GET INITIAL AI INTEREST
    # --------------------------------------------------

    interest_profile = analysis_data[
        "overall_interest"
    ]

    interest = interest_profile[
        "primary_interest"
    ].lower()

    # --------------------------------------------------
    # IF USER HAS BEHAVIOR DATA,
    # USE IT TO IMPROVE INTEREST
    # --------------------------------------------------

    behavior_primary_interest = (
        user_interest_profile.get(
            "primary_interest",
            ""
        )
        if user_interest_profile
        else ""
    )

    if behavior_primary_interest:

        interest = (
            behavior_primary_interest.lower()
        )

    user_difficulty = "Intermediate"

    scored_reels = []

    # --------------------------------------------------
    # SCORE EVERY REEL
    # --------------------------------------------------

    for reel in tech_reels:

        # ----------------------------------------------
        # AI / CONTENT RELEVANCE
        # ----------------------------------------------

        relevance = calculate_relevance(
            reel,
            interest
        )

        # ----------------------------------------------
        # DIFFICULTY
        # ----------------------------------------------

        difficulty_match = (
            calculate_difficulty_match(
                reel.get(
                    "difficulty",
                    "Intermediate"
                ),
                user_difficulty
            )
        )

        # ----------------------------------------------
        # EDUCATIONAL VALUE
        # ----------------------------------------------

        educational_value = float(
            reel.get(
                "educational_value",
                0.50
            )
        )

        # ----------------------------------------------
        # HYPE SCORE
        # ----------------------------------------------

        hype_score = float(
            reel.get(
                "hype_score",
                0.00
            )
        )

        # ----------------------------------------------
        # USER BEHAVIOR MATCH
        # ----------------------------------------------

        behavior_match = (
            calculate_behavior_match(
                reel,
                user_interest_profile
            )
        )

        # ----------------------------------------------
        # ORIGINAL SCORE
        # ----------------------------------------------

        base_score = calculate_score(
            relevance,
            educational_value,
            difficulty_match,
            hype_score
        )

        # ----------------------------------------------
        # BEHAVIOR BONUS
        # ----------------------------------------------

        behavior_bonus = (
            behavior_match * 15
        )

        # ----------------------------------------------
        # FINAL SCORE
        # ----------------------------------------------

        final_score = min(
            base_score + behavior_bonus,
            100
        )

        # ----------------------------------------------
        # STORE RESULT
        # ----------------------------------------------

        scored_reels.append({

            **reel,

            "relevance":
                round(
                    relevance,
                    2
                ),

            "difficulty_match":
                round(
                    difficulty_match,
                    2
                ),

            "behavior_match":
                round(
                    behavior_match,
                    2
                ),

            "behavior_bonus":
                round(
                    behavior_bonus,
                    2
                ),

            "score":
                round(
                    final_score,
                    2
                )
        })

    # --------------------------------------------------
    # RANK ALL REELS
    # --------------------------------------------------

    ranked = rank_reels(
        scored_reels
    )

    # --------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------

    if not ranked:

        return {
            "status": "error",
            "message": "No reels available"
        }

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

        "behavior_interest":
            user_interest_profile.get(
                "primary_interest",
                "None"
            ),

        "confidence":
            interest_profile[
                "confidence"
            ],

        "user_behavior_profile":
            user_interest_profile
            or {},

        # ----------------------------------------------
        # TOP RECOMMENDATION
        # ----------------------------------------------

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

            "relevance":
                ranked[0].get(
                    "relevance",
                    0
                ),

            "behavior_match":
                ranked[0].get(
                    "behavior_match",
                    0
                ),

            "behavior_bonus":
                ranked[0].get(
                    "behavior_bonus",
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

        # ----------------------------------------------
        # COMPLETE RANKING
        # ----------------------------------------------

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

                "relevance":
                    reel.get(
                        "relevance",
                        0
                    ),

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

                "behavior_match":
                    reel.get(
                        "behavior_match",
                        0
                    ),

                "behavior_bonus":
                    reel.get(
                        "behavior_bonus",
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

    result = (
        generate_offline_recommendation()
    )

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
        "AI Interest:",
        result["interest_detected"]
    )

    print(
        "Behavior Interest:",
        result["behavior_interest"]
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
        "Behavior Match:",
        result[
            "recommended_reel"
        ]["behavior_match"]
    )

    print(
        "Behavior Bonus:",
        result[
            "recommended_reel"
        ]["behavior_bonus"]
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
            f'| Behavior Bonus: '
            f'{reel["behavior_bonus"]} '
            f'| Source: {reel["source"]}'
        )
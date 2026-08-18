def calculate_score(
    relevance,
    educational_value,
    difficulty_match,
    hype_score
):
    """
    Calculate final recommendation score.

    Higher relevance       -> better
    Higher educational     -> better
    Better difficulty      -> better
    Higher hype            -> worse
    """

    score = (
        relevance * 40
        + educational_value * 30
        + difficulty_match * 20
        - hype_score * 10
    )

    return round(score, 2)


def rank_reels(scored_reels):
    """
    Sort reels from highest score to lowest score.
    """

    return sorted(
        scored_reels,
        key=lambda reel: reel["score"],
        reverse=True
    )
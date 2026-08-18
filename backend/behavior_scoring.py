# --------------------------------------------------
# USER BEHAVIOR SCORING
# --------------------------------------------------

def calculate_behavior_score(
    watch_time,
    duration,
    liked=False,
    rewatched=False,
    skipped=False
):
    """
    Calculate how strongly a user interacted
    with a reel.
    """

    duration = max(
        float(duration),
        1.0
    )

    watch_time = max(
        float(watch_time),
        0.0
    )

    # ----------------------------------------------
    # WATCH COMPLETION
    # ----------------------------------------------

    completion = min(
        watch_time / duration,
        1.0
    )

    watch_score = (
        completion * 50
    )

    # ----------------------------------------------
    # LIKE
    # ----------------------------------------------

    like_score = 30 if liked else 0

    # ----------------------------------------------
    # REWATCH
    # ----------------------------------------------

    rewatch_score = (
        15 if rewatched else 0
    )

    # ----------------------------------------------
    # SKIP PENALTY
    # ----------------------------------------------

    skip_penalty = (
        20 if skipped else 0
    )

    # ----------------------------------------------
    # FINAL SCORE
    # ----------------------------------------------

    final_score = (
        watch_score
        + like_score
        + rewatch_score
        - skip_penalty
    )

    final_score = max(
        0,
        min(
            final_score,
            100
        )
    )

    return {
        "watch_time": round(
            watch_time,
            2
        ),

        "duration": round(
            duration,
            2
        ),

        "completion_percentage": round(
            completion * 100,
            2
        ),

        "liked": liked,

        "rewatched": rewatched,

        "skipped": skipped,

        "behavior_score": round(
            final_score,
            2
        )
    }
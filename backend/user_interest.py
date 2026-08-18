from collections import defaultdict


class UserInterestProfile:

    def __init__(self):
        self.category_scores = defaultdict(float)

    def record_behavior(
        self,
        category,
        behavior_score
    ):
        category = str(
            category
        ).strip().lower()

        self.category_scores[
            category
        ] += float(
            behavior_score
        )

    def get_profile(self):

        if not self.category_scores:
            return {
                "primary_interest": None,
                "scores": {}
            }

        primary_interest = max(
            self.category_scores,
            key=self.category_scores.get
        )

        return {
            "primary_interest":
                primary_interest,

            "scores": dict(
                self.category_scores
            )
        }
import json
import os
from collections import defaultdict


# --------------------------------------------------
# PROFILE STORAGE
# --------------------------------------------------

PROFILE_FILE = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)
    ),
    "user_profile.json"
)


class UserInterestProfile:

    def __init__(self):

        self.category_scores = defaultdict(
            float
        )

        self.load_profile()


    # --------------------------------------------------
    # LOAD SAVED PROFILE
    # --------------------------------------------------

    def load_profile(self):

        if not os.path.exists(
            PROFILE_FILE
        ):
            return

        try:

            with open(
                PROFILE_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            scores = data.get(
                "scores",
                {}
            )

            for category, score in scores.items():

                self.category_scores[
                    category
                ] = float(score)

        except Exception as e:

            print(
                "Profile load error:",
                e
            )


    # --------------------------------------------------
    # SAVE PROFILE
    # --------------------------------------------------

    def save_profile(self):

        profile = self.get_profile()

        with open(
            PROFILE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                profile,
                file,
                indent=4
            )


    # --------------------------------------------------
    # RECORD USER BEHAVIOR
    # --------------------------------------------------

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

        # Save immediately
        self.save_profile()


    # --------------------------------------------------
    # GET USER PROFILE
    # --------------------------------------------------

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

            "scores":
                dict(
                    self.category_scores
                )
        }
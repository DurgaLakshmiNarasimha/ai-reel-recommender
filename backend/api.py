from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os


# --------------------------------------------------
# ALLOW IMPORTS FROM BACKEND FOLDER
# --------------------------------------------------

sys.path.append(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


from offline_recommender import (
    generate_offline_recommendation
)

from behavior_scoring import (
    calculate_behavior_score
)

from user_interest import (
    UserInterestProfile
)


# --------------------------------------------------
# CREATE FLASK APP
# --------------------------------------------------

app = Flask(__name__)

CORS(app)


# --------------------------------------------------
# USER INTEREST PROFILE
# --------------------------------------------------

user_profile = UserInterestProfile()


# --------------------------------------------------
# API: HEALTH CHECK
# --------------------------------------------------

@app.route(
    "/api/health",
    methods=["GET"]
)
def health():

    return jsonify({

        "status":
            "success",

        "message":
            "AI Reel Recommendation API is running"

    })


# --------------------------------------------------
# API: RECOMMENDATION
# --------------------------------------------------

@app.route(
    "/api/recommendation",
    methods=["GET"]
)
def recommendation():

    try:

        # Get current user behavior profile
        profile = user_profile.get_profile()

        # Generate recommendation using
        # AI interest + user behavior
        result = generate_offline_recommendation(
            user_interest_profile=profile
        )

        return jsonify(result)

    except Exception as e:

        return jsonify({

            "status":
                "error",

            "message":
                str(e)

        }), 500


# --------------------------------------------------
# API: RECORD REEL BEHAVIOR
# --------------------------------------------------

@app.route(
    "/api/behavior",
    methods=["POST"]
)
def record_behavior():

    try:

        data = request.get_json()

        if not data:

            return jsonify({

                "status":
                    "error",

                "message":
                    "No behavior data received"

            }), 400


        # --------------------------------------------------
        # GET BEHAVIOR DATA
        # --------------------------------------------------

        category = data.get(
            "category",
            "unknown"
        )

        watch_time = float(
            data.get(
                "watch_time",
                0
            )
        )

        duration = float(
            data.get(
                "duration",
                30
            )
        )

        liked = bool(
            data.get(
                "liked",
                False
            )
        )

        rewatched = bool(
            data.get(
                "rewatched",
                False
            )
        )

        skipped = bool(
            data.get(
                "skipped",
                False
            )
        )


        # --------------------------------------------------
        # CALCULATE BEHAVIOR SCORE
        # --------------------------------------------------

        behavior = calculate_behavior_score(

            watch_time,

            duration,

            liked,

            rewatched,

            skipped

        )


        behavior_score = behavior[
            "behavior_score"
        ]


        # --------------------------------------------------
        # UPDATE USER INTEREST
        # --------------------------------------------------

        user_profile.record_behavior(

            category,

            behavior_score

        )


        # Get updated profile

        profile = user_profile.get_profile()


        # --------------------------------------------------
        # RETURN RESULT
        # --------------------------------------------------

        return jsonify({

            "status":
                "success",

            "message":
                "User behavior recorded",

            "behavior":
                behavior,

            "user_interest":
                profile

        })


    except Exception as e:

        return jsonify({

            "status":
                "error",

            "message":
                str(e)

        }), 500


# --------------------------------------------------
# API: USER PROFILE
# --------------------------------------------------

@app.route(
    "/api/user-profile",
    methods=["GET"]
)
def get_user_profile():

    try:

        return jsonify({

            "status":
                "success",

            "profile":
                user_profile.get_profile()

        })


    except Exception as e:

        return jsonify({

            "status":
                "error",

            "message":
                str(e)

        }), 500


# --------------------------------------------------
# ROOT ROUTE
# --------------------------------------------------

@app.route(
    "/",
    methods=["GET"]
)
def home():

    return jsonify({

        "status":
            "success",

        "message":
            "AI Reel Recommendation API is running",

        "endpoints": [

            "/api/health",

            "/api/recommendation",

            "/api/behavior",

            "/api/user-profile"

        ]

    })


# --------------------------------------------------
# START FLASK SERVER
# --------------------------------------------------

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )
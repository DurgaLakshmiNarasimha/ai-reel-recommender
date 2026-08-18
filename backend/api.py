from flask import Flask, jsonify
from flask_cors import CORS
import sys
import os

# Allow imports from backend folder
sys.path.append(
    os.path.dirname(os.path.abspath(__file__))
)

from offline_recommender import generate_offline_recommendation


# --------------------------------------------------
# CREATE FLASK APP
# --------------------------------------------------

app = Flask(__name__)

CORS(app)


# --------------------------------------------------
# API: HEALTH CHECK
# --------------------------------------------------

@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({
        "status": "success",
        "message": "AI Reel Recommendation API is running"
    })


# --------------------------------------------------
# API: RECOMMENDATION
# --------------------------------------------------

@app.route("/api/recommendation", methods=["GET"])
def recommendation():

    try:

        # Offline recommendation engine
        result = generate_offline_recommendation()

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# --------------------------------------------------
# ROOT ROUTE
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "status": "success",
        "message": "AI Reel Recommendation API is running",
        "endpoints": [
            "/api/health",
            "/api/recommendation"
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
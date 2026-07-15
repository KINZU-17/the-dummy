from flask import Blueprint, request, jsonify
from app.database.queries import create_prediction, get_predictions_for_fixture
from app.utils.auth import login_required

predictions_bp = Blueprint("predictions", __name__, url_prefix="/api/predictions")


@predictions_bp.route("", methods=["POST"])
@login_required
def create_prediction_route():
    data = request.get_json(silent=True) or {}
    fixture_id = data.get("fixture_id")
    predicted_winner_id = data.get("predicted_winner_id")
    confidence = data.get("confidence", 50)

    if not fixture_id:
        return jsonify({"error": "fixture_id is required"}), 400

    prediction_id = create_prediction(request.user_id, fixture_id, predicted_winner_id, confidence)
    return jsonify({"prediction_id": prediction_id, "confidence": confidence}), 201


@predictions_bp.route("/fixture/<int:fixture_id>", methods=["GET"])
def list_predictions_for_fixture(fixture_id: int):
    rows = get_predictions_for_fixture(fixture_id)
    return jsonify({"predictions": rows})

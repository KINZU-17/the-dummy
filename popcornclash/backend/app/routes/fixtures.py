from flask import Blueprint, request, jsonify
from app.database.queries import get_all_fixtures, get_fixture, create_fixture, update_fixture_status
from app.utils.auth import admin_required, login_required

fixtures_bp = Blueprint("fixtures", __name__, url_prefix="/api/fixtures")


@fixtures_bp.route("", methods=["GET"])
def list_fixtures():
    rows = get_all_fixtures()
    return jsonify({"fixtures": rows})


@fixtures_bp.route("/<int:fixture_id>", methods=["GET"])
def get_fixture_by_id(fixture_id: int):
    row = get_fixture(fixture_id)
    if not row:
        return jsonify({"error": "Fixture not found"}), 404
    return jsonify({"fixture": row})


@fixtures_bp.route("", methods=["POST"])
@admin_required
def create_fixture_route():
    data = request.get_json(silent=True) or {}
    team_home_id = data.get("team_home_id")
    team_away_id = data.get("team_away_id")
    match_date = data.get("match_date")
    status = data.get("status", "SCHEDULED")

    if not all([team_home_id, team_away_id, match_date]):
        return jsonify({"error": "team_home_id, team_away_id, and match_date are required"}), 400

    fixture_id = create_fixture(team_home_id, team_away_id, match_date, status)
    row = get_fixture(fixture_id)
    return jsonify({"fixture": row}), 201


@fixtures_bp.route("/<int:fixture_id>/status", methods=["PATCH"])
@admin_required
def patch_fixture_status(fixture_id: int):
    data = request.get_json(silent=True) or {}
    status = data.get("status")
    if not status:
        return jsonify({"error": "status is required"}), 400
    update_fixture_status(fixture_id, status)
    row = get_fixture(fixture_id)
    return jsonify({"fixture": row})

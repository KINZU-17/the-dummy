from flask import Blueprint, request, jsonify
from app.database.queries import get_all_teams, get_team_by_id, get_leaderboard
from app.database.connection import get_cursor

teams_bp = Blueprint("teams", __name__, url_prefix="/api/teams")


@teams_bp.route("/leaderboard", methods=["GET"])
def leaderboard():
    rows = get_leaderboard(limit=100)
    return jsonify({"leaderboard": rows})


@teams_bp.route("", methods=["GET"])
def list_teams():
    rows = get_all_teams()
    return jsonify({"teams": rows})

from functools import wraps
from flask import request, jsonify


def _current_user_id() -> int | None:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ", 1)[1]
    if not token.startswith("mock-token-"):
        return None
    try:
        return int(token.split("-")[-1])
    except ValueError:
        return None


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = _current_user_id()
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        request.user_id = user_id
        return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = _current_user_id()
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        from app.database.queries import get_user_by_id
        user = get_user_by_id(user_id)
        if not user or user.get("role") != "admin":
            return jsonify({"error": "Forbidden: admin access required"}), 403
        request.user_id = user_id
        return fn(*args, **kwargs)
    return wrapper

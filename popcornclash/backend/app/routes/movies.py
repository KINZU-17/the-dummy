from flask import Blueprint, request, jsonify
from app.database.queries import get_all_movies, get_movie_by_id, create_movie

movies_bp = Blueprint("movies", __name__, url_prefix="/api/movies")


@movies_bp.route("", methods=["GET"])
def list_movies():
    query = request.args.get("q", "")
    genre = request.args.get("genre", "")
    limit = request.args.get("limit", 50, type=int)

    movies = get_all_movies(limit=limit)

    if query:
        q = query.lower()
        movies = [m for m in movies if q in (m.get("title") or "").lower() or q in (m.get("genre") or "").lower()]
    if genre:
        movies = [m for m in movies if (m.get("genre") or "").lower() == genre.lower()]

    return jsonify({"movies": movies})


@movies_bp.route("/<int:movie_id>", methods=["GET"])
def get_movie(movie_id: int):
    movie = get_movie_by_id(movie_id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404
    return jsonify({"movie": movie})


@movies_bp.route("", methods=["POST"])
def add_movie():
    data = request.get_json(silent=True) or {}
    tmdb_id = data.get("tmdb_id")
    title = (data.get("title") or "").strip()
    overview = data.get("overview") or ""
    poster_url = data.get("poster_url") or ""
    genre = data.get("genre") or ""
    year = data.get("year")
    rating = data.get("rating")
    duration = data.get("duration") or ""

    if not title:
        return jsonify({"error": "title is required"}), 400

    movie_id = create_movie(tmdb_id, title, overview, poster_url, genre, year, rating, duration)
    movie = get_movie_by_id(movie_id)
    return jsonify({"movie": movie}), 201

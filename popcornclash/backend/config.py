import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    DATABASE_PATH = os.environ.get("POPCORNCLASH_DB_PATH", os.path.join(os.path.dirname(__file__), "popcornclash.db"))
    BACKEND_URL = os.environ.get("VITE_BACKEND_URL", "http://localhost:5000")


config = Config()

from __future__ import annotations

from src.config import CONFIG


kinopoisk_unoff_base_url = "https://kinopoiskapiunofficial.tech/api"

headers = {
    "x-api-key": CONFIG.X_API_KEY,
    "Content-Type": "application/json",
}

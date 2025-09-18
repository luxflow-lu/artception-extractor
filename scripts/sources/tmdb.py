import os, requests
API = "https://api.themoviedb.org/3"
KEY = os.environ.get("TMDB_API_KEY")

def search_movies(query, year=None, page=1):
    params = {"api_key": KEY, "query": query, "page": page}
    if year:
        params["year"] = year
    r = requests.get(f"{API}/search/movie", params=params, timeout=30)
    r.raise_for_status()
    return r.json()

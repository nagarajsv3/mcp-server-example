import requests

CHESS_API_BASE = "https://api.chess.com/pub"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_player_profile(username: str):
    url = f"{CHESS_API_BASE}/player/{username}"
    response = requests.get(url, headers)
    response.raise_for_status()  # Raises HTTPError if status code is 4xx/5xx
    return response.json()

def get_player_stats(username: str):
    """Get player statistics and ratings from Chess.com API"""
    url = f"{CHESS_API_BASE}/player/{username}/stats"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

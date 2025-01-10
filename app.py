from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import requests
from collections import Counter

app = Flask(__name__)
CORS(app)  # Enable CORS so that your React app on another port can access it

API_KEY = "9051E62B25041C579CCB4ACA0A9A9345"

def call_steam_api(endpoint, params):
    """Helper function to call the Steam API."""
    base_url = f"http://api.steampowered.com/{endpoint}"
    params["key"] = API_KEY
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return {}

# Feature 1: Fetch owned games
def get_owned_games(steam_id):
    endpoint = "IPlayerService/GetOwnedGames/v0001/"
    params = {"steamid": steam_id, "format": "json", "include_appinfo": True}
    data = call_steam_api(endpoint, params)
    return data.get("response", {}).get("games", [])

# Feature 2: Fetch friends list
def get_friends_list(steam_id):
    endpoint = "ISteamUser/GetFriendList/v0001/"
    params = {"steamid": steam_id, "relationship": "friend"}
    data = call_steam_api(endpoint, params)
    return data.get("friendslist", {}).get("friends", [])

# Feature 3: Fetch friends' games
def get_friends_games(friends_ids):
    friends_games = Counter()
    for friend in friends_ids:
        friend_games = get_owned_games(friend["steamid"])
        friends_games.update([game["name"] for game in friend_games])
    return friends_games



# Feature 4: Recommend games
def recommend_games(your_games, friends_games):
    your_game_names = {game["name"] for game in your_games}
    recommendations = [game for game, count in friends_games.items() if game not in your_game_names]
    return recommendations[:15]  # Return only the first 15 recommendations

# Feature 5: Track achievements
def get_achievements(steam_id, appid):
    endpoint = "ISteamUserStats/GetPlayerAchievements/v0001/"
    params = {"steamid": steam_id, "appid": appid, "format": "json"}
    data = call_steam_api(endpoint, params)

    # Check if the API response indicates no stats available
    if not data.get("playerstats", {}).get("success", True):
        print(f"Achievements not available for AppID: {appid}")
        return []

    return data.get("playerstats", {}).get("achievements", [])

# Feature 6: Fetch wishlist
def fetch_wishlist(steam_id):
    url = f"https://store.steampowered.com/wishlist/profiles/{steam_id}/wishlistdata/"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching wishlist for Steam ID {steam_id}")
        return []

    try:
        wishlist_data = response.json()
        wishlist_games = [wishlist_data[game]["name"] for game in wishlist_data]
        return wishlist_games
    except ValueError:
        print("Failed to parse wishlist data.")
        return []

# Feature 7: Analyze playtime and genres
def analyze_playtime_and_genres(your_games):
    total_playtime = sum(game["playtime_forever"] for game in your_games) / 60  # In hours
    top_games = sorted(your_games, key=lambda x: x["playtime_forever"], reverse=True)[:5]
    genres = Counter()

    for game in your_games:
        appid = game.get('appid')
        game_details = get_steam_app_details(appid)
        if game_details:
            game_genres = [genre['description'] for genre in game_details.get('genres', [])]
            genres.update(game_genres)
            game['genres'] = game_genres  # Add genres to the game dictionary
        else:
            game['genres'] = ['Unknown']

    return total_playtime, top_games, genres

# Implement caching and rate limiting
app_details_cache = {}

def get_steam_app_details(appid, retries=3):
    """Fetch game details from the Steam Storefront API with retry logic."""
    if appid in app_details_cache:
        return app_details_cache[appid]

    url = f"https://store.steampowered.com/api/appdetails"
    params = {'appids': appid}
    delay = 0.5  # Initial delay

    for attempt in range(retries):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get(str(appid), {}).get('success'):
                app_details = data[str(appid)]['data']
                app_details_cache[appid] = app_details
                time.sleep(0.2)  # Slight delay to be polite
                return app_details
            else:
                print(f"No data available for AppID: {appid}")
                app_details_cache[appid] = None
                time.sleep(0.2)
                return None
        elif response.status_code == 429:
            print(f"Rate limit exceeded. Attempt {attempt + 1} of {retries}. Waiting for {delay} seconds.")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
        else:
            print(f"Error {response.status_code}: {response.text}")
            time.sleep(1)
            return None
    print(f"Failed to fetch data for AppID: {appid} after {retries} retries.")
    return None

# New Feature: Identify underplayed highly-rated games
def find_underplayed_highly_rated_games(your_games, max_playtime=120):
    """
    Identify games you own that have high user ratings but low playtime.
    max_playtime: maximum playtime in minutes to consider as underplayed
    """
    underplayed_games = []
    for game in your_games:
        playtime = game.get('playtime_forever', 0)
        if playtime <= max_playtime:  # Underplayed
            appid = game.get('appid')
            game_details = get_steam_app_details(appid)
            if game_details and game_details.get('type') == 'game':
                user_rating = game_details.get('metacritic', {}).get('score')
                genres = [genre['description'] for genre in game_details.get('genres', [])]
                if user_rating and user_rating >= 75:
                    underplayed_games.append({
                        'name': game_details.get('name'),
                        'playtime_hours': playtime / 60,
                        'user_rating': user_rating,
                        'genres': genres
                    })
    return underplayed_games
# (Paste your existing functions here: call_steam_api, get_owned_games, etc.)
# For brevity, let's imagine we copy all your existing Python code.

@app.route("/api/steam-data", methods=["GET"])
def get_steam_data():
    """
    Expects a `steamid` query parameter. Example: /api/steam-data?steamid=76561198210669612
    Returns JSON containing all processed Steam data.
    """
    steam_id = request.args.get("steamid", None)
    if not steam_id:
        return jsonify({"error": "steamid is required"}), 400

    # 1. Fetch your games
    your_games = get_owned_games(steam_id)
    
    # 2. Fetch friends
    friends_ids = get_friends_list(steam_id)
    friends_games = get_friends_games(friends_ids)

    # 3. Recommendations
    recommendations = recommend_games(your_games, friends_games)
    
    # 4. Achievements for the top game (optional)
    achievements = []
    if your_games:
        top_game = your_games[0]
        achievements = get_achievements(steam_id, top_game["appid"])

    # 5. Analyze playtime/genres
    total_playtime, top_games, genres = analyze_playtime_and_genres(your_games)

    # 6. Underplayed highly-rated games
    underplayed_games = find_underplayed_highly_rated_games(your_games)

    # 7. Return the collected data as JSON
    data_to_return = {
        "your_games": your_games,
        "friends_count": len(friends_ids),
        "recommendations": recommendations,
        "top_game_achievements": achievements,
        "total_playtime_hours": total_playtime,
        "top_5_games": top_games,
        "genres_distribution": dict(genres),
        "underplayed_highly_rated_games": underplayed_games
    }
    return jsonify(data_to_return)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

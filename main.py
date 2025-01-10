import requests
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
import time
from collections import Counter

#API KEYS
API_KEY = ""
YOUR_STEAM_ID = ""

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

# Example function to fetch friends' games
def get_friends_owned_games(friends_ids):
    friends_games = []
    for friend in friends_ids:
        owned_games = get_owned_games(friend["steamid"])  # Fetch each friend's owned games
        friends_games.extend([game["name"] for game in owned_games])
    return friends_games

# New function to compute number of friends owning each recommended game
def compute_friends_ownership(recommended_games, friends_games_list):
    """
    Count how many friends own each recommended game.
    """
    # Create a counter for all games owned by friends
    friends_game_counter = Counter(friends_games_list)

    # Prepare data for the frontend
    ownership_data = []
    for game in recommended_games:
        ownership_data.append({
            "name": game,
            "friend_count": friends_game_counter[game]
        })
    return ownership_data

# Feature 4: Recommend games
def recommend_games(your_games, friends_games):
    your_game_names = {game["name"] for game in your_games}
    recommendations = [game for game, count in friends_games.items() if game not in your_game_names]
    return recommendations

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

if __name__ == "__main__":
    # Fetch games
    your_games = get_owned_games(YOUR_STEAM_ID)
    print("Your Games:")
    for game in your_games:
        print(f"- {game['name']} ({game['playtime_forever'] // 60} hours)")

    # Fetch friends' games
    friends_ids = get_friends_list(YOUR_STEAM_ID)
    friends_games = get_friends_games(friends_ids)

    # Recommend games
    recommendations = recommend_games(your_games, friends_games)
    print("\nRecommended Games (Your Friends Play, You Don't):")
    for game in recommendations[:5]:
        print(f"- {game}")

    # Achievements for top game
    if your_games:
        print("\nAchievements for Your Top Game:")
        top_game = your_games[0]
        achievements = get_achievements(YOUR_STEAM_ID, top_game["appid"])
        if achievements:
            for achievement in achievements[:5]:  
                print(f"- {achievement['apiname']}: {'Unlocked' if achievement['achieved'] else 'Locked'}")
        else:
            print("No achievements available for this game.")

    # Analyze playtime and genres
    total_playtime, top_games, genres = analyze_playtime_and_genres(your_games)
    print(f"\nTotal Playtime: {total_playtime:.2f} hours")
    print("Top 5 Games by Playtime:")
    for game in top_games:
        print(f"- {game['name']} ({game['playtime_forever'] // 60} hours)")
    print("Game Genres Distribution:")
    for genre, count in genres.items():
        print(f"- {genre}: {count} games")

    # Underplayed Highly-Rated Games
    print("\nUnderplayed Highly-Rated Games in Your Library:")
    underplayed_games = find_underplayed_highly_rated_games(your_games)
    if underplayed_games:
        for game in underplayed_games:
            print(f"- {game['name']} (Playtime: {game['playtime_hours']:.2f} hours, User Rating: {game['user_rating']}/100)")
    else:
        print("No underplayed highly-rated games found in your library.")

    # Get favorite genres
    favorite_genres = [genre for genre, _ in genres.most_common(3)]
    print("\nYour Favorite Genres:")
    for genre in favorite_genres:
        print(f"- {genre}")

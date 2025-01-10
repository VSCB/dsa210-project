# Steam Gaming Data Analysis

## Description
This project focuses on collecting and analyzing **Steam** gaming data to gain insights into personal gaming habits, identify underplayed yet highly-rated games, and generate meaningful recommendations. It encompasses two main components:

1. A **Flask** backend that utilizes the **Steam Web API** and **Steam Storefront API** to retrieve and process data (owned games, achievements, friends’ libraries, genres, Metacritic scores, etc.).
2. A **React** frontend that presents the analysis in a clear, user-friendly website, where entering a SteamID allows you to view detailed statistics, recommendations, and highlights.

For an overview of the final analysis and visualizations, see the sections below. The source code for both the Flask backend and the React frontend can be found in this repository.

Also, here is the video of me presenting the website: [Presentation Video](https://drive.google.com/file/d/1xW4myizDI-6MHmYOkinx6D8253V0CsdE/view?usp=sharing)

---

## Table of Contents
- [Motivation](#motivation)
- [Tools](#tools)
- [Data Source](#data-source)
  - [Owned Games](#owned-games)
  - [Friends List & Achievements](#friends-list--achievements)
  - [Storefront API](#storefront-api)
- [Data Processing](#data-processing)
- [Data Visualizations](#data-visualizations)
- [Data Analysis](#data-analysis)
  - [Playtime Analysis](#playtime-analysis)
  - [Underplayed, Highly-Rated Games](#underplayed-highly-rated-games)
  - [Recommendations Based on Friends](#recommendations-based-on-friends)
- [Findings](#findings)
  - [Top 5 Games](#top-5-games)
  - [Underplayed Titles](#underplayed-titles)
  - [Recommended Games](#recommended-games)
- [Limitations](#limitations)
  - [API Constraints](#api-constraints)
  - [Personal Constraints](#personal-constraints)
- [Future Work](#future-work)

---

## Motivation
I noticed that **Steam** holds a treasure trove of personal playtime data, genre breakdowns, and friends’ gaming habits. By leveraging these APIs, this project aims to:

- **Uncover** personal gaming patterns (e.g., total hours, most-played titles).
- **Identify** hidden gems (underplayed but well-reviewed games).
- **Recommend** new titles from friends’ libraries that I do not yet own.

This project allowed me to exercise **data wrangling** skills and combine them with **web development** to produce a cohesive, user-friendly tool.

---

## Tools

- **Python (Flask)**  
  Builds the backend API that fetches and processes the user’s Steam data. Responsible for data analysis, caching, and logic for recommendation or filtering.

- **React**  
  Frontend library for creating a single-page application. It provides the form to enter SteamID, makes API requests to the Flask server, and displays the resulting data, stats, and visualizations.

- **Pandas**  
  Useful for data cleaning and transformation during prototyping or deeper EDA. Optional but handy in your analysis scripts.

- **Requests**  
  Manages HTTP calls to the **Steam Web API** and **Steam Storefront API** in Python.

- **Collections / NumPy**  
  Provides counters and numeric processing for friend-owned games, sorting by popularity, or slicing the top 5 played titles.

- **react-chartjs-2 / Chart.js**  
  Powers client-side visualizations, such as bar charts for friend ownership counts, pie charts for genre distribution, etc.

---

## Data Source

### Owned Games
Using `IPlayerService/GetOwnedGames`, the **Steam Web API** returns:
- **AppID**: Unique identifier for each game.
- **Playtime**: Tracked in minutes, converted to hours for simpler display.
- **Game Name**: For listing on the frontend.
- **Icon URLs** (optional): If the user wants to see thumbnails.

### Friends List & Achievements
- **Friends**: `ISteamUser/GetFriendList` yields a list of friend SteamIDs.
- **Achievements**: `ISteamUserStats/GetPlayerAchievements` can retrieve achievement progress for a given AppID (useful for top-played game).

### Storefront API
For each AppID, the **Storefront** endpoint (`https://store.steampowered.com/api/appdetails`) provides:
- **Genre(s)**: e.g., Action, Adventure, Strategy.
- **Metacritic Rating**: to determine underplayed, highly-rated games.
- **Type**: Verifies if it’s truly a “game,” as some AppIDs are DLC or software.

---

## Data Processing
**Flask** merges results from the Web API and Storefront API. It may store them in memory or simple data structures like dictionaries. Key steps:

1. **Convert** playtime from minutes to hours.
2. **Attach** genre and Metacritic score to each owned game.
3. **Aggregate** friends’ libraries using a `Counter`, incrementing for every game each friend owns.
4. **Exclude** user-owned games when building a “recommended games” list to avoid duplicates.

This is then returned to the React frontend, which displays all relevant stats and visualizations.

---

## Data Visualizations
On the frontend, we rely on **react-chartjs-2** to create interactive charts. Common visuals include:

- **Bar Chart**: Top 5 Games by playtime.
- **Pie / Doughnut Chart**: Distribution of genres in the user’s library.
- **Bar Chart (optional)**: Number of friends who own each recommended game.

For more in-depth exploration, a local Jupyter notebook (with libraries like Matplotlib or Seaborn) can be used. However, the user-facing data remains accessible in the React UI.

---

## Data Analysis

### Playtime Analysis
- **Total Hours**: Summed across the entire library—an eye-opening statistic to see total gaming time.
- **Top 5 Games**: Sorted by `playtime_forever` in descending order, typically revealing the user’s core preferences or longtime habits.

### Underplayed, Highly-Rated Games
We filter by low playtime (e.g., ≤120 minutes) and high Metacritic (≥75). This method highlights potential “hidden gems” in the user’s collection.

### Recommendations Based on Friends
1. Combine all friends’ libraries into a single dataset, often using a `Counter`.
2. Exclude any games the user already owns.
3. Sort by popularity (how many friends own it).
4. Limit to a smaller set (e.g., 15) for readability.
5. Optionally, display the friend-ownership counts in a bar chart.

---

## Findings

### Top 5 Games
In many cases, staple multiplayer titles like Counter-Strike 2, PUBG, or Tom Clancy’s Rainbow Six Siege dominate. Single-player epics can also appear if the user has devoted hundreds of hours to them.

### Underplayed Titles
Surprisingly, many critically acclaimed games (e.g., Deus Ex, Psychonauts) remain barely touched despite high ratings. Displaying these can motivate the user to revisit them.

### Recommended Games
Often revolve around popular friend-owned games—multiplayer titles or beloved single-player classics. Seeing how many friends own a particular game can help the user decide what to try next, especially for co-op experiences.

---

## Limitations

### API Constraints
- **Private Profiles**: Some friends lock their libraries, resulting in incomplete data.
- **Rate Limits**: If the user has a large friend list, requests can exceed Steam’s allowed calls, requiring caching or backoff strategies.

### Personal Constraints
- **Idling vs. Real Playtime**: Hours can be inflated if the user leaves games running.
- **Missing Metadata**: Certain older or lesser-known titles may lack detailed Storefront info (e.g., no Metacritic score).

---

## Future Work

- **Machine Learning**: Introduce collaborative filtering or advanced recommendation algorithms for more sophisticated suggestions.
- **Additional Visualizations**: Explore how playtime changes over months/years, or track achievements unlocked over time.
- **Caching & Scalability**: Implement robust caching layers, especially when analyzing dozens or hundreds of friend libraries.
- **Cross-Platform**: Extend to other game platforms (Epic, GOG, Origin) for a unified gaming overview.

---

**Note**: By pairing data science (filtering, summarizing, analyzing distributions) with web development (Flask, React), this project offers a hands-on example of building an end-to-end data product. With continued refinement—like more advanced recommendation logic—you can further elevate your Steam data insights.

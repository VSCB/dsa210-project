# DSA210 Project: Steam Gaming Data Analysis

## Introduction

I am planning to analyze my personal gaming data from **Steam** to gain insights into my gaming habits and preferences. By utilizing the **Steam Web API** and the **Steam Storefront API**, I intend to collect data about the games I own, how much I've played them, and what genres they belong to. Additionally, I want to examine my friends' game libraries to see what they're playing. The goal is to analyze this data to find patterns, discover underplayed games, and receive personalized game recommendations.

---

## Dataset Description

### Steam Web API

- **Purpose**: Allows access to personal Steam data.
- **Data Retrieved**:
  - **Owned Games**: List of all games I own, along with playtime statistics.
  - **Achievements**: Information about achievements unlocked in games.
  - **Friends List**: Details of my Steam friends for social data analysis.

### Steam Storefront API

- **Purpose**: Provides additional game details.
- **Data Retrieved**:
  - **Game Genres**: Classification of games into genres.
  - **Descriptions**: Summaries and overviews of each game.
  - **User Ratings**: Metacritic scores and user reviews.

---

## Project Idea and Plan

### Objectives

1. **Understand Gaming Habits**: Analyze my playtime to see which games and genres I spend the most time on.
2. **Discover Underplayed Games**: Identify highly-rated games in my library that I haven't played much.
3. **Get Recommendations**: Find new game suggestions based on my preferences and what my friends are playing.

### Data Collection

- **Fetch Owned Games**: Use the Steam Web API to retrieve a list of all games I own, including playtime.
- **Gather Game Details**: Utilize the Steam Storefront API to get genres and ratings for each game.
- **Obtain Friends' Data**: Collect information on my friends' game libraries to compare and find common interests.

### Data Analysis

#### Playtime Analysis

- Calculate total playtime across all games.
- Identify my top played games.
- Analyze playtime distribution to see if I favor certain games or genres.

#### Genre Analysis

- Determine which genres I own the most games in.
- Analyze which genres I spend the most time playing.
- Identify any discrepancies between owned genres and played genres.

#### Underplayed Highly-Rated Games

- Find games with high user ratings that I haven't played much.
- Create a list of these games as potential titles to revisit.

#### Friends' Recommendations

- Compare my game library with those of my friends.
- Identify popular games among my friends that I don't own.
- Consider these games for future purchases or to play together.

### Generating Insights

- Summarize key findings from the data analysis.
- Highlight any surprising patterns or trends.
- Develop personalized recommendations based on the analysis.

---

## Expected Outcomes

By analyzing my Steam data, I hope to gain valuable insights into my gaming behavior and discover new opportunities for enjoyment. This project will combine data collection and analysis techniques to provide a personalized look at my gaming life, ultimately leading to a more fulfilling gaming experience.

---

*Note: This project plan outlines my intended approach. Actual implementation and results may vary based on the data retrieved.*


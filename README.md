# Project

Football sandbox python project

Project used to demo football analysis and modelling from various data sources.

# Prerequiites

Before you start, ensure you meet the following requirements:
* Downloaded Python version 3.10.8
* Downloaded pyenv 
* Downloaded poetry to your local machine

# Project layout

This project has all it's code in the src/ folder which contains multiple folders for respective data providers. These specific folders has provider specific functions for fetching, cleaning and analytical purposes. There is also an 
utility/ folder that contains reusable functions across different data sources. 

### Notebooks

In this project, notebooks will be used to show various analysis work. This will include fetching and cleaning data from sources, analysis on teams as well as prediction on multiple aspects for the game of football.

### FBref

https://fbref.com/en/

Demo code for using fbref class:

1. Import fbref class: ```from src.fbref.fbref_class import FBref```
2. Define fbref class: ```fb = FBref()```
3. Look at competition dict: ```competition_dict = fb.get_competition_dict()```
4. Define competition id: ```competition_id = '9'```
5. Define season name (format: YYYY-YYYY): ```season_name = '2022-2023'```
6. Fetch league table df: ```league_table_df = fb.get_season_stats_table('league_table', competition_id, season_name)```
7. Fetch fixtures table df: ```fixtures_df = fb.get_fixtures_and_results(competition_id, season_name)```
8. Fetch top 5 leagues player table df: ```big5_players_standard_df = fb.get_big5_player_stats('standard', season_name)```

### football data

https://www.football-data.co.uk/

Demo code to access data from football-data:

1. Data manually downloaded from website above, link for competitions from England:                                     https://www.football-data.co.uk/englandm.php
2. Define season name: ```"2021_2022"```
3. If chosen competition was for Premier League, save data in following format: ```data/football_data_prem_{season_name}.csv```
4. Read football results data: ```football_data_df = pd.read_csv(f"data/football_data_prem_{season_name}.csv")```
"""Clean script for data extracted from FBref"""

import numpy as np
import pandas as pd

from src.fbref.config.fbref_config import (
    LEAGUE_TABLE_RENAME_COL_DICT,
    PLAYER_DEFENSE_FLOAT_COLUMNS,
    PLAYER_DEFENSE_RENAME_COL_DICT,
    PLAYER_DEFENSE_TOTAL_COUNT_COLUMNS,
    PLAYER_MISCELLANEOUS_FLOAT_COLUMNS,
    PLAYER_MISCELLANEOUS_RENAME_COL_DICT,
    PLAYER_MISCELLANEOUS_TOTAL_COUNT_COLUMNS,
    PLAYER_PASSING_FLOAT_COLUMNS,
    PLAYER_PASSING_RENAME_COL_DICT,
    PLAYER_PASSING_TOTAL_COUNT_COLUMNS,
    PLAYER_POSSESSION_FLOAT_COLUMNS,
    PLAYER_POSSESSION_RENAME_COL_DICT,
    PLAYER_POSSESSION_TOTAL_COUNT_COLUMNS,
    PLAYER_SHOOTING_FLOAT_COLUMNS,
    PLAYER_SHOOTING_RENAME_COL_DICT,
    PLAYER_SHOOTING_TOTAL_COUNT_COLUMNS,
    PLAYER_STANDARD_FLOAT_COLUMNS,
    PLAYER_STANDARD_RENAME_COL_DICT,
    TEAM_DEFENSE_RENAME_COL_DICT,
    TEAM_POSSESSION_RENAME_COL_DICT,
)
from src.fbref.etl.db.fetch import fetch_countries


def clean_fb_ref_column_names(fbref_df):
    """Function used to clean column names for fbref dataframes.
    Args:
        fbref_df (pandas.DataFrame): fbref dataframe
    Returns:
        fbref_df (pandas.DataFrame): Renamed fbref dataframe
    """
    # set column names

    # replace spaces and punctuation
    fbref_df.columns = [
        col_name.replace(" ", "_")
        .replace("Take-Ons", "take_ons")
        .replace("/", "_per_")
        .replace("+/-", "_plus_mins_")
        .replace("+", "_plus_")
        .replace("-", "_minus_")
        .replace("%", "_perc")
        .replace(":", "_")
        .replace("#", "no")
        for col_name in list(fbref_df.columns)
    ]
    # strip leading characters
    fbref_df.columns = [col_name.strip(" ").strip("_") for col_name in list(fbref_df.columns)]
    # make each column lower case
    fbref_df.columns = [col_name.lower() for col_name in list(fbref_df.columns)]
    return fbref_df


def clean_fb_ref_column_dtypes(fbref_df, integer_columns, float_columns, category_columns):
    """Function used to change fbref columns to correct data type"""
    # change column types
    for column in integer_columns:
        fbref_df = fbref_df.astype({column: "int32"})

    for column in float_columns:
        fbref_df = fbref_df.astype({column: "float32"})

    for column in category_columns:
        fbref_df = fbref_df.astype({column: "category"})
    return fbref_df


def clean_league_table_df(league_table_df):
    """Function used to clean league table data"""

    # change column types
    integer_columns = ["Rk", "MP", "W", "D", "L", "GF", "GA", "GD", "Pts"]
    float_columns = ["Pts/MP", "xG", "xGA", "xGD", "xGD/90"]
    category_columns = ["Squad", "Goalkeeper"]

    league_table_df = clean_fb_ref_column_dtypes(league_table_df, integer_columns, float_columns, category_columns)

    # round up dataframe
    for float_column in float_columns:
        league_table_df[float_column] = league_table_df[float_column].apply(lambda x: round(x, 2))

    # clean columns
    league_table_df["Squad"] = league_table_df["Squad"].apply(lambda x: x.strip())

    # Clean column names
    league_table_df = clean_fb_ref_column_names(league_table_df)

    # add addition columns
    league_table_df = league_table_df.assign(
        goals_per_game=lambda df_: round(df_.gf / df_.mp, 2),
        goals_conceded_per_game=lambda df_: round(df_.ga / df_.mp, 2),
        xg_per_game=lambda df_: round(df_.xg / df_.mp, 2),
        xg_against_per_game=lambda df_: round(df_.xga / df_.mp, 2),
    )

    # rename columns
    league_table_df.rename(columns=LEAGUE_TABLE_RENAME_COL_DICT, inplace=True)

    # drop columns
    league_table_df = league_table_df.drop(
        ["attendance", "top_team_scorer", "goalkeeper", "notes", "last_5"], axis=1, errors="ignore"
    )

    return league_table_df


def clean_home_away_league_table(home_away_league_table_df):
    """Function used to clean home_away_league_table data from fbref"""
    # change column types
    integer_columns = [
        "Rk",
        "Home MP",
        "Home W",
        "Home D",
        "Home L",
        "Home GF",
        "Home GA",
        "Home GD",
        "Home Pts",
        "Away MP",
        "Away W",
        "Away D",
        "Away L",
        "Away GF",
        "Away GA",
        "Away GD",
        "Away Pts",
    ]
    float_columns = [
        "Home Pts/MP",
        "Home xG",
        "Home xGA",
        "Home xGD",
        "Home xGD/90",
        "Away Pts/MP",
        "Away xG",
        "Away xGA",
        "Away xGD",
        "Away xGD/90",
    ]
    category_columns = ["Squad"]

    home_away_league_table_df = clean_fb_ref_column_dtypes(
        home_away_league_table_df, integer_columns, float_columns, category_columns
    )

    # round up dataframe
    home_away_league_table_df["Home xG"] = home_away_league_table_df["Home xG"].apply(lambda x: round(x, 1))
    home_away_league_table_df["Away xG"] = home_away_league_table_df["Away xG"].apply(lambda x: round(x, 1))

    # Clean column names
    home_away_league_table_df = clean_fb_ref_column_names(home_away_league_table_df)

    return home_away_league_table_df


def clean_fixtures_df(fixtures_df):
    """Function used to clean fixtures data from fbref"""
    # rename xg columns as we have two columns with name xg
    fixtures_df.columns = [
        "Wk",
        "Day",
        "Date",
        "Time",
        "Home",
        "home_xg",
        "Score",
        "away_xg",
        "Away",
        "Attendance",
        "Venue",
        "Referee",
        "Match Report",
        "Notes",
        "home_team_id",
        "away_team_id",
        "fixture_link",
    ]

    # change xg columns to float type
    fixtures_df["home_xg"] = fixtures_df["home_xg"].apply(lambda x: float(x) if x != "" else np.nan)
    fixtures_df["away_xg"] = fixtures_df["away_xg"].apply(lambda x: float(x) if x != "" else np.nan)

    # change column types
    integer_columns = ["Wk"]
    float_columns = ["home_xg", "away_xg"]
    category_columns = ["Day", "Home", "Away"]

    fixtures_df = clean_fb_ref_column_dtypes(fixtures_df, integer_columns, float_columns, category_columns)

    # datetime
    fixtures_df = fixtures_df.assign(
        Date=pd.to_datetime(fixtures_df["Date"]),
        kickoff=pd.to_datetime(fixtures_df["Date"] + " " + fixtures_df["Time"]),
    )
    # add columns
    fixtures_df["Score"] = fixtures_df["Score"].apply(lambda x: np.nan if x == "" else x)

    fixtures_df["home_score"] = fixtures_df["Score"].apply(
        lambda x: int(x.split("–")[0]) if isinstance(x, str) else np.nan
    )
    fixtures_df["away_score"] = fixtures_df["Score"].apply(
        lambda x: int(x.split("–")[1]) if isinstance(x, str) else np.nan
    )

    # Clean column names
    fixtures_df = clean_fb_ref_column_names(fixtures_df)

    return fixtures_df


def clean_defense_table(defense_df, per_match_columns=True):
    """Function used to clean defense table data"""

    # change column types
    integer_columns = [
        "# Pl",
        "Tackles Tkl",
        "Tackles TklW",
        "Tackles Def 3rd",
        "Tackles Mid 3rd",
        "Tackles Att 3rd",
        "Vs Dribbles Tkl",
        "Vs Dribbles Att",
        "Vs Dribbles Past",
        "Blocks Blocks",
        "Blocks Sh",
        "Blocks Pass",
        "Int",
        "Tkl+Int",
        "Clr",
        "Err",
    ]
    float_columns = ["90s"]
    category_columns = ["Squad"]

    defense_df = clean_fb_ref_column_dtypes(defense_df, integer_columns, float_columns, category_columns)

    # round up dataframe
    for float_column in float_columns:
        defense_df[float_column] = defense_df[float_column].apply(lambda x: round(x, 2))

    # clean columns
    defense_df["Squad"] = defense_df["Squad"].apply(lambda x: x.strip())

    # columns with total counts
    total_count_columns = [
        "Tackles Tkl",
        "Tackles TklW",
        "Tackles Def 3rd",
        "Tackles Mid 3rd",
        "Tackles Att 3rd",
        "Vs Dribbles Tkl",
        "Vs Dribbles Att",
        "Vs Dribbles Past",
        "Blocks Blocks",
        "Blocks Sh",
        "Blocks Pass",
        "Int",
        "Tkl+Int",
        "Clr",
        "Err",
    ]

    # add additional columns
    for column in total_count_columns:
        defense_df[f"{column}_per_match"] = defense_df.apply(lambda x: round(x[column] / x["90s"], 2), axis=1)

    # Clean column names
    defense_df = clean_fb_ref_column_names(defense_df)

    per_match_columns = [column for column in defense_df.columns if "per_match" in column]

    if per_match_columns:
        columns_to_filter = ["squad", "no_pl", "90s"] + per_match_columns
    else:
        columns_to_filter = [column for column in defense_df.columns if column not in per_match_columns]

    defense_df = defense_df[columns_to_filter]

    # rename columns
    defense_df.rename(columns=TEAM_DEFENSE_RENAME_COL_DICT, inplace=True)

    return defense_df


def clean_possession_table(possession_df, per_match_columns=True):
    """Function used to clean team possession table data from fbref"""
    stats_df = possession_df

    # rename columns
    stats_df.rename(columns=TEAM_POSSESSION_RENAME_COL_DICT, inplace=True)

    # columns with total counts
    total_count_columns = [
        "touches",
        "touches_in_defensive_penalty_area",
        "touches_in_defensive_third",
        "touches_in_midfield_third",
        "touches_in_attacking_third",
        "touches_in_attacking_penalty_area",
        "live_ball_touches",
        "successful_dribbles",
        "attempted_dribbles",
        "miscontrolled",
        "dispossessed",
        # "passes_received",
    ]

    # change column types
    integer_columns = ["no_players_used"] + total_count_columns

    float_columns = ["possession", "no_of_nineties"]
    category_columns = ["team"]

    stats_df = clean_fb_ref_column_dtypes(stats_df, integer_columns, float_columns, category_columns)

    # add additional columns
    for column in total_count_columns:
        stats_df[f"{column}_per_match"] = stats_df.apply(
            lambda x: round(x[column] / x["no_of_nineties"], 2) if x["no_of_nineties"] != 0 else np.nan, axis=1
        )

    # per match
    per_match_columns = [column for column in stats_df.columns if "per_match" in column]

    if per_match_columns:
        stats_df.drop(total_count_columns, axis=1)

    # round up dataframe
    for float_column in float_columns:
        stats_df[float_column] = stats_df[float_column].apply(lambda x: round(x, 2))

    return stats_df


def clean_player_stat_table(player_table_df, stat_type, per_match_columns=True):
    """Function used to clean player_stat_table_df data from fbref"""
    if stat_type == "standard":
        player_rename_dict = PLAYER_STANDARD_RENAME_COL_DICT
        float_columns = PLAYER_STANDARD_FLOAT_COLUMNS
        total_count_columns = []

        player_table_df["Playing Time Min"] = player_table_df["Playing Time Min"].apply(lambda x: x.replace(",", ""))
    elif stat_type == "passing":
        player_rename_dict = PLAYER_PASSING_RENAME_COL_DICT
        float_columns = PLAYER_PASSING_FLOAT_COLUMNS
        total_count_columns = PLAYER_PASSING_TOTAL_COUNT_COLUMNS
    elif stat_type == "defense":
        player_rename_dict = PLAYER_DEFENSE_RENAME_COL_DICT
        float_columns = PLAYER_DEFENSE_FLOAT_COLUMNS
        total_count_columns = PLAYER_DEFENSE_TOTAL_COUNT_COLUMNS
    elif stat_type == "possession":
        player_rename_dict = PLAYER_POSSESSION_RENAME_COL_DICT
        float_columns = PLAYER_POSSESSION_FLOAT_COLUMNS
        total_count_columns = PLAYER_POSSESSION_TOTAL_COUNT_COLUMNS
    elif stat_type == "shooting":
        player_rename_dict = PLAYER_SHOOTING_RENAME_COL_DICT
        float_columns = PLAYER_SHOOTING_FLOAT_COLUMNS
        total_count_columns = PLAYER_SHOOTING_TOTAL_COUNT_COLUMNS
    elif stat_type == "miscellaneous":
        player_rename_dict = PLAYER_MISCELLANEOUS_RENAME_COL_DICT
        float_columns = PLAYER_MISCELLANEOUS_FLOAT_COLUMNS
        total_count_columns = PLAYER_MISCELLANEOUS_TOTAL_COUNT_COLUMNS

    # replace blanks with NaN
    player_table_df = player_table_df.replace("", np.nan)

    # rename columns
    player_table_df.rename(columns=player_rename_dict, inplace=True)

    # add columns
    player_table_df = player_table_df.assign(
        country=player_table_df.country.apply(lambda x: x.split(" ")[1] if isinstance(x, str) else x),
        goalkeeper=player_table_df.position.str.contains("GK"),
        defender=player_table_df.position.str.contains("DF"),
        midfielder=player_table_df.position.str.contains("MF"),
        attacker=player_table_df.position.str.contains("FW"),
        competition=player_table_df.competition.apply(lambda x: x.split(maxsplit=1)[1]),
        age=player_table_df.age.apply(lambda x: x.split("-")[0] if isinstance(x, str) else np.nan),
    )

    # change column types
    integer_columns = []
    category_columns = ["country", "team"]

    player_table_df = clean_fb_ref_column_dtypes(player_table_df, integer_columns, float_columns, category_columns)

    # add additional per 90 columns
    if len(total_count_columns) > 0:
        for column in total_count_columns:
            player_table_df[f"{column}_per_90"] = player_table_df.apply(
                lambda x: round(x[column] / x["no_of_nineties"], 2) if x["no_of_nineties"] != 0 else np.nan, axis=1
            )

        # per match
        per_match_columns = [column for column in player_table_df.columns if "per_90" in column]

        if per_match_columns:
            player_table_df.drop(total_count_columns, axis=1)

    # round up dataframe
    for float_column in float_columns:
        player_table_df[float_column] = player_table_df[float_column].apply(lambda x: round(x, 2))

    # replace nulls in numerical columns with zero
    numerical_cols = player_table_df.select_dtypes(include=["float", "int"]).columns

    player_table_df[numerical_cols] = player_table_df[numerical_cols].replace(np.nan, 0)

    return player_table_df


def clean_full_match_stat_df(full_match_stat_df):
    """Function used to clean full_match_stat_df
    Args:
        full_match_stat_df (pandas.DataFrame): merged dataframe of match stats
    """
    # rename columns
    full_match_stat_df = clean_fb_ref_column_names(full_match_stat_df)

    full_match_stat_df = full_match_stat_df.assign(
        age=full_match_stat_df.age.apply(lambda x: x.split("-")[0] if isinstance(x, str) else np.nan),
        country=full_match_stat_df.nation.apply(lambda x: x.split(" ")[1] if isinstance(x, str) else x),
    )

    category_column_list = ["player", "nation", "country", "pos", "player_id", "player_link"]
    numeric_columns = [column for column in full_match_stat_df.columns if column not in category_column_list]

    # float for all numeric columns
    full_match_stat_df = full_match_stat_df.replace("", 0)

    full_match_stat_df = clean_fb_ref_column_dtypes(
        full_match_stat_df, integer_columns=[], float_columns=numeric_columns, category_columns=category_column_list
    )

    # round up dataframe
    for numeric_column in numeric_columns:
        full_match_stat_df[numeric_column] = full_match_stat_df[numeric_column].apply(lambda x: round(x, 2))

    # rename columns
    full_match_stat_df.rename(
        columns={
            "player": "player_name",
            "no": "shirt_no",
            "pos": "position",
            "int": "interceptions",
            "1_per_3": "one_per_three",
        },
        inplace=True,
    )

    # drop
    full_match_stat_df.drop(columns=["nation"], axis=1, inplace=True)
    return full_match_stat_df


def clean_big5_player_info(big5_player_info_df):
    """Function used to clean big5 player info df"""
    # fetch countries df
    country_df = fetch_countries()

    # replace blanks
    cleaned_player_df = big5_player_info_df.replace("", np.nan)
    cleaned_player_df = cleaned_player_df.drop_duplicates(subset=["player_id"])

    # clean player data
    cleaned_player_df = (
        cleaned_player_df.assign(
            country=cleaned_player_df.Nation.apply(lambda x: x.split(" ")[1] if isinstance(x, str) else x),
        )
        .merge(country_df, left_on="country", right_on="country_code")
        .rename(
            columns={
                "Player": "player_name",
                "Born": "year_of_birth",
                "Pos": "position",
            }
        )
    )[["player_id", "year_of_birth", "position", "player_name", "player_link", "country_id"]]
    return cleaned_player_df

""" Script used to help fetch data from football-data. """

import pandas as pd

from src.football_data.etl.clean import clean_football_data


def get_football_data_seasons(season_name_list):
    """Function used to grab seasons worth of data
    Args:
        season_name_list (List): List of strings indicating season names, format "YYYY_YYYY"

    Returns:
        cleaned_seasons_football_data_df (pandas.DataFrame): dataframe of fixture results data
    """
    cleaned_season_data_list = []

    for season_name in season_name_list:
        football_data_df = pd.read_csv(f"data/football_data_prem_{season_name}.csv")
        cleaned_football_data_df = clean_football_data(
            football_data_df=football_data_df,
            season_name=season_name,
            include_additional_columns=True,
        )
        cleaned_season_data_list.append(cleaned_football_data_df)

    cleaned_seasons_football_data_df = pd.concat(cleaned_season_data_list)

    return cleaned_seasons_football_data_df

""" Script used to help clean data from football-data. """

import pandas as pd

from src.football_data.config.football_data_config import (
    ADDITIONAL_FOOTBALL_DATA_COLUMNS,
    MAIN_FOOTBALL_DATA_COLUMNS,
)


def clean_football_data(football_data_df, season_name, include_additional_columns=False):
    """Function used to clean football data grabbed from football-data

    Args:
        football_data_df (pandas.DataFrame): dataframe of football results from football-data
        season_name (str): season in question

    Returns:
        cleaned_football_data_df (pandas.DataFrame): cleaned dataframe of football results
    """
    football_data_df.columns = [col_name.lower() for col_name in football_data_df.columns]

    cleaned_football_data_df = (
        football_data_df.rename(
            columns={
                "div": "league_code",
            }
        )
        .assign(
            kickoff=pd.to_datetime(football_data_df.date + " " + football_data_df.time),
            season_name=season_name,
        )
        .astype(
            {
                "league_code": "category",
                "hometeam": "category",
                "awayteam": "category",
                "ftr": "category",
                "season_name": "category",
            }
        )
    )

    if include_additional_columns:
        columns_of_interest = MAIN_FOOTBALL_DATA_COLUMNS + ADDITIONAL_FOOTBALL_DATA_COLUMNS
    else:
        columns_of_interest = MAIN_FOOTBALL_DATA_COLUMNS

    cleaned_football_data_df = cleaned_football_data_df[columns_of_interest]
    return cleaned_football_data_df

"""Script used for analysis on players and teams"""

import math

import pandas as pd


def get_percentile(rank, no_values):
    """Get percentile of value"""
    decimal_percentile = 1 - rank / no_values
    rounded_percentile = math.floor(decimal_percentile * 100)
    return rounded_percentile


def get_player_percentile_df(stats_list, input_df):
    """Function used to output percentile values of certain stats for each player."""
    no_values = len(input_df)

    percentile_dict = {}
    percentile_dict["player_name"] = input_df.player_name
    percentile_dict["position"] = input_df.position
    percentile_dict["age"] = input_df.age
    percentile_dict["no_of_nineties"] = input_df.no_of_nineties

    for stat in stats_list:
        rank_list = list(input_df[stat].rank(ascending=False, method="max"))
        percentile_list = [get_percentile(rank, no_values) for rank in rank_list]
        percentile_dict[f"{stat}_percentile"] = percentile_list

    percentile_df = pd.DataFrame(percentile_dict)

    # add aggregated rank
    percentile_df = percentile_df.assign(
        stat_score=percentile_df.drop(["no_of_nineties", "age"], axis=1)
        .select_dtypes(include=["float", "int"])
        .mean(axis=1)
    )
    return percentile_df

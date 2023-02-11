"""Script to fetch data extracted from FBref"""
from src.fbref.fbref_class import FBref

fb = FBref()


def get_stat_rank_df(input_df, stat_name):
    """Function used to get the rank of"""

    stat_rank_df = (
        input_df.sort_values(by=stat_name, ascending=False)
        .reset_index(drop=True)
        .reset_index()
        .assign(index=lambda df_: df_.index + 1)
        .rename(columns={"index": f"{stat_name}_rank"})[[f"{stat_name}_rank", "squad", f"{stat_name}", "season_name"]]
    )
    return stat_rank_df


def get_full_match_stats(home_team_id, away_team_id, fixture_link):
    """Function used to grab dictionary of team match stats"""
    stat_type_list = ["summary", "passing", "passing_types", "defense", "possession", "misc", "keeper", "shots"]

    team_match_stats_dict = {}

    for team_id in [home_team_id, away_team_id]:
        match_stats_dict = {}

        for stat_type in stat_type_list:
            stat_df = fb.get_fixture_stats(fixture_url=fixture_link, team_id=team_id, stat_type=stat_type)
            match_stats_dict[stat_type] = stat_df

        full_match_stat_df = (
            match_stats_dict["summary"]
            .merge(match_stats_dict["passing"])
            .merge(match_stats_dict["passing_types"])
            .merge(match_stats_dict["defense"])
            .merge(match_stats_dict["possession"])
            .merge(match_stats_dict["misc"])
        )

        team_match_stats_dict[team_id] = full_match_stat_df
    return team_match_stats_dict

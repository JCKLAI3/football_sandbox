"""Script to fetch data extracted from FBref"""


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

"""Script used to help with general functionality"""


def flatten_cols(df):
    """Function used to flatten multi indexed columns in panda dfs."""
    df.columns = ["_".join(x) for x in df.columns.to_flat_index()]
    return df

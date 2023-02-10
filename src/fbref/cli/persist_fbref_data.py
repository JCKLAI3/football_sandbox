from typing import List, Optional

import pandas as pd
import typer
from tqdm import tqdm

from src.fbref.etl.db.clean import clean_competition_seasons_df, clean_fixtures_df
from src.fbref.fbref_class import FBref
from src.utility.sql.fetch_and_persist import persist_to_db

app = typer.Typer()

fb = FBref()


@app.command()
def main(
    competition_ids: Optional[List[int]] = typer.Option(None),
    season_names: Optional[List[str]] = typer.Option(None),
):
    """
    CLI script used to persist football data from FBref.
    """
    competition_id_list = [str(league_id) for league_id in competition_ids]
    season_name_list = season_names

    competition_season_data_list = []
    fixtures_df_list = []

    for league_id in tqdm(competition_id_list):
        for season_name in season_name_list:
            competition_season_id = int(season_name.replace("-", "") + league_id)

            # append competition season data
            competition_season_data_list.append([competition_season_id, season_name, league_id])

            # # get fixtures data
            fixtures_df = fb.get_fixtures_and_results(league_id, season_name)
            fixtures_df = clean_fixtures_df(fixtures_df)
            fixtures_df_list.append(fixtures_df)

    competition_seasons_df = pd.DataFrame(
        competition_season_data_list, columns=["competition_seasons_id", "season_name", "competition_id"]
    )
    competition_seasons_df = clean_competition_seasons_df(competition_seasons_df)

    fixtures_df = pd.concat(fixtures_df_list)

    persist_dict = {
        "competition_seasons": competition_seasons_df,
        "fixtures": fixtures_df,
    }

    for table_name, df_to_persist in persist_dict.items():
        persist_to_db(
            df_to_persist=df_to_persist,
            table_name=table_name,
            schema_name="fbref",
        )


if __name__ == """__main__""":
    app()

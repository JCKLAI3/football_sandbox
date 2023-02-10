from typing import List, Optional

import pandas as pd
import typer
from tqdm import tqdm

from src.fbref.config.fbref_config import CURRENT_SEASON
from src.fbref.etl.db.clean import clean_competition_seasons_df, clean_fixtures_df
from src.fbref.etl.db.fetch import fetch_competition_seasons, fetch_fixtures
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

    # current season in id form
    current_season = CURRENT_SEASON.replace("-", "")

    # grab competition seasons in db
    db_competition_seasons_df = fetch_competition_seasons()

    if len(db_competition_seasons_df) > 0:
        competition_seasons_ids_in_db = list(db_competition_seasons_df.competition_seasons_id)
    else:
        competition_seasons_ids_in_db = []

    # grab competition seasons to persist data for
    input_competition_seasons_list = [
        int(season_name.replace("-", "") + competition_id)
        for competition_id in competition_id_list
        for season_name in season_name_list
    ]

    competition_seasons_id_to_persist_data_for = [
        competition_season
        for competition_season in input_competition_seasons_list
        if (str(competition_season)[:8] == current_season) or (competition_season not in competition_seasons_ids_in_db)
    ]

    if len(competition_seasons_id_to_persist_data_for) > 0:
        pass
    else:
        raise Exception("No competition seasons to persist data for")

    # fetch data

    competition_season_data_list = []
    fixtures_df_list = []

    for competition_season_id in tqdm(competition_seasons_id_to_persist_data_for):
        competition_id = str(competition_season_id)[8:]
        season_name = str(competition_season_id)[:4] + "-" + str(competition_season_id)[4:8]

        # append competition season data
        if competition_season_id not in competition_seasons_ids_in_db:
            competition_season_data_list.append([competition_season_id, season_name, competition_id])

        # get fixtures data
        fixtures_df = fb.get_fixtures_and_results(competition_id, season_name)
        fixtures_df = clean_fixtures_df(fixtures_df)

        # filter fixtures data
        fixtures_in_db = fetch_fixtures(competition_season_id)
        if len(fixtures_in_db) > 0:
            fixtures_to_persist_df = fixtures_df[~fixtures_df.fixture_id.isin(list(fixtures_in_db.fixture_id))]
        else:
            fixtures_to_persist_df = fixtures_df

        fixtures_df_list.append(fixtures_to_persist_df)

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
        print(f"Persisted {len(df_to_persist)} rows for table {table_name}.")


if __name__ == """__main__""":
    app()

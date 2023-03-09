"""Script used to clean data to be persisted to our fbref db"""

from datetime import datetime

from src.fbref.etl.db.fetch import fetch_seasons


def clean_competition_seasons_df(competition_seasons_df):
    """Function used to clean competition seasons to format needed to persist to db

    Args:
        competition_seasons_df (pandas.DataFrame): competition_seasons_df with columns
        competition_season_id, season_name and competition_id
    """
    seasons_df = fetch_seasons()
    season_id_dict = dict(zip(seasons_df.season_name, seasons_df.season_id))

    # add season id column
    competition_seasons_df = competition_seasons_df.assign(
        season_id=competition_seasons_df.season_name.map(season_id_dict),
    )
    # filter dataframe
    competition_seasons_df = competition_seasons_df[
        [
            "competition_seasons_id",
            "season_id",
            "competition_id",
        ]
    ]
    return competition_seasons_df


def clean_fixtures_df(fixtures_df):
    """Function used to clean fixtures data to format needed to persist to db.

    Args:
        fixtures_df (pandas.DataFrame): fixtures df grabbed from FBref class.
    """
    # clean fixtures df

    # filter postponed games
    fixtures_df = fixtures_df.loc[lambda dfr_: dfr_.notes != "Match Postponed"]

    # filter future games
    fixtures_df = fixtures_df.loc[lambda dfr_: dfr_.kickoff < datetime.today()]

    # get league_id and season_name
    league_id = fixtures_df.competition_id.iloc[0]
    season_name = fixtures_df.season_name.iloc[0]

    fixtures_df = fixtures_df.assign(
        fixture_id=fixtures_df["fixture_link"].apply(lambda x: x.split("/")[5]),
        competition_seasons_id=int(season_name + str(league_id)),
    )

    # rename columns

    fixtures_df = fixtures_df[
        [
            "fixture_id",
            "competition_seasons_id",
            "kickoff",
            "home_team_id",
            "home_score",
            "away_score",
            "away_team_id",
            "fixture_link",
        ]
    ]
    return fixtures_df

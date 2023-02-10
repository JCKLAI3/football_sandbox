"""Script used to fetch data from db"""

from src.utility.sql.fetch_and_persist import query_db


def fetch_seasons():
    return query_db("SELECT * FROM fbref.seasons")


def fetch_competitions():
    return query_db("SELECT * FROM fbref.competitions")


def fetch_competition_seasons():
    return query_db(
        """
        SELECT
        competition_seasons_id,
        cs.season_id,
        s.season_name,
        cs.competition_id,
        c.competition_name
        FROM fbref.competition_seasons as cs
        JOIN fbref.seasons as s
        ON cs.season_id = s.season_id
        JOIN fbref.competitions as c
        ON cs.competition_id = c.competition_id
        """
    )


def fetch_fixtures(competition_season_id=None):
    if competition_season_id is None:
        fixture_query = "SELECT * FROM fbref.fixtures"
    else:
        fixture_query = f"SELECT * FROM fbref.fixtures WHERE competition_seasons_id = {competition_season_id}"
    return query_db(fixture_query)

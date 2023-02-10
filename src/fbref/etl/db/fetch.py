"""Script used to fetch data from db"""

from src.utility.sql.fetch_and_persist import query_db


def fetch_seasons():
    return query_db("SELECT * FROM fbref.seasons")


def fetch_competitions():
    return query_db("SELECT * FROM fbref.competitions")


def fetch_competition_seasons():
    return query_db("SELECT * FROM fbref.competition_seasons")

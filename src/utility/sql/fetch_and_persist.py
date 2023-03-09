"""Script used to fetch and persist to db."""

import os

import pandas as pd
import sqlalchemy as db
from sqlalchemy.sql import text


def create_db_engine(db_user, db_password, db_host, db_port, db_name):
    """Function used to create a db engine"""
    engine = db.create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
    return engine


def query_db(query_text, engine=None):
    """Function used to query data from db."""

    if engine is None:
        engine = create_db_engine(
            db_user=os.environ.get("POSTGRES_USER"),
            db_password=os.environ.get("POSTGRES_PASS"),
            db_host=os.environ.get("POSTGRES_HOST"),
            db_port=os.environ.get("POSTGRES_PORT"),
            db_name=os.environ.get("POSTGRES_DB"),
        )

    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text(query_text))

    db_table_df = pd.DataFrame(query.fetchall())
    return db_table_df


def persist_to_db(df_to_persist, table_name, schema_name, engine=None):
    """Function used to persist data to db"""

    if engine is None:
        engine = create_db_engine(
            db_user=os.environ.get("POSTGRES_USER"),
            db_password=os.environ.get("POSTGRES_PASS"),
            db_host=os.environ.get("POSTGRES_HOST"),
            db_port=os.environ.get("POSTGRES_PORT"),
            db_name=os.environ.get("POSTGRES_DB"),
        )

    df_to_persist.to_sql(table_name, con=engine, schema=schema_name, if_exists="append", index=False)
    print("Data Persisted")

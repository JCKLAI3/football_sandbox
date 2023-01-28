"""Script used to fetch and persist to db."""

import pandas as p
import sqlalchemy as db
from sqlalchemy.sql import text


def create_db_engine(db_user, db_password, db_host, db_port, db_name):
    """Function used to create a db engine"""
    engine = db.create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
    return engine


def query_db(query_text, engine):
    """Function used to query data from db."""

    with engine.connect().execution_options(autocommit=True) as conn:
        query = conn.execute(text(query_text))

    db_table_df = pd.DataFrame(query.fetchall())
    return db_table_df


def persist_to_db(df_to_persist, table_name, schema_name, engine):
    """Function used to persist data to db"""
    with engine.connect().execution_options(autocommit=True) as conn:
        df_to_persist.to_sql(table_name, con=engine, schema=schema_name, if_exists="append", index=False)
    print("Data Persisted")

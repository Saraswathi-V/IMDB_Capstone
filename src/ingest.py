#ingest/bronze layer
import pandas as pd
from loguru import logger

from src.config import db
from src.models import Movie


def load_imdb_data() -> pd.DataFrame:
    logger.info("Loading IMDb datasets...")

    basics = pd.read_csv(
        "data/title.basics.tsv",
        sep="\t",
        na_values="\\N",
        low_memory=False,
    )

    ratings = pd.read_csv(
        "data/title.ratings.tsv",
        sep="\t",
        na_values="\\N",
    )

    logger.info("Merging basics and ratings...")
    df = basics.merge(ratings, on="tconst", how="left")

    # Keep only movies
    df = df[df["titleType"] == "movie"].copy()

    logger.info(f"Rows after movie filter: {len(df)}")
    return df


def preprocess_minimal(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Minimal preprocessing for RAW layer...")

    df = df[
        [
            "tconst",
            "primaryTitle",
            "originalTitle",
            "startYear",
            "runtimeMinutes",
            "genres",
            "averageRating",
            "numVotes",
        ]
    ].copy()

    # Numeric cleaning
    df.loc[:, "startYear"] = pd.to_numeric(df["startYear"], errors="coerce").fillna(0).astype(int)
    df.loc[:, "runtimeMinutes"] = pd.to_numeric(df["runtimeMinutes"], errors="coerce").fillna(0).astype(int)
    df.loc[:, "averageRating"] = pd.to_numeric(df["averageRating"], errors="coerce").fillna(0.0)
    df.loc[:, "numVotes"] = pd.to_numeric(df["numVotes"], errors="coerce").fillna(0).astype(int)

    # Text normalization (light — full cleaning happens later)
    df.loc[:, "primaryTitle"] = df["primaryTitle"].astype(str).str.strip()
    df.loc[:, "originalTitle"] = df["originalTitle"].astype(str).str.strip()

    # Split genres into list
    df.loc[:, "genres"] = df["genres"].fillna("").apply(
        lambda x: x.split(",") if x else []
    )

    # Remove duplicates
    df = df.drop_duplicates(subset=["tconst"])

    return df


def insert_raw_movies(df: pd.DataFrame) -> None:
    logger.info("Validating records with Pydantic and inserting into MongoDB (RAW layer)...")

    records = []
    for _, row in df.iterrows():
        movie = Movie(
            tconst=row["tconst"],
            primaryTitle=row["primaryTitle"],
            originalTitle=row["originalTitle"],
            startYear=row["startYear"],
            runtimeMinutes=row["runtimeMinutes"],
            genres=row["genres"],
            averageRating=row["averageRating"],
            numVotes=row["numVotes"],
        )
        records.append(movie.model_dump())

    db.raw_movies.drop()
    db.raw_movies.insert_many(records)

    logger.success(f"Inserted {len(records)} RAW movie records into MongoDB")


if __name__ == "__main__":
    df_raw = load_imdb_data()
    df_raw = preprocess_minimal(df_raw)
    insert_raw_movies(df_raw)

    logger.success("RAW INGESTION COMPLETED SUCCESSFULLY")

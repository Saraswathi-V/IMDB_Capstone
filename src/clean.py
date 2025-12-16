#clean/ silver layer: clean and validate movie data from RAW layer and store in CLEAN collection
import pandas as pd
from loguru import logger

from src.config import db
from src.models import Movie


def fetch_raw_movies() -> pd.DataFrame:
    logger.info("Loading RAW movies from MongoDB...")

    data = list(db.raw_movies.find({}, {"_id": 0}))
    df = pd.DataFrame(data)

    logger.info(f"RAW row count: {len(df)}")
    return df


def clean_movies(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Cleaning movie data (SILVER layer)...")

    # Handle missing values
    df["primaryTitle"] = df["primaryTitle"].fillna("").str.lower().str.strip()
    df["originalTitle"] = df["originalTitle"].fillna("").str.lower().str.strip()

    df["startYear"] = df["startYear"].fillna(0).astype(int)
    df["runtimeMinutes"] = df["runtimeMinutes"].fillna(0).astype(int)
    df["averageRating"] = df["averageRating"].fillna(0.0)
    df["numVotes"] = df["numVotes"].fillna(0).astype(int)

    # Ensure genres is always a list
    df["genres"] = df["genres"].apply(lambda x: x if isinstance(x, list) else [])

    # Remove duplicates
    df = df.drop_duplicates(subset=["tconst"])

    logger.info(f"SILVER row count after cleaning: {len(df)}")
    return df


def insert_clean_movies(df: pd.DataFrame) -> None:
    logger.info("Validating and inserting CLEAN movies into MongoDB...")

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

    db.clean_movies.drop()
    db.clean_movies.insert_many(records)

    logger.success(f"Inserted {len(records)} CLEAN movie records")


if __name__ == "__main__":
    df_raw = fetch_raw_movies()
    df_clean = clean_movies(df_raw)
    insert_clean_movies(df_clean)

    logger.success("CLEAN (SILVER) PIPELINE COMPLETED")

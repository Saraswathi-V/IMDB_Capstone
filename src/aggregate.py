# AGGREGATE / GOLD LAYER

import pandas as pd
from loguru import logger
from src.config import db


def fetch_clean_movies() -> pd.DataFrame:
    logger.info("Loading CLEAN movies from MongoDB (Silver layer)...")

    data = list(db.clean_movies.find({}, {"_id": 0}))
    df = pd.DataFrame(data)

    logger.info(f"CLEAN row count: {len(df)}")
    return df


def build_aggregations(df: pd.DataFrame) -> dict:
    logger.info("Building AGGREGATED datasets (Gold layer)...")

    # ---------------------------
    # 1. MOVIES BY GENRE
    # ---------------------------
    df_exploded = df.explode("genres")
    df_exploded = df_exploded[df_exploded["genres"] != ""]

    movies_by_genre = (
        df_exploded.groupby("genres")
        .agg(
            movie_count=("tconst", "count"),
            avg_rating=("averageRating", "mean"),
            total_votes=("numVotes", "sum"),
        )
        .reset_index()
        .sort_values("movie_count", ascending=False)
    )

    # ---------------------------
    # 2. MOVIES BY YEAR (FIXED)
    # ---------------------------
    # Filter out invalid / missing years
    df_valid_years = df[
        (df["startYear"] >= 1888) &  # first known films
        (df["startYear"] <= 2025)    # future buffer
    ]

    movies_by_year = (
        df_valid_years.groupby("startYear")
        .agg(
            movie_count=("tconst", "count"),
            avg_rating=("averageRating", "mean"),
        )
        .reset_index()
        .sort_values("startYear")
    )

    # ---------------------------
    # 3. TOP MOVIES
    # ---------------------------
    top_movies = (
        df[
            (df["numVotes"] >= 10_000) &
            (df["averageRating"] > 0)
        ]
        .sort_values("averageRating", ascending=False)
        .head(100)
    )

    return {
        "movies_by_genre": movies_by_genre,
        "movies_by_year": movies_by_year,
        "top_movies": top_movies,
    }


def insert_aggregates(aggregates: dict) -> None:
    logger.info("Writing Gold datasets back to MongoDB...")

    db.movies_by_genre.drop()
    db.movies_by_year.drop()
    db.top_movies.drop()

    db.movies_by_genre.insert_many(
        aggregates["movies_by_genre"].to_dict("records")
    )
    db.movies_by_year.insert_many(
        aggregates["movies_by_year"].to_dict("records")
    )
    db.top_movies.insert_many(
        aggregates["top_movies"].to_dict("records")
    )

    logger.success("Gold layer datasets inserted successfully")


if __name__ == "__main__":
    df_clean = fetch_clean_movies()
    aggregates = build_aggregations(df_clean)
    insert_aggregates(aggregates)

    logger.success("AGGREGATION PIPELINE COMPLETED SUCCESSFULLY")

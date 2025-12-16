from loguru import logger
from src.config import db

def create_indexes() -> None:
    logger.info("Creating MongoDB indexes...")

    # RAW
    db.raw_movies.create_index("tconst")

    # CLEAN
    db.clean_movies.create_index("tconst", unique=True)
    db.clean_movies.create_index("startYear")
    db.clean_movies.create_index("genres")

    # GOLD
    db.movies_by_genre.create_index("genres")
    db.movies_by_year.create_index("startYear")
    db.top_movies.create_index("averageRating")

    logger.success("Indexes created successfully")

if __name__ == "__main__":
    create_indexes()

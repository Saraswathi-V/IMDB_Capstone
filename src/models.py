# models.py: Define Pydantic models for movie data validation
from pydantic import BaseModel
from typing import List


class Movie(BaseModel):
    tconst: str
    primaryTitle: str
    originalTitle: str
    startYear: int
    runtimeMinutes: int
    genres: List[str]
    averageRating: float
    numVotes: int

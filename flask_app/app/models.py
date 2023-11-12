from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class FilmFilter(BaseModel):
    page: Optional[int] = 1
    page_size: Optional[int] = 10
    title: Optional[str] = None
    director: Optional[str] = None
    order_by: Optional[str] = "episode_id"
    planet: Optional[str]


class PlanetsFilter(BaseModel):
    page: Optional[int] = 1
    page_size: Optional[int] = 10
    film: Optional[str] = None
    order_by: Optional[str] = "episode_id"
    name: Optional[str] = None
    resident: Optional[str] = None


class Message(BaseModel):
    message: str


class Error(BaseModel):
    Error: str


class Film(BaseModel):
    title: str
    episode_id: int
    director: str
    producer: List[str]
    release_date: str
    planets: List[str]
    created: str = Field(default_factory=now_str)


class FilmsResponse(BaseModel):
    films: List[Film]


class Planet(BaseModel):
    name: str
    rotation_period: Optional[str]
    orbital_period: Optional[str]
    diameter: Optional[str]
    climate: Optional[str]
    gravity: Optional[str]
    terrain: Optional[str]
    surface_water: Optional[str]
    population: Optional[str]
    residents: Optional[List[str]]
    films: List[str]
    created: str = Field(default_factory=now_str)


class PlanetsResponse(BaseModel):
    planets: List[Planet]

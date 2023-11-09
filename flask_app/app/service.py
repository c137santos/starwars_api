from typing import List, Optional
from bson import ObjectId
from db import MongoDBConnection


class FilmService:
    @staticmethod
    def create(film_data: dict) -> ObjectId:
        return MongoDBConnection.films().insert_one(film_data).inserted_id

    @staticmethod
    def update(film_id: str, film_data: dict) -> None:
        result = MongoDBConnection.films().update_one(
            {"_id": ObjectId(film_id)}, {"$set": film_data}
        )
        if result.matched_count == 0:
            raise ValueError(f"Film not found with ID: {film_id}")

    @staticmethod
    def list(
        title: Optional[str] = None,
        director: Optional[str] = None,
        order_by: str = "episode_id",
        page: int = 1,
        page_size: int = 10,
    ) -> List[dict]:
        filter_query = {}
        if title:
            filter_query["title"] = {
                "$regex": title,
                "$options": "i",
            }
        if director:
            filter_query["director"] = {
                "$regex": director,
                "$options": "i",
            }

        d = 1
        if order_by[0] == "-":
            order_by = order_by[1:]
            d = -1

        skip = (page - 1) * page_size
        return list(
            MongoDBConnection.films()
            .find(filter_query)
            .sort(order_by, d)
            .skip(skip)
            .limit(page_size)
        )


class PlanetService:
    @staticmethod
    def create(planet_data: dict) -> ObjectId:
        return MongoDBConnection.planets().insert_one(planet_data).inserted_id

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
        planet: Optional[str] = None,
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
        if planet:
            filter_query["planets"] = {
                "$regex": planet,
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

    @staticmethod
    def update(planet_id: str, planet_data: dict) -> None:
        result = MongoDBConnection.planets().update_one(
            {"_id": ObjectId(planet_id)}, {"$set": planet_data}
        )
        if result.matched_count == 0:
            raise ValueError(f"Planet not found with ID: {planet_id}")

    @staticmethod
    def list(
        name: Optional[str],
        page: int = 1,
        page_size: int = 10,
        film: Optional[str] = None,
        order_by: Optional[str] = "name",
        resident: Optional[str] = None,
    ) -> List[dict]:
        filter_query = {}
        if name:
            filter_query["name"] = {"$regex": name, "$options": "i"}
        if film:
            filter_query["films"] = {"$regex": film, "$options": "i"}
        if resident:
            filter_query["resident"] = {"$regex": resident, "$options": "i"}

        d = 1
        if order_by[0] == "-":
            order_by = order_by[1:]
            d = -1

        skip = (page - 1) * page_size
        return list(
            MongoDBConnection.planets()
            .find(filter_query)
            .sort(order_by, d)
            .skip(skip)
            .limit(page_size)
        )

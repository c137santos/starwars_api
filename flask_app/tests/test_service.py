import pytest
from bson import ObjectId

from service import FilmService
from db import MongoDBConnection


def test_mongodb_connection_setup(mongo_mock):
    connection = MongoDBConnection.get_client()
    actual_host = connection.address[0]
    actual_port = connection.address[1]

    assert actual_host == "localhost"
    assert actual_port == 27017


def test_create_film(mongo_mock):
    film_data = {
        "title": "Test Film",
        "episode_id": 1,
        "director": "Test Director",
        "producer": ["Test Producer"],
        "release_date": "2023-01-01",
        "planets": ["Earth"],
    }

    film_id = FilmService.create(film_data)
    assert film_id is not None

    created_film = MongoDBConnection.films().find_one({"_id": film_id})
    assert created_film is not None
    assert created_film["title"] == "Test Film"


def test_update_film(mongo_mock):
    film_data = {
        "title": "Old Title",
        "episode_id": 2,
        "director": "Test Director",
        "producer": ["Test Producer"],
        "release_date": "2023-01-02",
        "planets": ["Mars"],
    }
    film_id = MongoDBConnection.films().insert_one(film_data).inserted_id

    update_data = {"title": "New Title"}
    FilmService.update(str(film_id), update_data)

    updated_film = MongoDBConnection.films().find_one({"_id": film_id})
    assert updated_film["title"] == "New Title"


def test_delete_film(mongo_mock):
    film_data = {
        "title": "Old Title",
        "episode_id": 2,
        "director": "Test Director",
        "producer": ["Test Producer"],
        "release_date": "2023-01-02",
        "planets": ["Mars"],
    }
    film_id = MongoDBConnection.films().insert_one(film_data).inserted_id

    FilmService.delete(str(film_id))

    delete_film = MongoDBConnection.films().find_one({"_id": film_id})
    assert delete_film is None


def test_delete_film_raise(mongo_mock):
    film_id = ObjectId("5" * 24)
    with pytest.raises(ValueError):
        FilmService.delete(film_id)


def test_list_films(mongo_mock):
    film_data_1 = {"title": "Film One", "episode_id": 1, "director": "Director One"}
    film_data_2 = {"title": "Film Two", "episode_id": 2, "director": "Director Two"}
    MongoDBConnection.films().insert_many([film_data_1, film_data_2])

    films = FilmService.list()
    assert len(films) == 2

    filtered_films = FilmService.list(**{"title": "Film One"})
    assert len(filtered_films) == 1
    assert filtered_films[0]["title"] == "Film One"


def test_list_films_order_by(mongo_mock):
    film_data_1 = {"title": "Film One", "episode_id": 1, "director": "Director One"}
    film_data_2 = {"title": "Film Two", "episode_id": 2, "director": "Director Two"}
    MongoDBConnection.films().insert_many([film_data_1, film_data_2])

    filtered_films = FilmService.list(**{"order_by": "episode_id"})
    assert len(filtered_films) == 2
    assert filtered_films[0]["title"] == "Film One"

    filtered_films = FilmService.list(**{"order_by": "-episode_id"})
    assert len(filtered_films) == 2
    assert filtered_films[0]["title"] == "Film Two"

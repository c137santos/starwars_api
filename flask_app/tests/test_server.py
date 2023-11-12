import pytest
from mongomock import MongoClient
from server import app as flask_app
from db import MongoDBConnection


@pytest.fixture(scope="function")
def mongo_mock():
    MongoDBConnection.client = MongoClient()
    yield
    MongoDBConnection.client = None


@pytest.fixture
def app():
    flask_app.config.update(
        {
            "TESTING": True,
        }
    )
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello World!" in response.data


def test_create_film(client, mongo_mock):
    film_data = {
        "title": "A New Hope",
        "episode_id": 4,
        "director": "George Lucas",
        "producer": ["Gary Kurtz", "Rick McCallum"],
        "release_date": "1977-05-25",
        "planets": ["Tatooine", "Alderaan"],
    }
    response = client.post("/films", json=film_data)
    assert response.status_code == 201
    data = response.get_json()
    assert "Film created successfully!" in data["message"]


def test_update_film(client, mongo_mock):
    film_data = {
        "title": "A Old Hope",
        "episode_id": 4,
        "director": "Georgi Lucas",
        "producer": ["Gary Kurtz", "Rick McCallum"],
        "release_date": "1977-05-25",
        "planets": ["Tatooine", "Alderaan"],
    }
    film_id = MongoDBConnection.films().insert_one(film_data).inserted_id
    film_data["title"] = "A New Hope"
    film_data["director"] = "Lucas Jorge"
    response = client.put(f"/films/{film_id}", json=film_data)
    assert response.status_code == 200
    data = response.get_json()
    assert "Film updated successfully!" in data["message"]

    response_list = client.get("/films")
    data = response_list.get_json()
    assert data["films"][0]["title"] == "A New Hope"
    assert data["films"][0]["director"] == "Lucas Jorge"


def test_update_film_raise(client, mongo_mock):
    film_id = "5" * 24
    film_data = {
        "title": "A Old Hope",
        "episode_id": 4,
        "director": "Georgi Lucas",
        "producer": ["Gary Kurtz", "Rick McCallum"],
        "release_date": "1977-05-25",
        "planets": ["Tatooine", "Alderaan"],
    }
    response = client.put(f"/films/{film_id}", json=film_data)
    assert response.status_code == 404


def test_list_films(client, mongo_mock):
    response = client.get("/films")
    assert response.status_code == 200
    data = response.get_json()
    assert "films" in data


def test_list_many_films(client, mongo_mock):
    film_data_one = {
        "title": "A New Hope",
        "episode_id": 4,
        "director": "George Lucas",
        "producer": ["Gary Kurtz", "Rick McCallum"],
        "release_date": "1977-05-25",
        "planets": ["Tatooine", "Alderaan"],
    }
    film_data_two = {
        "title": "Star Wars: Episode I – The Phantom Menace",
        "episode_id": 1,
        "director": "George Lucas",
        "producer": ["Rick McCallum"],
        "release_date": "1999-05-19",
        "planets": ["Naboo"],
    }
    MongoDBConnection.films().insert_many([film_data_one, film_data_two])
    response = client.get("/films")
    assert response.status_code == 200
    data = response.get_json()
    assert "films" in data
    assert len(data["films"]) == 2


def test_list_films_filters(client, mongo_mock):
    film_data_one = {
        "title": "A New Hope",
        "episode_id": 4,
        "director": "George Lucas",
        "producer": ["Gary Kurtz", "Rick McCallum"],
        "release_date": "1977-05-25",
        "planets": ["Tatooine", "Alderaan"],
    }
    film_data_two = {
        "title": "Star Wars: Episode I – The Phantom Menace",
        "episode_id": 1,
        "director": "George Lucas",
        "producer": ["Rick McCallum"],
        "release_date": "1999-05-19",
        "planets": ["Naboo"],
    }
    MongoDBConnection.films().insert_many([film_data_one, film_data_two])
    response = client.get("/films?title=New&director=George&order_by=episode_id")
    assert response.status_code == 200
    data = response.get_json()
    assert "films" in data
    assert len(data["films"]) == 1


def test_list_films_filters_order_by(client, mongo_mock):
    film_data_one = {
        "title": "A New Hope",
        "episode_id": 4,
        "director": "George Lucas",
        "producer": ["Gary Kurtz", "Rick McCallum"],
        "release_date": "1977-05-25",
        "planets": ["Tatooine", "Alderaan"],
    }
    film_data_two = {
        "title": "Star Wars: Episode I – The Phantom Menace",
        "episode_id": 1,
        "director": "George Lucas",
        "producer": ["Rick McCallum"],
        "release_date": "1999-05-19",
        "planets": ["Naboo"],
    }
    MongoDBConnection.films().insert_many([film_data_one, film_data_two])
    response = client.get("/films?director=George&order_by=-episode_id")
    assert response.status_code == 200
    data = response.get_json()
    assert "films" in data
    assert len(data["films"]) == 2
    assert data["films"][0]["episode_id"] == 4


def test_list_films_pages(client, mongo_mock):
    film_data_one = {
        "title": "A New Hope",
        "episode_id": 4,
        "director": "George Lucas",
        "producer": ["Gary Kurtz", "Rick McCallum"],
        "release_date": "1977-05-25",
        "planets": ["Tatooine", "Alderaan"],
    }
    film_data_two = {
        "title": "Star Wars: Episode I – The Phantom Menace",
        "episode_id": 1,
        "director": "George Lucas",
        "producer": ["Rick McCallum"],
        "release_date": "1999-05-19",
        "planets": ["Naboo"],
    }
    MongoDBConnection.films().insert_many([film_data_one, film_data_two])
    response = client.get("/films?page_size=1&order_by=episode_id")
    assert response.status_code == 200
    data = response.get_json()
    assert "films" in data
    assert len(data["films"]) == 1
    assert data["films"][0]["title"] == "Star Wars: Episode I – The Phantom Menace"

    response = client.get("/films?page_size=1&page=2&order_by=episode_id")
    assert response.status_code == 200
    data = response.get_json()
    assert "films" in data
    assert len(data["films"]) == 1
    assert data["films"][0]["title"] == "A New Hope"


def test_list_films_filters_planet(client, mongo_mock):
    film_data_one = {
        "title": "A New Hope",
        "episode_id": 4,
        "director": "George Lucas",
        "producer": ["Gary Kurtz", "Rick McCallum"],
        "release_date": "1977-05-25",
        "planets": ["Tatooine", "Alderaan"],
    }
    film_data_two = {
        "title": "Star Wars: Episode I – The Phantom Menace",
        "episode_id": 1,
        "director": "George Lucas",
        "producer": ["Rick McCallum"],
        "release_date": "1999-05-19",
        "planets": ["Naboo", "Tatooine"],
    }
    MongoDBConnection.films().insert_many([film_data_one, film_data_two])
    response = client.get("/films?planet=Tatooine")
    assert response.status_code == 200
    data = response.get_json()
    assert "films" in data
    assert len(data["films"]) == 2
    response = client.get("/films?planet=Alderaan")
    data = response.get_json()
    assert len(data["films"]) == 1


def test_create_planet(client, mongo_mock):
    planet_data = {
        "name": "Tatooine",
        "rotation_period": "23",
        "orbital_period": "304",
        "diameter": "10465",
        "climate": "arid",
        "gravity": "1 standard",
        "terrain": "desert",
        "surface_water": "1",
        "population": "200000",
        "residents": [
            "Luke Skywalker",
            "C-3PO",
            "Darth Vader",
            "Owen Lars",
            "Beru Whitesun lars",
            "R5-D4",
            "Biggs Darklighter",
            "Anakin Skywalker",
            "Shmi Skywalker",
            "Cliegg Lars",
        ],
        "films": [
            "A New Hope",
            "Return of the Jedi",
            "The Phantom Menace",
            "Attack of the Clones",
            "Revenge of the Sith",
        ],
    }
    response = client.post("/planets", json=planet_data)
    assert response.status_code == 201
    data = response.get_json()
    assert "Planet created successfully!" in data["message"]


def test_update_planet(client, mongo_mock):
    planet_data = {
        "name": "Naboo",
        "rotation_period": "26",
        "orbital_period": "312",
        "diameter": "12120",
        "climate": "temperate",
        "gravity": "1 standard",
        "terrain": "grassy hills, swamps, forests, mountains",
        "surface_water": "12",
        "population": "4500000000",
        "residents": [
            "Padmé Amidala",
            "Jar Jar Binks",
            "Boss Nass",
            "Captain Tarpals",
            "Ric Olié",
            "Qui-Gon Jinn",
            "Obi-Wan Kenobi",
            "Anakin Skywalker",
            "Shmi Skywalker",
            "Senator Palpatine",
        ],
        "films": [
            "The Phantom Menace",
            "Attack of the Clones",
            "" "The Clone Wars",
            "Revenge of the Sith",
        ],
    }

    planet_id = MongoDBConnection.planets().insert_one(planet_data).inserted_id

    response_list = client.get("/planets")
    data = response_list.get_json()
    assert data["planets"][0]["_id"] == str(planet_id)
    assert data["planets"][0]["name"] == "Naboo"
    assert data["planets"][0]["climate"] == "temperate"
    assert data["planets"][0]["gravity"] == "1 standard"
    planet_data["climate"] = "rainforest"
    planet_data["gravity"] = "2 standard"
    response = client.put(f"/planets/{planet_id}", json=planet_data)
    assert response.status_code == 200
    data = response.get_json()
    assert "Planet updated successfully!" in data["message"]

    response_list = client.get("/planets")
    data = response_list.get_json()
    assert data["planets"][0]["_id"] == str(planet_id)
    assert data["planets"][0]["name"] == "Naboo"
    assert data["planets"][0]["climate"] == "rainforest"
    assert data["planets"][0]["gravity"] == "2 standard"


def test_list_planets(client, mongo_mock):
    response = client.get("/planets")
    assert response.status_code == 200
    data = response.get_json()
    assert "planets" in data


def test_list_many_planets(client, mongo_mock):
    planet_one = {
        "name": "Naboo",
        "rotation_period": "26",
        "orbital_period": "312",
        "diameter": "12120",
        "climate": "temperate",
        "gravity": "1 standard",
        "terrain": "grassy hills, swamps, forests, mountains",
        "surface_water": "12",
        "population": "4500000000",
        "residents": [],
        "films": [
            "The Phantom Menace",
            "Attack of the Clones",
            "The Clone Wars",
            "Revenge of the Sith",
        ],
    }
    planet_two = {
        "name": "Tatooine",
        "rotation_period": "23",
        "orbital_period": "304",
        "diameter": "10465",
        "climate": "arid",
        "gravity": "1 standard",
        "terrain": "desert",
        "surface_water": "1",
        "population": "200000",
        "residents": [],
        "films": [
            "A New Hope",
            "Return of the Jedi",
            "The Phantom Menace",
            "Attack of the Clones",
            "Revenge of the Sith",
        ],
    }
    MongoDBConnection.planets().insert_many([planet_one, planet_two])
    response = client.get("/planets")
    assert response.status_code == 200
    data = response.get_json()
    assert "planets" in data
    assert len(data["planets"]) == 2


def test_list_planets_filters(client, mongo_mock):
    planet_one = {
        "name": "Naboo",
        "rotation_period": "26",
        "orbital_period": "312",
        "diameter": "12120",
        "climate": "temperate",
        "gravity": "1 standard",
        "terrain": "grassy hills, swamps, forests, mountains",
        "surface_water": "12",
        "population": "4500000000",
        "residents": [],
        "films": [
            "The Phantom Menace",
            "Attack of the Clones",
            "The Clone Wars",
            "Revenge of the Sith",
        ],
    }
    planet_two = {
        "name": "Tatooine",
        "rotation_period": "23",
        "orbital_period": "304",
        "diameter": "10465",
        "climate": "arid",
        "gravity": "1 standard",
        "terrain": "desert",
        "surface_water": "1",
        "population": "200000",
        "residents": [],
        "films": [
            "A New Hope",
            "Return of the Jedi",
            "The Phantom Menace",
            "Attack of the Clones",
            "Revenge of the Sith",
        ],
    }
    MongoDBConnection.planets().insert_many([planet_one, planet_two])
    response = client.get("/planets?name=naboo")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["planets"]) == 1


def test_list_planets_filters_order_by(client, mongo_mock):
    planet_one = {
        "name": "Naboo",
        "rotation_period": "26",
        "orbital_period": "312",
        "diameter": "12120",
        "climate": "temperate",
        "gravity": "1 standard",
        "terrain": "grassy hills, swamps, forests, mountains",
        "surface_water": "12",
        "population": "4500000000",
        "residents": [],
        "films": [
            "The Phantom Menace",
            "Attack of the Clones",
            "The Clone Wars",
            "Revenge of the Sith",
        ],
    }
    planet_two = {
        "name": "Tatooine",
        "rotation_period": "23",
        "orbital_period": "304",
        "diameter": "10465",
        "climate": "arid",
        "gravity": "1 standard",
        "terrain": "desert",
        "surface_water": "1",
        "population": "200000",
        "residents": [],
        "films": [
            "A New Hope",
            "Return of the Jedi",
            "The Phantom Menace",
            "Attack of the Clones",
            "Revenge of the Sith",
        ],
    }
    MongoDBConnection.planets().insert_many([planet_one, planet_two])
    response = client.get("/planets?order_by=-rotation_period")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["planets"]) == 2
    assert data["planets"][0]["name"] == "Naboo"


def test_list_planets_pages(client, mongo_mock):
    planet_one = {
        "name": "Naboo",
        "rotation_period": "26",
        "orbital_period": "312",
        "diameter": "12120",
        "climate": "temperate",
        "gravity": "1 standard",
        "terrain": "grassy hills, swamps, forests, mountains",
        "surface_water": "12",
        "population": "4500000000",
        "residents": [],
        "films": [
            "The Phantom Menace",
            "Attack of the Clones",
            "The Clone Wars",
            "Revenge of the Sith",
        ],
    }
    planet_two = {
        "name": "Tatooine",
        "rotation_period": "23",
        "orbital_period": "304",
        "diameter": "10465",
        "climate": "arid",
        "gravity": "1 standard",
        "terrain": "desert",
        "surface_water": "1",
        "population": "200000",
        "residents": [],
        "films": [
            "A New Hope",
            "Return of the Jedi",
            "The Phantom Menace",
            "Attack of the Clones",
            "Revenge of the Sith",
        ],
    }
    MongoDBConnection.planets().insert_many([planet_one, planet_two])
    response = client.get("/planets?page_size=1&page=2")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["planets"]) == 1


def test_list_planets_filters_films(client, mongo_mock):
    planet_one = {
        "name": "Naboo",
        "rotation_period": "26",
        "orbital_period": "312",
        "diameter": "12120",
        "climate": "temperate",
        "gravity": "1 standard",
        "terrain": "grassy hills, swamps, forests, mountains",
        "surface_water": "12",
        "population": "4500000000",
        "residents": [],
        "films": [
            "The Phantom Menace",
            "Attack of the Clones",
            "The Clone Wars",
            "Revenge of the Sith",
        ],
    }
    planet_two = {
        "name": "Tatooine",
        "rotation_period": "23",
        "orbital_period": "304",
        "diameter": "10465",
        "climate": "arid",
        "gravity": "1 standard",
        "terrain": "desert",
        "surface_water": "1",
        "population": "200000",
        "residents": [],
        "films": [
            "A New Hope",
            "Return of the Jedi",
            "The Phantom Menace",
            "Attack of the Clones",
            "Revenge of the Sith",
        ],
    }
    MongoDBConnection.planets().insert_many([planet_one, planet_two])
    response = client.get("/planets?film=The%20Phantom%20Menace")
    assert response.status_code == 200
    data = response.get_json()
    assert "planets" in data
    assert len(data["planets"]) == 2
    response = client.get("/planets?film=A%20new%20hope")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["planets"]) == 1
    assert data["planets"][0]["name"] == "Tatooine"

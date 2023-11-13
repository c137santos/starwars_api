from datetime import datetime
import freezegun
from server import app as flask_app
from db import MongoDBConnection


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


def test_update_planet_raise(client, mongo_mock):
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

    planet_id = "5" * 24
    response = client.put(f"/planets/{planet_id}", json=planet_data)
    assert response.status_code == 404


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


def test_list_planets_filters_planet_name(client, mongo_mock):
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


def test_list_planets_filters_planet_name_residents(client, mongo_mock):
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
    MongoDBConnection.planets().insert_many([planet_one, planet_two])
    response = client.get("/planets?resident=luke%20skywalker")
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


def test_delete_planets(client, mongo_mock):
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
    id_planet = MongoDBConnection.planets().insert_one(planet_data).inserted_id
    response = client.delete(f"/planets/{id_planet}")
    assert response.status_code == 200
    data = response.get_json()
    assert "Planet deleted successfully!" in data["message"]


def test_delete_planets_error(client, mongo_mock):
    id_planet = "5" * 24
    response = client.delete(f"/planets/{id_planet}")
    assert response.status_code == 404


def test_update_planet_date(client, mongo_mock):
    with freezegun.freeze_time("1999-01-01 12:00:00"):
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
            "created": datetime(1999, 1, 1, 12, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
        }
        planet_id = MongoDBConnection.planets().insert_one(planet_data).inserted_id

    with freezegun.freeze_time("2023-01-02 12:00:00"):
        planet_data["name"] = "Naboo"
        planet_data["climate"] = "temperate"
        response = client.put(f"/planets/{planet_id}", json=planet_data)

    assert response.status_code == 200
    data = response.get_json()
    assert "Planet updated successfully!" in data["message"]

    response_list = client.get("/planets")
    data = response_list.get_json()

    created_datetime = data["planets"][0]["created"]
    assert created_datetime == datetime(1999, 1, 1, 12, 0, 0).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    updated_datetime = data["planets"][0]["last_updated"]
    assert updated_datetime == datetime(2023, 1, 2, 12, 0, 0).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    assert data["planets"][0]["name"] == "Naboo"
    assert data["planets"][0]["climate"] == "temperate"

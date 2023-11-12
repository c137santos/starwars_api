from server import app as flask_app
from db import MongoDBConnection


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


def test_delete_film(client, mongo_mock):
    film_data_one = {
        "title": "A New Hope",
        "episode_id": 4,
        "director": "George Lucas",
        "producer": ["Gary Kurtz", "Rick McCallum"],
        "release_date": "1977-05-25",
        "planets": ["Tatooine", "Alderaan"],
    }

    id_film = MongoDBConnection.films().insert_one(film_data_one).inserted_id
    response = client.delete(f"/films/{id_film}")
    assert response.status_code == 200
    data = response.get_json()
    assert "Film deleted successfully!" in data["message"]


def test_delete_film_error(client, mongo_mock):
    id_film = "5" * 24
    response = client.delete(f"/films/{id_film}")
    assert response.status_code == 404

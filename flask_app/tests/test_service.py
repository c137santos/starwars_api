import mongomock
import pytest

from service import FilmService
from db import MongoDBConnection


# Configuração do banco de dados mock
@pytest.fixture(scope="function")
def mongo_mock():
    MongoDBConnection.client = mongomock.MongoClient()
    yield
    MongoDBConnection.client = None


def test_create_film(mongo_mock):
    # Dados do filme para teste
    film_data = {
        "title": "Test Film",
        "episode_id": 1,
        "director": "Test Director",
        "producer": ["Test Producer"],
        "release_date": "2023-01-01",
        "planets": ["Earth"],
    }

    # Criar o filme
    film_id = FilmService.create(film_data)
    assert film_id is not None

    # Buscar o filme criado
    created_film = MongoDBConnection.films().find_one({"_id": film_id})
    assert created_film is not None
    assert created_film["title"] == "Test Film"


def test_update_film(mongo_mock):
    # Criar um filme para atualizar
    film_data = {
        "title": "Old Title",
        "episode_id": 2,
        "director": "Test Director",
        "producer": ["Test Producer"],
        "release_date": "2023-01-02",
        "planets": ["Mars"],
    }
    film_id = MongoDBConnection.films().insert_one(film_data).inserted_id

    # Atualizar o filme
    update_data = {"title": "New Title"}
    FilmService.update(str(film_id), update_data)

    # Buscar o filme atualizado
    updated_film = MongoDBConnection.films().find_one({"_id": film_id})
    assert updated_film["title"] == "New Title"


def test_list_films(mongo_mock):
    # Inserir dados de teste
    film_data_1 = {"title": "Film One", "episode_id": 1, "director": "Director One"}
    film_data_2 = {"title": "Film Two", "episode_id": 2, "director": "Director Two"}
    MongoDBConnection.films().insert_many([film_data_1, film_data_2])

    # Listar filmes sem filtro
    films = FilmService.list()
    assert len(films) == 2

    # Listar filmes com filtro
    filtered_films = FilmService.list(**{"title": "Film One"})
    assert len(filtered_films) == 1
    assert filtered_films[0]["title"] == "Film One"


def test_list_films_order_by(mongo_mock):
    # Inserir dados de teste
    film_data_1 = {"title": "Film One", "episode_id": 1, "director": "Director One"}
    film_data_2 = {"title": "Film Two", "episode_id": 2, "director": "Director Two"}
    MongoDBConnection.films().insert_many([film_data_1, film_data_2])

    filtered_films = FilmService.list(**{"order_by": "episode_id"})
    assert len(filtered_films) == 2
    assert filtered_films[0]["title"] == "Film One"

    filtered_films = FilmService.list(**{"order_by": "-episode_id"})
    assert len(filtered_films) == 2
    assert filtered_films[0]["title"] == "Film Two"

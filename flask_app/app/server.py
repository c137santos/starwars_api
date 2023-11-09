from datetime import datetime
from bson import ObjectId
from flask import Flask, request, jsonify
from flask.json.provider import DefaultJSONProvider
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request

from models import Error, Film, FilmsResponse, FilmFilter, Message
from service import FilmService


class MongoJsonProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


app = Flask(__name__)
app.json = MongoJsonProvider(app)
spec = FlaskPydanticSpec("flask", title="Demo API", version="v1")
spec.register(app)


@app.get("/")
@spec.validate(resp=Response(HTTP_200=Message))
def home():
    return jsonify({"message": "Hello World!"}), 200


@app.post("/films")
@spec.validate(body=Request(Film), resp=Response(HTTP_201=Message))
def create_film():
    film_data = request.context.body.dict()
    film_id = FilmService.create(film_data)
    return (
        jsonify({"message": "Film created successfully!", "film_id": film_id}),
        201,
    )


@app.put("/films/<film_id>")
@spec.validate(body=Request(Film), resp=Response(HTTP_200=Message, HTTP_404=Error))
def edit_film(film_id):
    film_data = request.context.body.dict()
    try:
        FilmService.update(film_id, film_data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    return jsonify({"message": "Film updated successfully!"}), 200


@app.get("/films")
@spec.validate(
    query=FilmFilter,
    resp=Response(HTTP_200=FilmsResponse),
)
def list_films():
    return (
        jsonify(
            {
                "films": FilmService.list(
                    title=request.context.query.title,
                    director=request.context.query.director,
                    order_by=request.context.query.order_by,
                    page=request.context.query.page,
                    page_size=request.context.query.page_size,
                )
            }
        ),
        200,
    )


@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify(error=str(e)), 500


@app.post("/planet")
@spec.validate(body=Request(Film), resp=Response(HTTP_201=Message))
def create_planet():
    planet_data = request.context.body.dict()
    film_id = FilmService.create(planet_data)
    return (
        jsonify({"message": "Film created successfully!", "film_id": film_id}),
        201,
    )


if __name__ == "__main__":
    app.run(debug=True)

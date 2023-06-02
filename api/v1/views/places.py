from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from flask import jsonify, abort, request


@app_views.route("/cities/<city_id>/places")
def places(city_id):
    """Get all places in a city

    Args:
        city_id (str): ID of the City

    Returns:
        list: All the places in that city

    Raises:
        404: If the specified city_id does not exist
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    result = []

    for place in city.places:
        result.append(place.to_dict())

    return jsonify(result)


@app_views.route("/places/<place_id>")
def place(place_id):
    """Get a place

    Args:
        place_id (str): ID of the place

    Returns:
        dict: Place JSON
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())

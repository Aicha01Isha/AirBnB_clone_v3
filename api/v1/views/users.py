from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route("/users")
def users():
    """Get all users

    Returns:
        list: All the users
    """
    users = storage.all(User)
    result = []

    for user in users.values():
        result.append(user.to_dict())

    return jsonify(result)


@app_views.route("/users/<user_id>")
def one_user(user_id):
    """Get one user

    Args:
        user_id (str): ID of the user

    Returns:
        dict: The user in JSON
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    user.delete()
    storage.save()

    return jsonify({})


@app_views.route("/users", methods=["POST"])
def create_user():
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    if "email" not in payload:
        abort(400, "Missing email")
    if "password" not in payload:
        abort(400, "Missing password")

    user = User(**payload)
    user.save()

    return jsonify(user.to_dict()), 201
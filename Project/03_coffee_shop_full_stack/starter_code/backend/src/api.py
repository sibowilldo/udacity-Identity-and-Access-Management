import os
from flask import Flask, request, jsonify
from sqlalchemy import exc
import json
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import Forbidden, Unauthorized, BadRequest

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
from dotenv import load_dotenv

load_dotenv('../.env')

app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

base_api_route = os.getenv("BASE_API_URL", "/api/v1")

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''


# db_drop_and_create_all()

# ROUTES

'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route(f"{base_api_route}/drinks", methods=['GET'])
def get_all_drinks():
    try:
        drinks = Drink.query.all()
        drinks = list(map(lambda drink: drink.short(), drinks))
        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200
    except Exception as ex:
        return jsonify({
            "success": False,
            "message": str(ex.__dict__['orig'])
        }), 500


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route(f"{base_api_route}/drinks-detail", methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details(payload):
    try:
        drinks = Drink.query.all()
        drinks = list(map(lambda drink: drink.long(), drinks))
        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200
    except Forbidden or Unauthorized or BadRequest:
        raise AuthError


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route(f"{base_api_route}/drinks", methods=['POST'])
@requires_auth('post:drinks')
def post_new_drink(payload):
    try:
        req = request.get_json()
        drink = Drink()

        drink.title = req.get("title", "")
        drink.recipe = json.dumps(req.get("recipe"))

        drink.insert()
        return jsonify({
            "success": True,
            "drinks": drink.long()
        }), 200
    except Forbidden or Unauthorized or BadRequest:
        raise AuthError


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route(f"{base_api_route}/drinks/<int:drink_id>", methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink_details(payload, drink_id):
    try:
        req = request.get_json()
        drink = Drink.query.filter(Drink.id == drink_id).first_or_404()

        drink.title = req.get('title')
        # Only update the recipe field, if recipe data was passed
        if req.get('recipe') is not None:
            drink.recipe = json.dumps(req.get('recipe'))

        drink.update()
        return jsonify({
            "success": True,
            "drinks": drink.long()
        }), 200
    except Forbidden or Unauthorized or BadRequest:
        raise AuthError


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id}
        where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route(f"{base_api_route}/drinks/<int:drink_id>", methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    try:
        drink = Drink.query.filter(Drink.id == drink_id).first_or_404()
        drink.delete()
        return jsonify({
            "success": True,
            "delete": drink_id
        }), 200
    except Forbidden or Unauthorized or BadRequest:
        raise AuthError


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with appropriate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.error['code'],
        "message": error.error['description']
    }), error.status_code

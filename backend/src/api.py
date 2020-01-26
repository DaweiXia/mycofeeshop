import os, operator
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# db_drop_and_create_all()

# ROUTES
@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    drinks_short = [drink.short() for drink in drinks]
    return jsonify({'success': True, 'drinks': drinks_short})


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def drinks_detail(payload):
    drinks = Drink.query.all()
    drinks_long = [drink.long() for drink in drinks]
    return jsonify({'success': True, 'drinks': drinks_long})


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    data = request.json
    drink = Drink(title=data['title'], recipe=json.dumps(data['recipe']))
    try:
        drink.insert()
        return jsonify({
                        'success': True,
                        'drinks': [drink.short() for drink in Drink.query.all()]})
    except:
        db.session.rollback()
        abort(422)


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(payload, id):
    data = request.json
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink:
        if drink.title != data['title']:
            drink.title = data['title']
        patch_recipe = json.dumps(data['recipe'])
        if not operator.eq(drink.recipe, patch_recipe):
            drink.recipe = patch_recipe
        try:
            drink.update()
            return jsonify({'success': True})
        except:
            db.session.rollback()
            abort(422)
    else:
        abort(404)


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink:
        try:
            drink.delete()
            return jsonify({'success': True})
        except:
            db.session.rollback()
            abort(422)
    else:
        abort(404)


# Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404


@app.errorhandler(401)
def invalid_header(error):
    return jsonify({
                    "success": False,
                    "error": 401,
                    "message": "Invalid header!"
                    }), 401


@app.errorhandler(405)
def permission_error(error):
    return jsonify({
                    "success": False,
                    "error": 405,
                    "message": "Permission not found!"
                    }), 405

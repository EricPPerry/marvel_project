from functools import wraps
import secrets

from flask import request, jsonify
from marvel_collection.models import Character, User

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
        
        if not token:
            return jsonify({"message":"Uh oh, token is missing"}), 401
        
        try:
            current_user_token = User.query.filter_by(token = token).first()

        except:
            owner = User.query.filter_by(token = token).first()
            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({"message":"Woohoo, token is valid."})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated

import decimal
from flask import json

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)
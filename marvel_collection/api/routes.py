from flask import Blueprint, request, jsonify
from marvel_collection.helpers import token_required
from marvel_collection.models import User, Character, CharacterSchema, characters_schema, db, character_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some':'value'}


#Using API to create a character
@api.route('/characters', methods = ['POST'])
@token_required
def create_character(current_user_token):
    character_name = request.json['character_name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    user_token = current_user_token.token

    character = Character(character_name, description, comics_appeared_in, super_power, user_token = user_token)

    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)

#Retrieving ALL characters tied to a user's id at once
@api.route('/characters', methods = ['GET'])
@token_required
def get_characters(current_user_token):
    owner = current_user_token.token
    characters = Character.query.filter_by(user_token = owner).all()
    response = characters_schema.dump(characters)
    return jsonify(response)


#Retrieve only ONE character, by its id value
@api.route('/characters/<id>', methods = ['GET'])
@token_required
def get_character(current_user_token, id):
    character = Character.query.get(id)
    response = character_schema.dump(character)
    return jsonify(response)

#Update specific character endpoint in API with new value (by id)
@api.route('/characters/<id>', methods = ['POST', 'PUT'])
@token_required
def update_character(current_user_token, id):
    character = Character.query.get(id)

    character.character_name = request.json['character_name']
    character.description = request.json['description']
    character.comics_appeared_in = request.json['comics_appeared_in']
    character.super_power = request.json['super_power']
    character.user_token = current_user_token.token

    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)


#Deleting a specific character endpoint from the API

@api.route('/characters/<id>', methods = ['DELETE'])
@token_required
def delete_character(current_user_token, id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)
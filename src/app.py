"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET','POST'])
def handle_members():
    response_body = {}
    if request.method == 'GET':
        # this is how you can use the Family datastructure by calling its methods
        members = jackson_family.get_all_members()
        response_body['message'] = 'Encontrado'
        response_body['results'] = members
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        print(data)
        jackson_family.add_member(data)
        members = jackson_family.get_all_members()
        response_body['message'] = 'Recibido'
        response_body['results'] = members
        return response_body, 200

@app.route('/members/<int:id_member>', methods=['GET', 'DELETE', 'PUT'])
def handle_member(id_member):
    response_body = {}
    if request.method == 'GET':
        member = jackson_family.get_member(id_member)
        if member:
            response_body['message'] = 'Encontrado'
            response_body['results'] = member
            return response_body, 200
        response_body['message'] = 'No encontrado'
        response_body['results'] = []  
        return response_body, 400
    if request.method == 'DELETE':
        member = jackson_family.delete_member(id_member)
        if member:
            response_body['message'] = 'Eliminado'
            response_body['results'] = member
            return response_body, 200
        response_body['message'] = 'No encontrado'
        response_body['results'] = []  
        return response_body, 400
    if request.method == 'PUT':
        data = request.json
        jackson_family.modify_member(data, id_member)
        member = jackson_family.get_member(id_member)
        response_body['message'] = 'Modificado'
        response_body['results'] = member
        return response_body, 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

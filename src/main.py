"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Skill, Experience, Project
#from models import Person
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
# Setup the Flask-JWT-Simple extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

# Provide a method to create access tokens. The create_jwt()
# function is used to actually generate the token
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)

    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    usercheck = User.query.filter_by(email=email, password=password).first()
    if usercheck == None:
        return jsonify({"msg": "Bad email or password"}), 401


 # Identity can be any data that is json serializable
    user = {
        'access_token': create_access_token(identity=email),
        'user_info': usercheck.serialize()
    }
    return jsonify(user), 200

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    all_people = User.query.all()
    all_people = list(map(lambda x: x.serialize(), all_people))
    return jsonify(all_people), 200

@app.route('/skill', methods=['GET'])
def handle_skills():
    all_skills = Skill.query.all()
    all_skills = list(map(lambda x: x.serialize(), all_skills))
    return jsonify(all_skills), 200

@app.route('/experience', methods=['GET'])
def handle_exps():
    all_exps = Experience.query.all()
    all_exps = list(map(lambda x: x.serialize(), all_exps))
    return jsonify(all_exps), 200

@app.route('/project', methods=['GET'])
def handle_projects():
    all_projects = Project.query.all()
    all_projects = list(map(lambda x: x.serialize(), all_projects))
    return jsonify(all_projects), 200


@app.route('/user', methods=['POST'])
def handle_person():
    """
    Create person and retrieve all persons
    """
    # POST request
   
    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'username' not in body:
        raise APIException('You need to specify the username', status_code=400)
    if 'email' not in body:
        raise APIException('You need to specify the email', status_code=400)
    if 'password' not in body:
        raise APIException('You need to specify the password', status_code=400)    
    user1 = User(username=body['username'], email=body['email'], password=body['password'], is_active=body['is_active'])
    db.session.add(user1)
    db.session.commit()
    return "ok", 200

@app.route('/user/<int:user_id>', methods=['GET', 'PUT'])
# @jwt_required
def get_single_person(user_id):
    """
    Single person
    """
    body = request.get_json() #{ 'username': 'new_username'}
    if request.method == 'PUT':
        user1 = User.query.get(user_id)
        user1.username = body["username"]
        user1.email = body["email"]
        db.session.commit()
        return jsonify(user1.serialize()), 200
    
    if request.method == 'GET':
        user1 = User.query.get(user_id)
        return jsonify(user1.serialize()), 200

    return "Invalid Method", 404

@app.route('/skill', methods=['POST'])
def handle_skill():
    """
    Create person and retrieve all persons
    """
    # POST request
   
    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)    
    skill1 = Skill(skill_type=body['skill_type'], user_id=body['user_id'])
    db.session.add(skill1)
    db.session.commit()
    return "ok", 200

@app.route('/experience', methods=['POST'])
def handle_exp():
    """
    Create person and retrieve all persons
    """
    # POST request
   
    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)    
    exp1 = Experience(company=body['company'], position=body['position'], description=body['description'] , user_id=body['user_id'])
    db.session.add(exp1)
    db.session.commit()
    return "ok", 200

@app.route('/project', methods=['POST'])
def handle_project():
    """
    Create person and retrieve all persons
    """
    # POST request
   
    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)    
    project1 = Project(project_name=body['project_name'], project_description=body['project_description'], user_id=body['user_id'])
    db.session.add(project1)
    db.session.commit()
    return "ok", 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

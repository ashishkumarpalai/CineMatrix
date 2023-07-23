import os


from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
from flask_cors import CORS
from bson import json_util

# Load environment variables from .env
load_dotenv()


app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.route("/")
def get():
    return '<h1 style="color:blue;text-align:center">Wellcome To cinematrix Backend</h1>'
    

# ==============================================get all users ==============================================
@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    result = []
    for user in users:
        result.append({
            '_id': str(user['_id']),
            'name':user['name'],
            'username': user['username'],
            'user_status': user['user_status'],
            'gender': user['gender'],
            'membership_type': user['membership_type'],
            'bio': user['bio'],
            'date_of_birth': user['date_of_birth']
        })
    return jsonify(result), 200



# =================================get by id ============================

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user:
        result = {
            'name':user['name'],
            'id': str(user['_id']),
            'username': user['username'],
            'user_status': user['user_status'],
            'gender': user['gender'],
            'membership_type': user['membership_type'],
            'bio': user['bio'],
            'date_of_birth': user['date_of_birth']
        }
        return jsonify(result), 200
    else:
        return jsonify({'message':'User not found'}), 404
    

# =============================user put ==============================

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.get_json()
    user = {
        'name':user_data['name'],
        'username': user_data['email'],
        'user_status': user_data['user_status'],
        'gender': user_data['gender'],
        'membership_type': user_data['membership_type'],
        'bio': user_data['bio'],
        'date_of_birth': user_data['date_of_birth']
    }
    result = mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': user})
    if result.modified_count > 0:
        return jsonify({'message':'User updated successfully'}), 200
    else:
        return jsonify({'message':'User not found'}), 404

# ================================== user delete=================================

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = mongo.db.users.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404
    

# ==============================================user register ==============================================

@app.route('/register', methods=['POST'])
def register():
    # Get user data from the JSON payload of the request
    name = request.json.get("name")
    username = request.json.get('email')
    password = bcrypt.generate_password_hash(request.json.get('password')).decode('utf-8')
    user_status = request.json.get('user_status')
    gender = request.json.get('gender')
    membership_type = request.json.get('membership_type')
    bio = request.json.get('bio')
    date_of_birth = request.json.get('date_of_birth')

    # Check if the username already exists in the database
    existing_user = mongo.db.users.find_one({'username': username})
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 409

    # Create a new user document
    user_data = {
        'name': name,
        'username': username,
        'password': password,
        'user_status': user_status,
        'gender': gender,
        'membership_type': membership_type,
        'bio': bio,
        'date_of_birth': date_of_birth
    }

    # Insert the user data into the 'users' collection
    user_id = mongo.db.users.insert_one(user_data).inserted_id
    return jsonify({'message': 'User registered successfully', 'user_id': str(user_id)}), 201

# ==============================================user logiin======================================
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('email')
    password = request.json.get('password')
    # Check if the username exists in the database
    user = mongo.db.users.find_one({'username': username})
    if not user:
        return jsonify({'message': 'Invalid username or password'}), 401
    # Check if the password is correct
    if bcrypt.check_password_hash(user['password'], password):
        access_token = create_access_token(identity=str(user['_id']))
        return jsonify({'message': 'Login successfully',"name":user['name'],'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401



# ==================================protected route if you have a tocken then you have acces it==============================================
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'user_id': current_user}), 200

# ***********************Movie route start**************************
class Movie:
    def __init__(self, title, description, genre,image):
        self.title = title
        self.description = description
        self.genre = genre
        self.image = image

class Show:
    def __init__(self, movie_id, timings, categories):
        self.movie_id = movie_id
        self.timings = timings
        self.categories = categories


# Event Model
class Event:
    def __init__(self, name, description, date):
        self.name = name
        self.description = description
        self.date = date


# Participant Model
class Participant:
    def __init__(self, name, email):
        self.name = name
        self.email = email

# ====================Get all movie =============================================
@app.route('/api/movies', methods=['GET'])
def get_movies():
    movies_list = list(mongo.db.movie.find())
    # return json_util.dumps(movies_list), 200
    result = []
    for movie in movies_list:
        result.append({
            '_id': str(movie['_id']),
            'title':movie['title'],
            'description': movie['description'],
            'genre': movie['genre'],
            'image':movie['image']
        })
    return jsonify(result), 200

# ====================get movie by movie_id==============================
@app.route('/api/movies/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    movies_list = mongo.db.movie.find_one({'_id': ObjectId(movie_id)})
    if movies_list:
        result={
            '_id': str(movies_list['_id']),
            'title':movies_list['title'],
            'description': movies_list['description'],
            'genre': movies_list['genre'],
            'image':movies_list['image']
        }
        return jsonify(result), 200
    else:
        return jsonify({'message': 'Movie not found'}), 404

# ============================movie added=============================
@app.route('/api/movies', methods=['POST'])
def create_movie():
    data = request.json
    title = data.get('title')
    
    if not title:
        return jsonify({'message': 'Movie title is required'}), 400

    # Check if the movie with the same title already exists
    existing_movie = mongo.db.movie.find_one({'title': title})
    if existing_movie:
        return jsonify({'message': 'Movie already exists'}), 409

    movie = Movie(data['title'], data['description'], data['genre'],data['image'])
    movie_id = mongo.db.movie.insert_one(movie.__dict__).inserted_id
    return jsonify({'message': 'Movie created', 'movie_id': str(movie_id)}), 201

# ================================Edit movie data ==========================
@app.route('/api/movies/<string:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    data = request.json
    movie = Movie(data['title'], data['description'], data['genre'],data['image'])
    result = mongo.db.movie.update_one({'_id': ObjectId(movie_id)}, {'$set': movie.__dict__})
    if result.modified_count > 0:
        return jsonify({'message': 'Movie updated'}), 200
    return jsonify({'message': 'Movie not found'}), 404


# ==============================Delete Movie Data==============================
@app.route('/api/movies/<string:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    result = mongo.db.movie.delete_one({'_id': ObjectId(movie_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Movie deleted'}), 200
    return jsonify({'message': 'Movie not found'}), 404

# # ************************Show CRUD operations for a specific Movie******************************

@app.route('/api/movies/<string:movie_id>/shows', methods=['GET'])
def get_shows_for_movie(movie_id):
    movie = mongo.db.movie.find_one({'_id': ObjectId(movie_id)})
    if movie:
        shows_list = list(mongo.db.shows.find({'movie_id': movie_id}))
        result = []
        for show in shows_list:
            result.append({
                '_id': str(show['_id']),
                'timings': show['timings'],
                'categories': show['categories']
            })
        return jsonify(result), 200
    return jsonify({'message': 'Movie not found'}), 404

# Route to create a new show for a movie
@app.route('/api/movies/<string:movie_id>/shows', methods=['POST'])
def create_show_for_movie(movie_id):
    movie = mongo.db.movie.find_one({'_id': ObjectId(movie_id)})
    if not movie:
        return jsonify({'message': 'Movie not found'}), 404

    data = request.json
    timings = data.get('timings', [])
    categories = data.get('categories', [])

    # Validate that timings and categories are lists
    if not isinstance(timings, list) or not isinstance(categories, list):
        return jsonify({'message': 'Timings and categories must be provided as arrays'}), 400

    # Create the Show document with the movie_id and other details
    show = Show(movie_id=movie_id, timings=timings, categories=categories)
    show_id = mongo.db.shows.insert_one(show.__dict__).inserted_id
    return jsonify({'message': 'Show created', 'show_id': str(show_id)}), 201

# Route to update a show for a movie
@app.route('/api/movies/<string:movie_id>/shows/<string:show_id>', methods=['PUT'])
def update_show_for_movie(movie_id, show_id):
    movie =mongo.db.movie.find_one({'_id': ObjectId(movie_id)})
    if not movie:
        return jsonify({'message': 'Movie not found'}), 404

    data = request.json
    timings = data.get('timings', [])
    categories = data.get('categories', [])

    # Validate that timings and categories are lists
    if not isinstance(timings, list) or not isinstance(categories, list):
        return jsonify({'message': 'Timings and categories must be provided as arrays'}), 400

    # Update the Show document with the new timings and categories
    result = mongo.db.shows.update_one({'_id': ObjectId(show_id), 'movie_id': movie_id},{'$set': {'timings': timings, 'categories': categories}})
    if result.modified_count > 0:
        return jsonify({'message': 'Show updated'}), 200
    return jsonify({'message': 'Show not found'}), 404

# Route to delete a show for a movie
@app.route('/api/movies/<string:movie_id>/shows/<string:show_id>', methods=['DELETE'])
def delete_show_for_movie(movie_id, show_id):
    movie = mongo.db.movie.find_one({'_id': ObjectId(movie_id)})
    if not movie:
        return jsonify({'message': 'Movie not found'}), 404

    result = mongo.db.shows.delete_one({'_id': ObjectId(show_id), 'movie_id': movie_id})
    if result.deleted_count > 0:
        return jsonify({'message': 'Show deleted'}), 200
    return jsonify({'message': 'Show not found'}), 404

# **************************************************Routes for Events***********************************************************

# ================================create events============================
@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.json
    event = Event(data['name'], data['description'], data['date'])
    event_id = mongo.db.event.insert_one(event.__dict__).inserted_id
    return jsonify({'message': 'Event created', 'event_id': str(event_id)}), 201

# ================================GET all events============================
@app.route('/api/events', methods=['GET'])
def get_events():
    events_list = list(mongo.db.event.find())
    result = []
    for event in events_list:
        result.append({
            '_id': str(event['_id']),
            'name': event['name'],
            'description': event['description'],
            'date': event['date']
        })
    return jsonify(result), 200

# ================================GET porticular  events============================
@app.route('/api/events/<string:event_id>', methods=['GET'])
def get_event(event_id):
    event = mongo.db.event.find_one({'_id': ObjectId(event_id)})
    if event:
        return jsonify({
            '_id': str(event['_id']),
            'name': event['name'],
            'description': event['description'],
            'date': event['date']
        }), 200
    return jsonify({'message': 'Event not found'}), 404

# ================================DELETE events============================
@app.route('/api/events/<string:event_id>', methods=['DELETE'])
def delete_event(event_id):
    result = mongo.db.event.delete_one({'_id': ObjectId(event_id)})
    if result.deleted_count > 0:
        # Delete the associated participant-event relationships
        mongo.db.event_participant.delete_many({'event_id': ObjectId(event_id)})
        return jsonify({'message': 'Event deleted'}), 200
    return jsonify({'message': 'Event not found'}), 404


# ***************************Routes for Participants**********************************************

# ================================create participants============================
@app.route('/api/participants', methods=['POST'])
def create_participant():
    data = request.json
    participant = Participant(data['name'], data['email'])
    participant_id = mongo.db.participant.insert_one(participant.__dict__).inserted_id
    return jsonify({'message': 'Participant created', 'participant_id': str(participant_id)}), 201

# ================================GET  participants============================
@app.route('/api/participants', methods=['GET'])
def get_participants():
    participants_list = list(mongo.db.participant.find())
    result = []
    for participant in participants_list:
        result.append({
            '_id': str(participant['_id']),
            'name': participant['name'],
            'email': participant['email']
        })
    return jsonify(result), 200

# ================================GET  porticular participants============================
@app.route('/api/participants/<string:participant_id>', methods=['GET'])
def get_participant(participant_id):
    participant = mongo.db.participant.find_one({'_id': ObjectId(participant_id)})
    if participant:
        return jsonify({
            '_id': str(participant['_id']),
            'name': participant['name'],
            'email': participant['email']
        }), 200
    return jsonify({'message': 'Participant not found'}), 404

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ================================DELETE   porticular participants============================
@app.route('/api/participants/<string:participant_id>', methods=['DELETE'])
def delete_participant(participant_id):
    result = mongo.db.participant.delete_one({'_id': ObjectId(participant_id)})
    if result.deleted_count > 0:
        # Delete the associated participant-event relationships
        mongo.db.event_participant_collection.delete_many({'participant_id': ObjectId(participant_id)})
        return jsonify({'message': 'Participant deleted'}), 200
    return jsonify({'message': 'Participant not found'}), 404


# Routes for Event-Participant Relationship

@app.route('/api/events/<string:event_id>/participants', methods=['POST'])
def register_participant_for_event(event_id):
    event = mongo.db.event.find_one({'_id': ObjectId(event_id)})
    if not event:
        return jsonify({'message': 'Event not found'}), 404

    data = request.json
    participant_id = data.get('participant_id')
    participant = mongo.db.participant.find_one({'_id': ObjectId(participant_id)})
    if not participant:
        return jsonify({'message': 'Participant not found'}), 404

    mongo.db.event_participant_collection.insert_one({'event_id': ObjectId(event_id), 'participant_id': ObjectId(participant_id)})
    return jsonify({'message': 'Participant registered for the event'}), 201


@app.route('/api/events/<string:event_id>/participants', methods=['GET'])
def get_participants_for_event(event_id):
    event = mongo.db.event.find_one({'_id': ObjectId(event_id)})
    if event:
        participants_list = list(mongo.db.event_participant_collection.find({'event_id': ObjectId(event_id)}))
        result = []
        for relationship in participants_list:
            participant_id = relationship['participant_id']
            participant = mongo.db.participant.find_one({'_id': participant_id})
            if participant:
                result.append({
                    '_id': str(participant['_id']),
                    'name': participant['name'],
                    'email': participant['email']
                })
        return jsonify(result), 200
    return jsonify({'message': 'Event not found'}), 404


@app.route('/api/participants/<string:participant_id>/events', methods=['GET'])
def get_events_for_participant(participant_id):
    participant = mongo.db.participant.find_one({'_id': ObjectId(participant_id)})
    if participant:
        events_list = list(mongo.db.event_participant_collection.find({'participant_id': ObjectId(participant_id)}))
        result = []
        for relationship in events_list:
            event_id = relationship['event_id']
            event = mongo.db.event.find_one({'_id': event_id})
            if event:
                result.append({
                    '_id': str(event['_id']),
                    'name': event['name'],
                    'description': event['description'],
                    'date': event['date']
                })
        return jsonify(result), 200
    return jsonify({'message': 'Participant not found'}), 404


@app.route('/api/events/<string:event_id>/participants/<string:participant_id>', methods=['DELETE'])
def delete_participant_from_event(event_id, participant_id):
    mongo.db.event_participant_collection.delete_one({'event_id': ObjectId(event_id), 'participant_id': ObjectId(participant_id)})
    return jsonify({'message': 'Participant removed from the event'}), 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
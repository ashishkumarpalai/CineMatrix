from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


app = Flask(__name__)
# app.config['MONGO_URI'] = 'mongodb+srv://ashish:ashish@cluster0.dsmyzjx.mongodb.net/cinematrix?retryWrites=true&w=majority'
# app.config['JWT_SECRET_KEY'] = 'ashish'
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.route("/")
def get():
    return "Wellcome cinematrix"
    

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
        return jsonify('User not found'), 404
    

# =============================user put ==============================

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.get_json()
    user = {
        'username': user_data['email'],
        'user_status': user_data['user_status'],
        'gender': user_data['gender'],
        'membership_type': user_data['membership_type'],
        'bio': user_data['bio'],
        'date_of_birth': user_data['date_of_birth']
    }
    result = mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': user})
    if result.modified_count > 0:
        return jsonify('User updated successfully'), 200
    else:
        return jsonify('User not found'), 404

# ================================== user delete=================================

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = mongo.db.users.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count > 0:
        return jsonify('User deleted successfully'), 200
    else:
        return jsonify('User not found'), 404
    

# user register
# @app.route('/register', methods=['POST'])
# def register():
#     name = request.json.get("name")
#     username = request.json.get('email')
#     password = bcrypt.generate_password_hash(request.json.get('password')).decode('utf-8')
#     user_status = request.json.get('user_status')
#     gender = request.json.get('gender')
#     membership_type = request.json.get('membership_type')
#     bio = request.json.get('bio')
#     date_of_birth = request.json.get('date_of_birth')

#     # Check if the username already exists in the database
#     existing_user = mongo.db.users.find_one({'username': username})
#     if existing_user:
#         return jsonify({'message': 'Username already exists'}), 409
#     # Create a new user in the database
#     user_id = mongo.db.users.insert_one({'name': name, 'username': username, 'password': password,"user_status":user_status,"gender":gender,"membership_type":membership_type,"bio":bio,"date_of_birth":date_of_birth}).inserted_id
#     return jsonify({'message': 'User registered successfully', 'user_id': str(user_id)}), 201


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
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401



# ==================================protected route if you have a tocken then you have acces it==============================================
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'user_id': current_user}), 200




if __name__ == '__main__':
    app.run(debug=True)

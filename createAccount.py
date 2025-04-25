from flask import Flask, request, jsonify
import bcrypt
import re
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

app = Flask(__name__)

#connect to Mongo databse
def connect():
    try:
        # db information from weiguo
        client = MongoClient('mongodb+srv://Liam:LiamPassword@cluster0.upg7jme.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
        db = client["UserDatabase"]
        return db
    except ConnectionFailure as e:
        print("Could not connect to database")
    return None

@app.route('/createAccount', methods=['POST'])
def createAccount():
    #get username and password 
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    
    #username blank
    if not username:
        return jsonify({'message': 'Username required'}), 400 #bad request
    
    #password blank
    if not password:
        return jsonify({'message': 'Password required'}), 400 #bad request
    
    #username too short
    if len(username) < 6:
        return jsonify({'message': 'Username must be at least 6 characters long'}), 400 #bad request

    #password too short
    if len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters long'}), 400 #bad request
    
    #password must contain at least one digit
    if not re.search(r'[0-9]', password):
        return jsonify({'message': 'Password must contain at least one digit'}), 400 #bad request
    
    #Password must contain at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return jsonify({'message': 'Password must contain at least one lowercase letter'}), 400 #bad request
    
    #Password must contain at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return jsonify({'message': 'Password must contain at least one uppercase letter'}), 400 #bad request
    
    #Password must contain at least one special character
    if not re.search(r'[\W_]', password):
        return jsonify({'message': "Password must contain at least one special character"}), 400 #bad request
    
    #connect to db to add new user information
    db = connect()

    if db is None:
        return jsonify({'message': 'Error: could not connect to database'}), 500
    
    #check if user already exists in the database
    users = db["userInfo"]
    if users.find_one({"username": username}):
        return jsonify({'message': 'User already exists'}), 400 #bad request
    
    else:
        #if not, hash password and store info in database
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        userData = {
            "username": username,
            "password": hashed_password
        }
    try:
        users.insert_one(userData)
        return jsonify({'message': 'Account created successfully'}), 201
    except Exception as e:
        print(e)
        return jsonify({'message': 'Server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
import bcrypt
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

app = Flask(__name__)

#connect to database
def connect():
    try:
        # db information from weiguo
        client = MongoClient('mongodb+srv://Liam:LiamPassword@cluster0.upg7jme.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
        db = client["UserDatabase"]
        return db
    except ConnectionFailure as e:
        print("Could not connect to database")
    return None

@app.route('/login', methods=['POST'])
def login():
    
    #get username and password
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    
    if not username:
        return jsonify({'message': 'Username required'}), 400 #bad request
    
    if not password:
        return jsonify({'message': 'Password required'}), 400 #bad request

    #connect to database to see if user exists
    db = connect()
    if db is None:
        return jsonify({'message': 'Error: could not connect to database'}), 500
        
     #check if username is in database 
    users = db["userInfo"]
    user = users.find_one({"username": username})
    if not user:
        return jsonify({'message': 'User not found'}), 404  # Not Found
    
        #check if hashed password matches
    stored_password = user['password']
    if bcrypt.checkpw(password.encode('utf-8'), stored_password):
        return jsonify({'message': 'Login successful'}), 200  # success
    else:
        return jsonify({'message': 'Incorrect Password'}), 401  #passwords dont match
    
if __name__ == '__main__':
    app.run(debug=True)
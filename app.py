from flask import Flask, session, Response, jsonify, request
import os
from utils.utils import validate_username, validate_password
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key = "asdasd56465asd43123123446546^%*&%(&Asd7a987(&"




@app.route('/signup', methods=['POST'])
def create_user():  # put application's code here
    data = {
        "user_id": "",
        "nickname": "",
        "comment": "",
        "password": "",
    }
    json = request.json

    user_id = json["user_id"]
    password = json["password"]

    if(user_id == None or password ==None):
        res = {
                "message": "Account creation failed",
                 "cause": "required user_id and password"
            }
        return Response(jsonify(res), status=400, mimetype='application/json')


    user_status = validate_username(user_id)
    password_status = validate_password(password)

    if user_status["text_type"]:
        res = {
                "message": "Account creation failed",
                "cause": "user_id is not alphanumeric"
            }
        return jsonify(res), 400

    if user_status["char_type"]:
        res = {
                "message": "Account creation failed",
                "cause": "user_id is not half-width"
            }
        return jsonify(res), 400


    if password_status["text_type"]:
        res = {
                "message": "Account creation failed",
                "cause": "password is not alphanumeric"
            }
        return jsonify(res), 400

    if password_status["char_type"]:
        res = {
                "message": "Account creation failed",
                "cause": "password is not half-width"
            }
        return jsonify(res), 400


    if session.get(user_id) != None:
        res = {
                "message": "Account creation failed",
                "cause": "already same user_id is used"
            }
        return jsonify(res), 400


    data[user_id] = user_id
    data[password] = password
    session[user_id] = data

    return jsonify(data), 200


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):  # put application's code here
    if request.authorization["username"] in session:
        if session.get(request.authorization["username"])["password"] != request.authorization["password"]:
            return jsonify({"message": "Authentication failed"}), 401

    if session.get(user_id) == None:
        return jsonify({"message": "no user found"}), 404
    res = {
        "message":"User Details by user_id",
        "user":{
            "user_id": session.get(user_id)["user_id"],
            "nickname":session.get(user_id)["nickname"],
            "comment":session.get(user_id)["comment"],
    }
    }

    return jsonify(res), 200


@app.route('/users/<user_id>', methods=['PATCH'])
def update_user(user_id):  # put application's code here

    if request.authorization["username"] in session:
        if session.get(request.authorization["username"])["password"] != request.authorization["password"]:
            return jsonify({"message": "Authentication failed"}), 401

    if session.get(user_id) == None:
        return jsonify({"message": "no user found"}), 404

    data = session.get(user_id)
    data["nickname"] = request.json['nickname']
    data["comment"] = request.json['comment']
    session[user_id] = data
    res = {
        "message":"update user by user id",

        "recipe": {
            "nickname": session.get(user_id)["nickname"],
            "comment": session.get(user_id)["comment"],
        }
    }

    return jsonify(res), 200


@app.route('/close', methods=['POST'])
def delete_user():  # put application's code here
    if request.authorization["username"] in session:
        if session.get(request.authorization["username"])["password"] != request.authorization["password"]:
            return jsonify({"message": "Authentication failed"}), 401

    session.pop(request.authorization["username"])

    return jsonify({"message": "user deleted"}), 200


if __name__ == '__main__':
    app.run()

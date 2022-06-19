from flask import Flask, jsonify, request
from utils.utils import validate_username, validate_password
from models.users import UserModel, db

app = Flask(__name__)
app.secret_key = "asdasd56465asd43123123446546^%*&%(&Asd7a987(&"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app=app)


@app.before_first_request
def create_table():
    db.create_all()


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/signup', methods=['POST'])
def create_user():  # put application's code here

    json = request.get_json()

    if "user_id" not in json or "password" not in json:
        res = {
            "message": "Account creation failed",
            "cause": "required user_id and password"
        }
        return res, 400

    user_id = json["user_id"]
    password = json["password"]

    if (user_id == None or password == None):
        res = {
            "message": "Account creation failed",
            "cause": "required user_id and password"
        }
        return res, 400

    user_status = validate_username(user_id)
    password_status = validate_password(password)

    if not user_status["text_type"]:
        res = {
            "message": "Account creation failed",
            "cause": "user_id is not alphanumeric"
        }
        return res, 400

    if not user_status["char_type"]:
        res = {
            "message": "Account creation failed",
            "cause": "user_id is not half-width"
        }
        return res, 400

    if not user_status["length"]:
        res = {
            "message": "Account creation failed",
            "cause": "user_id length is not between 6 to 20"
        }
        return res, 400

    if not password_status["text_type"]:
        res = {
            "message": "Account creation failed",
            "cause": "password is not alphanumeric"
        }
        return res, 400

    if not password_status["char_type"]:
        res = {
            "message": "Account creation failed",
            "cause": "password is not half-width"
        }
        return res, 400

    if not password_status["length"]:
        res = {
            "message": "Account creation failed",
            "cause": "password length is not between 8 to 20"
        }
        return res, 400

    user = UserModel.query.filter_by(user_id=user_id).first()
    if user:
        res = {
            "message": "Account creation failed",
            "cause": "already same user_id is used"
        }
        return jsonify(res), 400

    new_user = UserModel(user_id=user_id)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 200


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):  # put application's code here

    if not "authorization" in request.headers:
        return jsonify({"message": "Authentication failed for no auth header"}), 401

    if "username" not in request.authorization or "password" not in request.authorization:
        return jsonify({"message": "Authentication failed"}), 401

    auth_user = UserModel.query.filter_by(user_id=request.authorization["username"]).first()
    if auth_user:
        password = request.authorization["password"]
        if not auth_user.check_password(password):
            return jsonify({"message": "Authentication failed for invalid password"}), 401
    else:
        return jsonify({"message": "Authentication failed  for invalid username"}), 401

    user = UserModel.query.filter_by(user_id=user_id).first()
    if user:
        res = {
            "message": "User Details by user_id",
            "user": {
                "user_id": user.user_id,
                "nickname": user.nickname,
                "comment": user.comment,
            }
        }

        return jsonify(res), 200

    return jsonify({"message": "no user found"}), 404


@app.route('/users/<user_id>', methods=['PATCH'])
def update_user(user_id):  # put application's code here
    if not "authorization" in request.headers:
        return jsonify({"message": "Authentication failed for no auth header"}), 401

    if "username" not in request.authorization or "password" not in request.authorization:
        return jsonify({"message": "Authentication failed for invalid username or password"}), 401

    auth_user = UserModel.query.filter_by(user_id=request.authorization["username"]).first()
    if auth_user:
        password = request.authorization["password"]
        if not auth_user.check_password(password):
            return jsonify({"message": "Authentication failed for invalid password"}), 401
    else:
        return jsonify({"message": "Authentication failed  for invalid username"}), 401

    user = UserModel.query.filter_by(user_id=user_id).first()
    if user:
        if "nickname" in request.json:
            user.nickname = request.json['nickname']
        if "comment" in request.json:
            user.comment = request.json['comment']
        db.session.add(user)
        db.session.commit()
        res = {
            "message": "updated user by user id",

            "recipe": {
                "nickname": user.nickname,
                "comment": user.comment,
            }
        }
        return jsonify(res), 200

    return jsonify({"message": "no user found"}), 404


@app.route('/close', methods=['POST'])
def delete_user():  # put application's code here
    if not "authorization" in request.headers:
        return jsonify({"message": "Authentication failed"}), 401

    if "username" not in request.authorization or "password" not in request.authorization:
        return jsonify({"message": "Authentication failed"}), 401

    auth_user = UserModel.query.filter_by(user_id=request.authorization["username"]).first()
    if auth_user:
        password = request.authorization["password"]
        if not auth_user.check_password(password):
            return jsonify({"message": "Authentication failed for invalid password"}), 401
    else:
        return jsonify({"message": "Authentication failed  for invalid username"}), 401

    user = UserModel.query.filter_by(user_id=request.authorization["username"]).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "user deleted"}), 200

    return jsonify({"message": "no user found"}), 404


if __name__ == '__main__':
    app.run()

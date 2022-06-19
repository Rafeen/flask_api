from flask import Flask, session, Response, jsonify
import json


app = Flask(__name__)
app.secret_key = "asdasd56465asd43123123446546^%*&%(&Asd7a987(&"
@app.route('/test', methods=['GET'])
def recursive_api():  # put application's code here
    data = {
        "Response": "Api call successfull",
    }

    return jsonify(data)


if __name__ == '__main__':
    app.run()

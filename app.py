from flask import Flask, session, Response
from flask import request
from datetime import datetime, timezone
import requests
import json


app = Flask(__name__)
app.secret_key = "asdasd56465asd43123123446546^%*&%(&Asd7a987(&"
@app.route('/api/recursive/ask', methods=['GET'])
def recursive_api():  # put application's code here
    n = int(request.args.get('n'))
    seed = request.args.get('seed')

    # if n and seed is not provided
    if n is None or seed is None:
        return Response(
            "400 BadRequest",
            status=400,
        )

    if seed in session:
        dt = int((datetime.now(timezone.utc)-session.get(seed+'time')).total_seconds())

        # if 1hr passed from the first request reset time and count
        if dt > 3600:
            set_session(seed)

        #if api is called over 50 times within 1 hour
        if session.get(seed) == 0:
            return Response(
                "Service Unavailable",
                status=503,
            )

    else:
        set_session(seed)


    #perform the recursive task
    print(recursive_task(n, seed))
    session[seed] = session.get(seed) - 1


    #after successfully running the function
    return Response(
                "OK",
                status=200,
            )

cache = {}
def recursive_task(n, seed):

    if n == 0:
        return 1

    elif n == 2:
        return 2

    elif n % 2 == 0:
        return recursive_task(n-1, seed) + recursive_task(n-2, seed) + recursive_task(n-3, seed) + recursive_task(n-4, seed)

    else:
        if session.get(seed) == 0:
            print("over limit")
            return 0
        if n in cache:
            return cache[n]
        else:
            cache[n] = ask_server(n, seed)
            return cache[n]


def set_session(seed):
    session[seed] = 50
    session[seed + 'time'] = datetime.now(timezone.utc)


def ask_server(n, seed):
    response = requests.get(f'http://challenge-server.code-check.io/api/recursive/ask?n={n}&seed={seed}')
    json_data = json.loads(response.text.encode('utf8'))
    return int(json_data["result"])


if __name__ == '__main__':
    app.run()

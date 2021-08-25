from flask import Flask, request, Response
import os

app = Flask(__name__)


@app.route('/meta')
def meta():
    env_name = os.environ['ENV_NAME']
    expected_response = request.args.get('response-type')

    return Response(env_name, status=expected_response, mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

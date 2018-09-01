from flask import Flask, request, Response, jsonify


def create_app():

    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def home():
        data = {
            'message': 'Hello World',
            'count': 3
            }
        response = jsonify(data)
        response.status_code = 200
        
        return response

    return app


if __name__ == '__main__':
    FLASK_APP = create_app()
    FLASK_APP.run(host='0.0.0.0', debug=True)

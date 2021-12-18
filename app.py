from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS

from api import PorfirevichApi

from utils import UtilsMethods

app = Flask(__name__)
api = Api(app)
CORS(app)


class StatusApp(Resource):
    @staticmethod
    def get() -> jsonify:
        return jsonify({'run': True})

      
class RandomStory(Resource):
    @staticmethod
    def get() -> jsonify:
        json_data = PorfirevichApi().get_json()
        return jsonify(UtilsMethods.create_story_list(json_data))


api.add_resource(StatusApp, '/')
api.add_resource(RandomStory, '/random')

if __name__ == '__main__':
    app.run()

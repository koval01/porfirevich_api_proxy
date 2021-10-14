import logging

from flask import Flask, jsonify, request, g
from flask_restful import Resource, Api
from flask_cors import CORS
from requests import get
from time import time

app = Flask(__name__)
api = Api(app)
CORS(app)


class status(Resource):
    def get(self) -> None:
        g.start = time()
        return jsonify({'run': True, "time": "%.5fs" % (time() - g.start)})

      
class Random(Resource):
    def get(self) -> None:
        g.start = time()
        
        response = get(
          "https://porfirevich.ru/api/story",
          params={
            "limit": 20,
            "offset": 0,
            "orderBy": "RAND()",
          }
        ).json()
        json_data = response["data"]
        
        return jsonify({'posts': json_data, "time": "%.5fs" % (time() - g.start)})


api.add_resource(status, '/')
api.add_resource(Random, '/random')

if __name__ == '__main__':
    app.run()

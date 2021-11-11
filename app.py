import logging

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS

from requests import get

from utils import check_long_words_in_string, cleanhtml, fix_string, decode_story_string, check_len_story

app = Flask(__name__)
api = Api(app)
CORS(app)


class status(Resource):
    def get(self) -> None:
        return jsonify({'run': True})

      
class Random(Resource):
    def get(self) -> None:
        response = get(
          "https://porfirevich.ru/api/story",
          params={
            "limit": 20,
            "offset": 0,
            "orderBy": "RAND()",
          }
        ).json()
        json_data = response["data"]
        
        for el in json_data:
            if check_len_story(el["content"]):
                el["content"] = decode_story_string(el["content"])
                el["createdAt"] = el["createdAt"].replace("T", " ").replace(".000Z", "")
                
                del el["description"], el["editId"], el["isBanned"], el["isDeleted"]
                del el["isPublic"], el["updatedAt"], el["userId"], el["viewsCount"] 
                del el["violationsCount"], el["postcard"]
        
        return jsonify(json_data)


api.add_resource(status, '/')
api.add_resource(Random, '/random')

if __name__ == '__main__':
    app.run()

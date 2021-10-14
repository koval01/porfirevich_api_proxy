import logging, re, json

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS
from requests import get
from time import time

app = Flask(__name__)
api = Api(app)
CORS(app)


def cleanhtml(raw_html) -> str:
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def fix_string(string) -> str:
    in_word = string
    in_between_words = ['-', '–']
    in_sentences = ['«', '(', '[', '{', '"', '„', '\'']
    string = string.replace("\n\n", "\n")
    for item in in_between_words:
        regex = r'\w[%s]\s\w' % item
        in_word = re.findall(regex, string)

        for x in in_word:
            a = x[:1]; b = x[3:4]
            string = string.replace(x, a + '-' + b)

    for item in in_sentences:
        string = string.replace(f' {item} ', f' {item}')
    return string


def decode_story_string(array) -> str:
    struct_array = []
    array = json.loads(array)
    for i in array:
        text = cleanhtml(i[0])
        text = fix_string(text)
        if check_long_words_in_string(text):
            text = text.replace('\n', '</br>')
            if i[1]:
                struct_array.append('<b>%s</b>' % text)
            else: 
                struct_array.append('<i>%s</i>' % text)
        else:
            struct_array.append('<b>Произошла ошибка!</b>')
    return ''.join(struct_array)


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
            el["content"] = decode_story_string(el["content"])
        
        return jsonify(json_data)


api.add_resource(status, '/')
api.add_resource(Random, '/random')

if __name__ == '__main__':
    app.run()

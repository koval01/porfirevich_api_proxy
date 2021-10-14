import logging, re, json

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS
from requests import get
from time import time

app = Flask(__name__)
api = Api(app)
CORS(app)


def check_long_words_in_string(string) -> bool:
    """
    Проверка наличия слишком довгих слов/елементов в строке
    """
    status = True
    s = string.split()
    for i in s:
        if len(i) > 29:
            status = False

    return status


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


def prepare_element(el, bold=False) -> str or None:
    if el[-1:] != " ": return
    ptrn = "*"; if bold: ptrn = "**"
    end = re.sub(r"(\w)\s", r"\1%s " % ptrn, el[-2:])
    return ptrn + x.rstrip()[:-1] + end


def decode_story_string(array) -> str:
    struct_array = []
    array = json.loads(array)
    for i in array:
        text = cleanhtml(i[0])
        text = fix_string(text)
        if check_long_words_in_string(text):
            if i[1]:
                x = prepare_element(text, True)
                if not x: x = "**%s**" % text
                struct_array.append(x) # Bold
            else:
                x = prepare_element(text)
                if not x: x = "*%s*" % text
                struct_array.append(x) # Italic
        else:
            struct_array.append('**Произошла ошибка!**')
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
            del el["description"], el["editId"], el["isBanned"], el["isDeleted"], el["isPublic"], el["updatedAt"], el["userId"], el["viewsCount"], el["violationsCount"], el["postcard"]
        
        return jsonify(json_data)


api.add_resource(status, '/')
api.add_resource(Random, '/random')

if __name__ == '__main__':
    app.run()

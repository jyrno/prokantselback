from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_restful import reqparse, Resource, Api

import synonymes as syn
import keerukus

import backend
import analyzer

app = Flask(__name__)
CORS(app)
api = Api(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route("/synonymes/", methods=['GET'])
def synonymes():
    word = request.args.get('word', default = '*', type = str)
    synonymes = syn.list_of_synonymes(word)
    return jsonify(word = word, synonymes = synonymes)


@app.route("/teksti-keerukus/", methods=['GET'])
def teksti_keerukus():
    text = request.args.get('text', default = '*', type = str)
    response = keerukus.text_complexity_evaluation(text)
    return jsonify(complexity = response[1], percentage = response[0])


class Kantseliit(Resource):
    def get(self):
        return "Kantseliit on selline keeruline asi, millest keegi aru ei saa"


class Loe(Resource):
    def get(self, tekst):
        return backend.kokku(tekst)


class Pooltarind(Resource):
    def get(self, tekst):
        return backend.poolttarind(tekst)


parser = reqparse.RequestParser()
parser.add_argument('text')


class Analuus(Resource):
    def post(self):
        args = parser.parse_args()
        text = args['text']
        print(text)
        return jsonify({
            'complexity': keerukus.text_complexity_evaluation(text),
            'analysis': analyys(text)
        })


def analyys(tekst):
    return analyzer.sisend(tekst)


api.add_resource(Kantseliit, '/kantsel')
api.add_resource(Loe, '/loe/<tekst>')
api.add_resource(Pooltarind, '/tarind/<tekst>')
api.add_resource(Analuus, '/check')

if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context='adhoc')

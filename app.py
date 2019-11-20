from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api
from flask import request
import synonymes as syn

import backend

app = Flask(__name__)
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

class Kantseliit(Resource):
    def get(self):
        return "Kantseliit on selline keeruline asi, millest keegi aru ei saa"

class Loe(Resource):
    def get(self, tekst):
        return backend.kokku(tekst)

class Pooltarind(Resource):
    def get(self, tekst):
        return backend.poolttarind(tekst)

class Analuus(Resource):
    def post(self, tekst):
        return jsonify({'analuus': (tekst)})



api.add_resource(Kantseliit, '/kantsel')
api.add_resource(Loe, '/loe/<tekst>')
api.add_resource(Pooltarind, '/tarind/<tekst>')
api.add_resource(Analuus, '/analuus')

if __name__ == '__main__':
    app.run()

import json
from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  


def load_filmes():
    try:
        with open('filmes.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_filmes(filmes):
    with open('filmes.json', 'w') as file:
        json.dump(filmes, file, indent=4)

filmes = load_filmes()

@app.route('/filmes', methods=['GET'])
def get_filmes():
    return jsonify(filmes)

@app.route('/filmes/<int:filme_id>', methods=['GET'])
def get_filme(filme_id):
    filme = next((f for f in filmes if f['id'] == filme_id), None)
    if filme is None:
        abort(404)
    return jsonify(filme)

@app.route('/filmes', methods=['POST'])
def create_filme():
    if not request.json or not 'titulo' in request.json:
        abort(400)
    new_id = filmes[-1]['id'] + 1 if filmes else 1
    filme = {
        'id': new_id,
        'titulo': request.json['titulo'],
        'diretor': request.json.get('diretor', ""),
        'ano': request.json.get('ano', 0),
        'nota': request.json.get('nota', 0.0),
        'duracao': request.json.get('duracao', 0),
        'genero': request.json.get('genero', "")
    }
    filmes.append(filme)
    save_filmes(filmes)
    return jsonify(filme), 201

@app.route('/filmes/<int:filme_id>', methods=['PUT'])
def update_filme(filme_id):
    filme = next((f for f in filmes if f['id'] == filme_id), None)
    if filme is None:
        abort(404)
    data = request.get_json()
    filme.update(data)
    save_filmes(filmes)
    return jsonify(filme)

@app.route('/filmes/<int:filme_id>', methods=['DELETE'])
def delete_filme(filme_id):
    global filmes
    filmes = [f for f in filmes if f['id'] != filme_id]
    save_filmes(filmes)
    return jsonify({'message': 'Filme excluído com sucesso'}), 200


@app.route('/filmes/titulo/<string:titulo>', methods=['DELETE'])
def delete_filme_by_titulo(titulo):
    global filmes
    filme = next((f for f in filmes if f['titulo'] == titulo), None)
    if filme is None:
        abort(404)
    filmes = [f for f in filmes if f['titulo'] != titulo]
    save_filmes(filmes)
    return jsonify({'message': 'Filme excluído com sucesso'}), 200


@app.route('/', methods=['GET'])
def home():
    return '''
    '''

if __name__ == '__main__':
    app.run(debug=True)

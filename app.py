import flask, os
from flask import Flask, request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from awsTranscribe import makeTrans
from flask import jsonify

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/convertir', methods=['POST'])
def transcribir():

    print('Iniciando')
    target=os.getcwd()
    archivo=request.files['file']
    print(archivo)
    filename=secure_filename(archivo.filename)
    print(filename)
    destination="/".join([target, os.path.splitext(filename)[0]+'.wav'])
    archivo.save(destination)
    string = makeTrans(archivo)
    print(string)
    return jsonify(resultado=string.split(' ', 1)[0])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
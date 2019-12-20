import flask, os
from flask import Flask, request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from awsTranscribe import makeTrans
from flask import jsonify
import unidecode
import re

#Iniciamos el servidor Flask
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

#Funcion que recibe el audio en formato WAV y lo envia al metodo del script awsTranscribe.py para ser procesado
@app.route('/convertir', methods=['POST'])
def transcribir():

    print('Iniciando')
    #Se guarda el archivo en la carpeta actual
    target=os.getcwd()
    archivo=request.files['file']
    print(archivo)
    filename=secure_filename(archivo.filename)
    print(filename)
    destination="/".join([target, filename])
    archivo.save(destination)
    #Se envia el archivo al metodo y se recibe un string
    string = unidecode.unidecode(re.sub(r'[^\w\s]','',makeTrans(archivo).upper()))
    print(string)
    #Se devuelve el string con la primera palabra identificada del audio
    return jsonify(resultado=unidecode.unidecode(string.split(' ', 1)[0]))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5010, debug=True)
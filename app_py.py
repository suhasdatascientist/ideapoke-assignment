import os
import requests
from spacy_extract_info import extract_info
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods = ['POST','GET'])
def output():
    json_input = request.get_json(force=True)
    text = json_input['Input']        
    
    return jsonify({"Output":extract_info(text)})


if __name__ == '__main__':
    app.run('0.0.0.0' , 5080 , debug=True , threaded=True)  

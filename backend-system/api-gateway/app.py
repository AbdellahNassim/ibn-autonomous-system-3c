from flask import Flask, request, jsonify
import json
import os
from rdflib import Graph
from utils import setup_logger


app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>Hello API Gateway </h1>'


@app.route('/services', methods=['POST'])
def services():
    """
        Post route to allow providing intent in standard format
    """

    logger = setup_logger()
    # depending on the content type we will map our data
    if request.content_type == "application/json":
        logger.info("Received intent in json format")
        # the received content is in json
        received_intent_json = json.dumps(request.get_json())
        logger.info(received_intent_json)
        # creating a graph back
        g = Graph()
        current_absolute_path = 'file://' + os.path.abspath('.')+'/'
        print(current_absolute_path)
        received_intent_json = received_intent_json.replace(
            current_absolute_path, '')
        print(received_intent_json)
        # parsing the format
        g.parse(format="json-ld", data=received_intent_json)
        if len(g) == 0:
            return jsonify(exception="Error parsing the intent")
        else:
            print(g.serialize(format="turtle"))
    elif request.content_type == "application/xml":
        # if the received content is in xml then
        print(request.content_type)
        print(request.get_data())
    else:
        # adding support for other formats
        print(request.content_type)
        print(request.get_data())


port = int(os.environ.get('PORT', 8080))
app.run(debug=True, host='0.0.0.0', port=port)

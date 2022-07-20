from flask import Flask, request, jsonify
import os
from utils import setup_logger, validate_intent_format, forward_intent


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
        # validate the intent format (rdf)
        print(request.get_json())
        intent_validated = validate_intent_format(
            'json', request.get_json(), logger)
        # check if it's valid
        if not intent_validated:
            return jsonify(exception="Error parsing the intent")
        else:
            # if the intent is valid then send it back to the backend
            return forward_intent(intent_validated, logger)
    elif request.content_type == "application/xml":
        intent_validated = validate_intent_format(
            "xml", request.get_data(), logger)
        # check if it's valid
        if not intent_validated:
            return jsonify(exception="Error parsing the intent")
        else:
            # if the intent is valid then send it back to the backend
            return forward_intent(intent_validated, logger)

    else:
        # adding support for other formats
        print(request.content_type)
        print(request.get_data())


port = int(os.environ.get('PORT', 8080))
app.run(debug=True, host='0.0.0.0', port=port)

from flask import Flask, request, jsonify, send_file
import os 
import json
app = Flask(__name__)







@app.route('/')
def hello():
    return '<h1>Hello From ML Marketplace </h1>'



@app.route('/models/search', methods=["GET"])
def search_models():
    """
        Api route that allows requesting a Machine Learning models. 
        The parameters of the model are passed as GET params

        Accepted body is 
        {
            service: "",
            input:[],
            output:[],
            is_trained: True,
            format: "h5"
        }
    """
    model_request_data = request.get_json()
    # check the properties 
    if "service" not in model_request_data:
        return jsonify(error="No service specified")
    if "input" not in model_request_data:
        return jsonify(error="The input parameters of the model needs to be specified")
    
    # get the current available models 
    with open("models_index.json") as model_index:
        available_models = json.load(model_index)
        # loop on the categories of the models based on the service
        category_models = None
        for category in available_models:
            if category["service"] == model_request_data["service"]:
                category_models = category
                break
        if category_models == None:
            return jsonify(error="No model could be found with the requested service")
        # Loop then on the models of the category 
        for model in category_models["available_models"]:
            if model["input"] == model_request_data["input"]:
                return jsonify(model)
    return jsonify(error="No model could be found with the requested parameters")


@app.route('/models/<uuid:model_id>', methods=["GET"])
def get_models(model_id):
    """
        Route to allow the intent manager to get the model by the model id . 
    """
    # list all the models in the directory 
    for model_file in os.scandir('./production-models'):
        # split the file name to remove extension
        if str(model_id) == os.path.splitext(model_file.name)[0]:
            # read the model and send it 
            return send_file('./production-models/{}'.format(model_file.name), mimetype="h5")
    return jsonify('No model with the model_id {}'.format(model_id))

port = int(os.environ.get('PORT', 8000))
app.run(debug=True, host='0.0.0.0', port=port)
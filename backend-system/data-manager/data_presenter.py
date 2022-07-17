from flask import Flask, request, jsonify
import os


app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>Hello From Data Manager </h1>'


@app.route('/network/throughput/<namespace>', methods=['GET'])
def network_throughput_data_view(namespace):
    """
        Data View to get value of the network throughput 
    """
    print(namespace)
    return jsonify('Intent deployment scheduled successfully')


def start_data_presenter(logger):
    """
        Start the flask server 
    """
    port = int(os.environ.get('DATA_MANAGER_INTERNAL_PORT', 8080))
    app.run(debug=True, threaded=True, host='0.0.0.0', port=port)

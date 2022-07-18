from flask import Flask, request, jsonify
import os
from utils import create_connection, check_env_variables


app = Flask(__name__)


# check and load the environment variables
check_env_variables()

# create connection
db_client = create_connection()


@app.route('/')
def hello():
    return '<h1>Hello From Data Manager </h1>'


@app.route('/network/throughput/<namespace>', methods=['GET'])
def network_throughput_data_view(namespace):
    """
        Data View to get value of the network throughput 
    """

    # query to get
    query = """
        from(bucket: "{}")
    |> range(start: {})
    |> filter(fn: (r) => r._measurement =="{}"  and r.namespace == "{}")
    |> filter(fn: (r) => r._field == "{}" )
    |> derivative(unit: 1s)
    """
    # get bucket name
    bucket = os.environ['INFLUX_DB_BUCKET']
    # set start
    starting_form = "-1h"
    # set measurement
    measurement = "pods_network_measurement"
    # set field
    receive_bytes_field = "_receive_bytes_total"
    # format query
    # TODO this is a very vulnerable way to format queries
    query = query.format(bucket, starting_form, measurement,
                         namespace, receive_bytes_field)
    # get query api
    query_api = db_client.query_api()
    # get organization name
    bucket = os.environ['INFLUX_DB_ORG']
    # get result
    result = query_api.query(org=org, query=query)
    return jsonify(result)


port = int(os.environ.get('DATA_MANAGER_INTERNAL_PORT', 8080))
app.run(debug=True, host='0.0.0.0', port=port)

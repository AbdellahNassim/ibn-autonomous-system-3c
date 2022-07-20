import os
import re
from utils import create_connection
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime


"""
    The data pre processor responsibility is to standardize and pre process the received
    data from the telemetry.
    It then injects the data into Data Store
    For the current version influxdb is used as a data store where the schema that we choosed is:
        - Each data point is a metric 
        - Each metric belongs to a measurment we will have three measurements 'compute' 'storage' 'network'
        - Tags will be namespace and podName 
        - Fields will depends on the measurement for example:
        Point("measurement"="compute_measurement","namespace"="intent-100","podName"="intent-100-transcoder",
                "_field"="memory_usage", "_value"="100"
                )

"""


# # names of the received metrics that are related to network
# NETWORK_METRICS = ['container_network_receive_bytes_total', 'container_network_transmit_packets_dropped_total', 'container_network_receive_packets_dropped_total',
#                    'container_network_transmit_packets_total', 'container_network_receive_packets_total', 'container_network_transmit_bytes_total']

# # names of the received metrics related to compute
# COMPUTE_METRICS = ['node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate',
#                    'container_memory_working_set_bytes', 'kube_pod_container_resource_requests', 'kube_pod_container_resource_limits']

# # names of the received metrics related to storage
# STORAGE_METRICS = ['container_fs_writes_bytes_total',
#                    'container_fs_reads_bytes_total']


# client
db_client = None


def init_preprocessor():
    """
        An function to initialize the data preprocessor
    """
    # use the global variable
    global db_client
    # initialize a connection
    db_client = create_connection()


def standardize_metrics(metric):
    """
        Function that standardize the metric names 
            - Initially it just map the received metrics names to more standards that 
                can be queried by the data view component
            - Categorize the metric into either "network", "compute", or "storage" measurement 
        returns 
            - measurement_name which is the category of the metric will be also used by influxdb as the measurement 
            - field_name which is the field in measurement
            - field_value value of the metric
    """
    # get metric name
    metric_name = metric["MetricName"]
    # check if metric is network metric
    network_metric = re.findall(r'container_network(.*)', metric_name)
    # if the regex matches
    if len(network_metric):
        # we set the measurement
        measurement_name = "pods_network_measurement"
        # set the field of the metric
        field_name = network_metric[0]
        # set the value
        field_value = metric['MetricValue']
        return (measurement_name, field_name, field_value)
    # check if metric is storage metric
    storage_metric = re.findall(r'container_fs(.*)', metric_name)
    if len(storage_metric):
        # we set the measurement
        measurement_name = "pods_storage_measurement"
        # set the field of the metric
        field_name = storage_metric[0]
        # set the value
        field_value = metric['MetricValue']
        return (measurement_name, field_name, field_value)
    # Compute metrics
    measurement_name = "pods_compute_measurement"
    field_name = metric_name
    field_value = metric['MetricValue']
    return (measurement_name, field_name, field_value)


def preprocess_data(metric):
    """
        A function that process the received metrics, standardize it and clean it in order
        to be saved for further usage.
    """

    # filter metrics that are related to kube-system or prometheus namespace
    if (metric['Namespace'] != "prometheus") and (metric['Namespace'] != "kube-system"):
        measurement_name, field_name, field_value = standardize_metrics(metric)
        # create a point which is a data
        # specify the tags and fields
        p = Point(measurement_name).tag("namespace", metric['Namespace']).tag(
            "pod", metric["PodName"]).field(field_name,
                                            float(field_value)).time(metric['TimeStamp'], write_precision="ms")
        write_api = db_client.write_api(write_options=SYNCHRONOUS)
        bucket = os.environ['INFLUX_DB_BUCKET']
        # write data to bucket
        write_result = write_api.write(bucket=bucket, record=p)

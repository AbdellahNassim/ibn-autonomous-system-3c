import os
from utils import create_connection

# client
db_client = None


def init_preprocessor():
    """
        An function to initialize the data preprocessor
    """
    global db_client
    db_client = create_connection()


def preprocess_data(metric):
    """
        A function that process the received metrics, standardize it and clean it in order
        to be saved for further usage.
    """
    # filter metrics that are related to kube-system or prometheus namespace
    if (metric['namespace'] != "prometheus") and (metric['namespace'] != "kube-system"):
        # standardize the names of labels
        print(db_client)

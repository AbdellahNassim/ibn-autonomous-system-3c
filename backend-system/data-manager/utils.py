from dotenv import load_dotenv
import logging
import os
from influxdb_client import InfluxDBClient


def setup_logger():
    """
        This is a simple setup function it load environment variables and
        configure a logger. 
        return@ logger 
    """
    # This will load environment variables from the .env
    load_dotenv()
    # Now we can access those variables like any environment variable
    # configure the logging format
    logging.basicConfig(
        format="[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s ")
    # set logger name
    log = logging.getLogger("Data Management")
    # Check if we are in debug mode

    isDebug = ("DEBUG" in os.environ) and bool(os.environ["DEBUG"])
    # by default ignore debug logs
    logging_level = logging.WARNING
    if isDebug:
        logging_level = logging.DEBUG
    log.setLevel(logging_level)
    return log


def create_connection():
    """
        Create a connection to the influx db 
        This abstract database connectiona and interactions from the view of the preprocessor
    """
    influx_db_host = os.environ['INFLUX_DB_HOST']
    influx_db_port = os.environ['INFLUX_DB_PORT']
    influx_db_org = os.environ['INFLUX_DB_ORG']
    influx_db_token = os.environ['INFLUX_DB_TOKEN']
    influx_db_bucket = os.environ['INFLUX_DB_BUCKET']
    # create a client
    client = InfluxDBClient(f'http://{influx_db_host}:{influx_db_port}',
                            token=influx_db_token, org=influx_db_org)
    return client


def check_env_variables():
    """
        Check if the required env variables were specified or not 
    """
    if "DATA_MANAGEMENT_PORT" not in os.environ:
        raise Exception(
            "Environment Variable not specified $DATA_MANAGEMENT_PORT")
    if "INFLUX_DB_HOST" not in os.environ:
        raise Exception(
            "Environment Variable not specified $INFLUX_DB_HOST")
    if "INFLUX_DB_PORT" not in os.environ:
        raise Exception(
            "Environment Variable not specified $INFLUX_DB_PORT")
    if "INFLUX_DB_TOKEN" not in os.environ:
        raise Exception(
            "Environment Variable not specified $INFLUX_DB_TOKEN")
    if "INFLUX_DB_ORG" not in os.environ:
        raise Exception(
            "Environment Variable not specified $INFLUX_DB_ORG")
    if "INFLUX_DB_BUCKET" not in os.environ:
        raise Exception(
            "Environment Variable not specified $INFLUX_DB_BUCKET")

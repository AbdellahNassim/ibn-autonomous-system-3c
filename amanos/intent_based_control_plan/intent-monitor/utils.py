from dotenv import load_dotenv
import logging
import os


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
    log = logging.getLogger("Intent Monitor")
    # Check if we are in debug mode

    isDebug = ("DEBUG" in os.environ) and bool(os.environ["DEBUG"])
    # by default ignore debug logs
    logging_level = logging.WARNING
    if isDebug:
        logging_level = logging.DEBUG
    log.setLevel(logging_level)
    return log


def check_env_variables():
    """
        Check if the required env variables were specified or not 
    """
    if "INTENT_MANAGER_URL" not in os.environ:
        raise Exception(
            "Environment Variable not specified $INTENT_MANAGER_URL")
    if "DATA_MANAGER_URL" not in os.environ:
        raise Exception(
            "Environment Variable not specified $DATA_MANAGER_URL")
    if "INTENT_MONITOR_PORT" not in os.environ:
        raise Exception(
            "Environment Variable not specified $INTENT_MONITOR_PORT")

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
        format="[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s in %(pathname)s")
    # set logger name
    log = logging.getLogger("API Gateway")
    # Check if we are in debug mode
    isDebug = bool(os.environ["DEBUG"])
    # by default ignore debug logs
    logging_level = logging.WARNING
    if isDebug:
        logging_level = logging.DEBUG
    log.setLevel(logging_level)
    return log

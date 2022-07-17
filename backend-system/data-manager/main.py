from utils import setup_logger, check_env_variables
from data_preprocessor import init_preprocessor
from raw_data_collector import start_collector
from data_presenter import start_data_presenter
# setup logger
logger = setup_logger()


if __name__ == '__main__':
    # first check the environment variables
    try:
        check_env_variables()
        # if the env variables are working
        init_preprocessor()
        # start data presenter
        start_data_presenter(logger)
        # start the collector
        start_collector(logger)

    except Exception as e:
        raise e

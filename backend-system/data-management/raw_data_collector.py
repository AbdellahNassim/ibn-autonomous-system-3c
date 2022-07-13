import asyncio
import os
from utils import setup_logger

logger = setup_logger()


async def handle_data(reader, writer):
    """
        Data collector function 
        It allows the collection of telemetry data from the m&o layer
    """
    # read data from the network
    data = await reader.read()
    # decode from byte to string
    time_serie_metric = data.decode()
    print(time_serie_metric)


async def main():
    """
        Main function of the component 
    """
    # get environment port
    port = os.environ.get('DATA_MANAGEMENT_PORT', 6001)
    # create a simple server
    server = await asyncio.start_server(handle_data, '0.0.0.0', port)
    logger.info('Serving on  0.0.0.0:6001')

    # start the server
    async with server:
        await server.serve_forever()
        logger.info("Server started successfully")


asyncio.run(main())

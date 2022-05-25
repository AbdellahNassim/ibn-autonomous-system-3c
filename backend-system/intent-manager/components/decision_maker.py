

def process_intent(name, queue, logger):
    """
        function that process the intent. 
        We can have multiple instances of this function depending on the environment variable 
    """
    while True:    
        if not queue.empty():
            intent = queue.get()
            logger.info(intent)
        

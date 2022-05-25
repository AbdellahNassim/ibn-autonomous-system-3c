import queue
import os 
from components.decision_maker import process_intent
import threading


def schedule_processing(logger, queue, intent_dict):
    """
        Schedule the processing of the intent. 
    """
    logger.info("Scheduling the processing of intent {}".format(intent_dict['id']))
    # put the intent in a queue
    queue.put(intent_dict)


def setup_queue(logger):
    """
        Create Async Queue
    """
    logger.info("Creating an empty queue to process intents")
    # Create a queue that we will use to store our "workload".
    intent_queue = queue.Queue()
    return intent_queue

def setup_workers(logger, queue):
    """
        Create and start decision maker workers 
    """
    workers = []
    # get the number of workers 
    decision_makers_number= int(os.environ['DECISION_MAKER_INSTANCES'])
    logger.info("Launching {} Intance(s) of the decision maker".format(decision_makers_number))
    # save the tasks in a list in order to cleanup after 
    for i in range(decision_makers_number):
        # for each instance create a task that process the intent 
        worker = threading.Thread(target=process_intent, 
                                args=("intent-decision-maker-{}".format(i+1), 
                                queue, logger))
        worker.start()
        workers.append(worker)
    return workers


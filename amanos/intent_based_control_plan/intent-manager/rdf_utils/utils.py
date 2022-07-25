from rdf_utils.namespace import ICM, Catalog, TelecomMetrics, NetworkSliceModel
from rdflib import Graph, Literal, RDF, URIRef, BNode, Namespace


def create_namespaces(graph):
    """
        Creates namespaces that set urls to common models. 
    """
    # define the Intent Common Model namespace
    graph.bind("icm", ICM)
    # define the scoring services catalog namespace
    graph.bind("cat", Catalog)
    # define the telecom metrics namespace
    graph.bind("met", TelecomMetrics)
    # define the telecom metrics namespace
    graph.bind("ns", NetworkSliceModel)
    # create the base namespace
    scoring_base = Namespace('https://socring-ibn.univ-lr.fr/')
    # bind the namespace
    graph.bind('sc', scoring_base)
    return scoring_base


def format_to_graph(logger, intent):
    """
        Format the received intent into an rdf graph
    """
    # create graph
    g = Graph()
    # create and bind namespaces to make it readable
    create_namespaces(g)
    # parse the received intent
    g.parse(format="json-ld", data=intent)
    # logging the intent in a human readable format
    logger.info(g.serialize(format="turtle"))
    return g


def map_rdf_intent(logger, intent_graph):
    """
        This function will extract the informations from the rdf intent 
        it uses rdf queries in order to extract the requirements 
    """
    result_intent = {}

    # add it to the new intent model
    result_intent['id'] = extract_intent_id(intent_graph)
    # set service type
    result_intent['service_type'] = extract_service_type(intent_graph)
    # set service params
    result_intent["service_params"] = extract_service_params(intent_graph)
    return result_intent


def extract_intent_id(intent_graph):
    """
        Extracting the intent id from the graph 
    """
    # query to extract the id
    # The query get the entity that is of type intent
    intent_id_query = """
    SELECT ?intent_id WHERE { ?intent_id a icm:Intent }
    """
    # generate a list from the result
    query_result = list(intent_graph.query(intent_id_query))
    # extracting first element
    intent_id = query_result[0][0].replace(
        'https://socring-ibn.univ-lr.fr/', '')
    return intent_id


def extract_service_type(intent_graph):
    """
        Extracting the service type

    """
    # extract the service to deliver
    delivery_service_query = """
    SELECT ?service_type ?service_type_param WHERE {
        sc:service_delivery_expectation icm:params ?service_type_param.
        ?service_type_param a icm:DeliveryParam.
        ?service_type_param icm:targetDescription ?service_type.
    }
    """
    query_result = list(intent_graph.query(delivery_service_query))
    service_type = query_result[0][0].replace(Catalog._NS, '')
    return service_type


def extract_service_params(intent_graph):
    """
        Extracts and sets the service parameters
    """
    params = {}
    params_query = """
    SELECT ?param_name ?param_value ?param  WHERE {
        ?param a icm:PropertyParam . 
        ?param ?param_name [ icm:exactly ?param_value].
    }
    """
    query_result = intent_graph.query(params_query)
    for row in query_result:
        params[row.param_name.replace(
            TelecomMetrics._NS, '')] = str(row.param_value)
    return params

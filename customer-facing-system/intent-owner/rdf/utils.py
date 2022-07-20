from rdflib import Graph, Literal, RDF, URIRef, BNode, Namespace
from .namespaces import ICM, Catalog, TelecomMetrics, NetworkSliceModel


def standardize_intent(logger, user_intent):
    """
        This function will takes in a user intent and map it to 
        a standard format of the TmForum model 

        expected intent example
        user_intent = {
            "id":"intent-100",
            "service_type":"video",
            "latency":"20",
            "resolution":"640x480",
            "throughput":"30"
            # This is just a mockup until we implement the user authentication
            # TODO 
            "user_id":1
        }
    """

    # create the ontology graph
    g = Graph()
    # creating namespaces
    base_namespace = create_namespaces(g)
    # create delivery expectation
    delivery_expectation = create_delivery_expectations(g, base_namespace)
    # create property expectation
    property_expectation = create_property_expectation(
        g, base_namespace, latency=user_intent["latency"], throughput=user_intent['throughput'])
    # create the intent
    intent = create_intent(
        g, base_namespace, user_intent['id'], delivery_expectation, property_expectation)
    logger.info("Standard intent format has been generated")
    logger.info(g.serialize(format="turtle"))

    # returning the intent in json format to be sent
    return g.serialize(format="json-ld")


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


def create_intent(graph, base_namespace, intent_id, delivery_expectations, property_expectation):
    # creates a new intent
    intent = base_namespace[intent_id]
    # it has a type of intent
    graph.add((intent, RDF.type, ICM.Intent))
    for delivery_expectation in delivery_expectations:
        # it has a delivery expectation to deliver
        graph.add((intent, ICM.hasExpectation, delivery_expectation))
    # and has properties expectation on the service
    graph.add((intent, ICM.hasExpectation, property_expectation))
    return intent


def create_delivery_expectations(graph, base_namespace):
    """
        Creating delivery expectations
        A delivery expectation defines what the intent is expecting to deliver 
        In our case the intent will deliver a service and a network slice
    """
    # Creating the expectation of a network slice
    network_slice_delivery_expectation = base_namespace["network_slice_delivery_expectation"]
    # the subject is a delivery expectation
    graph.add((network_slice_delivery_expectation,
              RDF.type, ICM.DeliveryExpectation))
    # set the target of the delivery
    graph.add((network_slice_delivery_expectation,
              ICM.target, Literal("slice")))
    # defining the params of the target
    slice_param = base_namespace['slice_param']
    # the service_type_param is a deliveryparam
    graph.add((slice_param, RDF.type, ICM.DeliveryParam))
    # It target a video service from the scoring catalog
    graph.add((slice_param, ICM.targetDescription, NetworkSliceModel.core5g))
    # The service delivery expectation has the service type as params
    graph.add((network_slice_delivery_expectation,
              ICM.params, slice_param))

    # Setting the service delivery Expectations

    # Creating a new subject
    service_delivery_expectation = base_namespace["service_delivery_expectation"]
    # the subject is a delivery expectation
    graph.add((service_delivery_expectation, RDF.type, ICM.DeliveryExpectation))
    # it target the delivery of a service
    # Note: Here we should have used variable but because our system will
    # mainly deliver services we will choose individual
    graph.add((service_delivery_expectation, ICM.target, Literal("service")))

    # defining the params of the target
    service_type_param = base_namespace['service_type_param']
    # the service_type_param is a deliveryparam
    graph.add((service_type_param, RDF.type, ICM.DeliveryParam))
    # It target a video service from the scoring catalog
    graph.add((service_type_param, ICM.targetDescription, Catalog.video))
    # The service delivery expectation has the service type as params
    graph.add((service_delivery_expectation, ICM.params, service_type_param))

    return [service_delivery_expectation, network_slice_delivery_expectation]


def create_property_expectation(graph, base_namespace, **service_params):
    """
        Creates a property expectation. 
        The property expectation specify the requirements on the properties 
        of the wanted entity to be delivered. 
        In our case it specify the properties of the service to be delivered.
    """
    # create a new variable
    service_property_expectation = base_namespace['service_property_expectation']
    # the variable is a property expectation
    graph.add((service_property_expectation, RDF.type, ICM.PropertyExpectation))
    # The property expectation target the service
    # meaning it will define the properties of the service wanted to be delivered
    graph.add((service_property_expectation, ICM.target, Literal("service")))
    for param, value in service_params.items():
        # create a new variable of the param
        service_param = base_namespace['service_' + param + '_param']
        # the variable is a propertyParam
        graph.add((service_param, RDF.type, ICM.PropertyParam))

        # we create an empty node
        value_bnode = BNode()
        # set the empty node to be exactly the value
        # THis is important to represent that the service
        # params needs a param that is exactly a certain value
        graph.add((value_bnode, ICM.exactly, Literal(value)))
        # set the value of the param of the video service
        # Todo this is currently bounded to the video service only
        graph.add((service_param, TelecomMetrics[param], value_bnode))
        # the service property has params this parameter
        graph.add((service_property_expectation, ICM.params, service_param))
    return service_property_expectation

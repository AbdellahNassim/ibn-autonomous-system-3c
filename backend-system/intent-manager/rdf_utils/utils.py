from rdf_utils.namespace import ICM, Catalog, VideoService
from rdflib import Graph, Literal, RDF, URIRef, BNode, Namespace

def create_namespaces(graph):
    """
        Creates namespaces that set urls to common models. 
    """
    # define the Intent Common Model namespace
    graph.bind("icm",ICM)
    # define the scoring services catalog namespace
    graph.bind("cat",Catalog)
    # define the video service provider mode namespace
    graph.bind("vid",VideoService)
    # create the base namespace 
    scoring_base = Namespace('https://socring-ibn.univ-lr.fr/')
    # bind the namespace
    graph.bind('sc',scoring_base)


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


    
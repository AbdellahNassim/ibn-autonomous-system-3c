from rdflib.namespace import DefinedNamespace, Namespace
from rdflib.term import URIRef


class ICM(DefinedNamespace):
    """
    Intent Common Model, Version 1.1.0
    https://www.tmforum.org/resources/standard/ig1253a-intent-common-model-v1-1-0/
    Date: 2022-05-18
    """

    _fail = True

    # Classes
    Intent: URIRef
    Expectation: URIRef
    DeliveryExpectation: URIRef
    PropertyExpectation: URIRef

    ExpectationParam: URIRef
    PropertyParam: URIRef
    DeliveryParam: URIRef

    Information: URIRef
    InformationElement: URIRef

    ExpectationTarget: URIRef

    Context: URIRef

    ReferenceableNode: URIRef
    RequirementDefiner: URIRef
    RequirementElement: URIRef
    RequirementExplainer: URIRef
    RequirementReporter: URIRef
    RequirementReportExplainer: URIRef

    IntentReport: URIRef
    ReportingParam: URIRef
    ReportingExpectationReport: URIRef

    ReportingExpectation: URIRef
    DeliveryExpectationReport: URIRef
    ExpectationReport: URIRef
    ExpectationReportParam: URIRef
    ExpectationTarget: URIRef
    ParamReason: URIRef
    PropertyExpectationReport: URIRef

    IntentUpdateState: URIRef
    IntentHandlingEvent: URIRef
    IntentManagementState: URIRef
    IntentManagmentProcedure: URIRef
    IntentHandlingState: URIRef
    RejectionReason: URIRef

    # Properties
    atLeast: URIRef
    atMost: URIRef
    exactly: URIRef
    greater: URIRef
    hasContext: URIRef
    hasExpectation: URIRef
    hasExpectationReport: URIRef
    hasInformation: URIRef
    hasReportContext: URIRef
    oneOf: URIRef
    params: URIRef
    paramsCompliant: URIRef
    paramsDegraded: URIRef
    paramsUnknown: URIRef
    partOfProcedure: URIRef
    reasonForParamDegraded: URIRef
    reasonForParamUnknown: URIRef
    rejectedBecause: URIRef
    reportingDuration: URIRef
    reportingDurationLeft: URIRef
    reportingEvent: URIRef
    reportedEvent: URIRef
    reportingInterval: URIRef
    reportingIntervalLeft: URIRef
    reportsAbout: URIRef
    reportTimestamp: URIRef
    reportNumber: URIRef
    sameContextAs: URIRef
    smaller: URIRef
    target: URIRef
    targetDescription: URIRef
    targetReport: URIRef
    targetType: URIRef

    # I supposed the model will be available here
    _NS = Namespace("https://www.tmforum.org/2020/07/IntentCommonModel/")


class Catalog(DefinedNamespace):
    """
    SCORING Service Catalog 
    Date: 2022-05-18
    """

    _fail = True

    # individuals
    video: URIRef

    _NS = Namespace("https://chistera-scoring.github.io/services-catalog/")


class TelecomMetrics(DefinedNamespace):
    """
        Example of a video service model 
        Date: 2022-05-18
    """
    _fail = True

    latency: URIRef
    throughput: URIRef

    # I supposed the model will be available here
    _NS = Namespace("http://www.sdo.org/TelecomMetrics/Version_1.0/")


class NetworkSliceModel(DefinedNamespace):
    """
        Example of a video service model 
        Date: 2022-05-18
    """
    _fail = True

    core5g: URIRef
    ran: URIRef

    _NS = Namespace(
        "https://raw.githubusercontent.com/Orange-OpenSource/towards5gs-helm/main/repo/")

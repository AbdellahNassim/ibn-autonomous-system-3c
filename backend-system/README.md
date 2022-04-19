# Backend System

It is the core subsystem it is responsible for all the tasks related to intent management and configuration

# Architecture

The Backend System is built on a microservices based architecture, where an API Gateway (nodejs and ExpressJs) play the role of router and load balancer with the different microservices.

## Microservices

- **Data Contextualization** is responsible for the data collection and preprocessing, it can be accessed via `http://localhost:8080/data_contextualize`
- **Policy Generator** is responsible for the generation of relevent configurations based on the supplied decisions, can be accessed via `http://localhost:8080/policy_generator`
- **Intent Monitor** is responsible for the monitoring of the intent fulfillment, it provides also predictions and diagnoses, can be accessed via `http://localhost:8080/intent_monitor`
- **Intent Decision Maker** is responsible for generating decisions depending on the required services and Quality parameters, can be accessed via `http://localhost:8080/decision_maker`

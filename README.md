# SCORING-IB3C

A Proof-of-Concept Implementation of the Intent-Based Computing Caching and Communication (IB3C) Knowledge and Management plane of the Smart Collaborative Computing Caching and Communication (SCORING C4) Architecture.


## Development Environment
We will use minikube in order to simplify the developement stage. 
Next are the steps to setup kubernetes cluster in minikube:
- Install minikube 
```
    # Use url for more informations https://kubernetes.io/fr/docs/tasks/tools/install-minikube/
    curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
  && chmod +x minikube
    # Adding minikube executable to path 
    sudo mkdir -p /usr/local/bin/
    sudo install minikube /usr/local/bin/ 

```
- Start kubernetes cluster 

```bash
    # for development we will be using Minikube 
    # This will start minikube with 2 nodes a 8gb of rams and a maximum of cpu 
    minikube start --nodes=2 --memory='8192'  --cpus='max'
```

- Install kube ovn 
```bash
    # download kube ovn 
    wget https://raw.githubusercontent.com/kubeovn/kube-ovn/release-1.10/dist/images/install.sh

    # Install kube ovn 
    ./install.sh 
```



# Getting started

## Launch The Intent Based System

- To deploy the customer facing service

```
    cd customer-facing-system
    docker-compose up --build -d
```

- To deploy the backend system

```
    cd backend-system
    docker-compose up --build -d
```


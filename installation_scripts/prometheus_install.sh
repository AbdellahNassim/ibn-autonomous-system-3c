#!/bin/bash

# add helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
# create namespace for prometheus
kubectl create namespace prometheus


# deploy chart
helm install prometheus prometheus-community/kube-prometheus-stack -n prometheus

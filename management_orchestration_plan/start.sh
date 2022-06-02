#!/bin/bash 
cd e2e_orchestrator 
go mod download 

go build  -o e2e_orchestrator
./e2e_orchestrator &
#!/bin/bash 
cd e2e_orchestrator 
go mod download 

go build  -o e2e_orchestrator
cp .env.example .env
./e2e_orchestrator &
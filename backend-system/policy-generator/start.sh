#!/bin/bash
go build .
if [ $? -eq 0 ]
  then 
   ./policy-generator
  fi
 

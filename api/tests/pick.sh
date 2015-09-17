#!/bin/bash
curl -X POST  -H "Accept: Application/json" -H "Content-Type: application/json" http://127.0.0.1:8081/api/v1.0/pick/ -d "{\"dest\":$2}" --cookie "bibber=$1" -v | grep }| python -mjson.tool 

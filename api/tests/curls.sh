#!/bin/bash
curl -X POST  -H "Accept: Application/json" -H "Content-Type: application/json" http://127.0.0.1:8081/api/setup/ -d '{"num_players":"3"}'

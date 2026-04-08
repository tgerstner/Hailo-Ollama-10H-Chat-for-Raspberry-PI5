#!/usr/bin/bash 

json=$(curl -s http://localhost:8000/hailo/v1/list) 
echo "$json" | jq -r '.models[]'
echo 


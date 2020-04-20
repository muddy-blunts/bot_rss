#!/bin/bash
while true
do
 python3 main.py &
 PID=$!
 sleep 60
 kill -SIGKILL $PID
done
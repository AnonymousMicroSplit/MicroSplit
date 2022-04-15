#!/bin/bash
sudo apt update -y
sudo apt install python3-pip -y
pip3 install python-http-client

kubectl apply -f myver.yaml
kubectl get svc frontend |  awk '{print $3}' | sed 1d >> frontend.txt


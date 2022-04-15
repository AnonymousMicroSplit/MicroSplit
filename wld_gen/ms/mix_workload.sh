#!/bin/bash
echo "Enter the scenario name( i.e. edge, cloud, mix):"
read s
n=50
for u in 30 60 80 100 120 150 200 300 #90 120 #5  30  60 #70 80 100 120
do
        echo "Running Mix-workload experiments for $n  requests and $u concurrent users:"
        python3 all_requests.py $n $u $s
        sleep 5

done


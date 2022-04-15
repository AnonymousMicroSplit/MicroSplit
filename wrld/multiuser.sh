#!/bin/bash
echo "Enter the scenario name( i.e. edge, cloud, mix):"
read s
n=50
for u in 1 30 60 80 100 120 #120 150 #1  30 60 80 100 #90 120 #5  30  60 #70 80 100 120
do
	echo "Running multi-user experiments for $n  requests and $u users for request type 1-register user"
	c=1
	python3 register_par.py $n $u $s
	sleep 5
	
	echo "Running multi-user experiments for $n  requests and $u users for request type 2-Follow"
	c=2
	python3 follow_par.py $n $u $s
	sleep 5
	 
	echo "Running multi-user experiments for $n  requests and $u users for request type 3-compose-post"
        c=3
        python3 composepost_par.py $n $u $s
	sleep 5

	echo "Running multi-user experiments for $n  requests and $u users for request type 4-read-home-timeline"
	c=4
	python3 timeline_par.py $n $u $s 1
	sleep 5

	echo "Running multi-user experiments for $n  requests and $u users for request type 5-read-user-timeline"
        c=5
	python3 timeline_par.py $n $u $s 2
	sleep 5
done	
echo "All multi-user experiments for scenario $s are done now. In order to calculate the exact latency for request type 5 and 6, you must add request type 3 and request types 3+5 respectively (i.e. SCENARIO_mux_rt[3/5]_rx_ux)"

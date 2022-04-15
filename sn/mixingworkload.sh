#!/bin/bash
echo "Enter the scenario name( i.e. edge, cloud, mix):"
read s
n=50
for u in 5 10 # 20 30 40 50 60 70 80 100 120
do
	echo "Running multi-user experiments for $n  requests and $u users for request type 1-index"
	c=1
	python3 get_par_closed.py $n $u $s $c
	sleep 5

	echo "Running multi-user experiments for $n  requests and $u users for request type 2-setCurrency"
	c=2
	python3 setCurrency_par_closed.py $n $u $s 
	sleep 5
	 
	echo "Running multi-user experiments for $n  requests and $u users for request type 3-browseProduct"
        c=3
        python3 get_par_closed.py $n $u $s $c
	sleep 5

	echo "Running multi-user experiments for $n  requests and $u users for request type 4-viewCart"
        c=4
        python3 get_par_closed.py $n $u $s $c
	sleep 5

	echo "Running multi-user experiments for $n  requests and $u users for request type 5-(3+quantity)"
        c=5
        python3 quantity_par_closed.py $n $u $s
	sleep 5

	echo "Running multi-user experiments for $n  requests and $u users for request type 6-(5+checkout)"
        c=6
        python3 checkout_par_closed.py $n $u $s
	sleep 5
done	
echo "All multi-user experiments for scenario $s are done now. In order to calculate the exact latency for request type 5 and 6, you must add request type 3 and request types 3+5 respectively (i.e. SCENARIO_mux_rt[3/5]_rx_ux)"

#!/bin/bash
sudo kubectl -n social-network exec -it $1 -- tc filter add dev eth0 protocol ip parent 1: prio 1 u32 match ip src  $2 flowid 1:11
#sudo kubectl -n social-network exec -it $3 -- tc filter add dev eth0 protocol ip parent 1: prio 1 u32 match ip dst  $4 flowid 1:11

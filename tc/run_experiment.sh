#!/bin/bash 
INTERFACE=eth0
function start 
{
  # echo "amar: $2" 
  # start the amar_client, just commented the entry point 
  # docker stop amar_client
  # docker rm amar_client
  # mkdir -p /scratch/amardeep/$2
  # docker run -d --net=web_serving --cap-add=NET_ADMIN -v /scratch/amardeep/$2:/faban/output --name=amar_client amar_client sleep infinity
  # docker run -d --net=web_serving --cap-add=NET_ADMIN -v /scratch/amardeep/default_faban_output:/faban/output --name=amar_client amar_client sleep infinity
  # configure the client
  # docker exec amar_client apt install traceroute 
  #docker exec amar_client mkdir -p /usr/share/latency
  #docker cp client_latency_script.sh amar_client:/usr/share/latency
  #docker exec amar_client chmod +x /usr/share/latency/client_latency_script.sh
  #docker exec amar_client /usr/share/latency/client_latency_script.sh start

 
  
  # configure front-end
  #docker exec -ti --user root dockercompose_front-end_1 mkdir -p /usr/share/latency
  #docker cp frontend_latency.sh dockercompose_front-end_1:/usr/share/latency
  #docker exec -ti --user root dockercompose_front-end_1 chmod +x /usr/share/latency/frontend_latency.sh 
  #docker exec -ti --user root dockercompose_front-end_1 /usr/share/latency/frontend_latency.sh start
  
  

 
  #config edge_router
  docker exec -ti --user root dockercompose_edge-router_1 mkdir -p /usr/share/latency
  docker cp edge_frontend_latency.sh dockercompose_edge-router_1:/usr/share/latency
  docker exec -ti --user root dockercompose_edge-router_1 chmod +x /usr/share/latency/edge_frontend_latency.sh 
  docker exec -ti --user root dockercompose_edge-router_1 sh -c "/usr/share/latency/edge_frontend_latency.sh start"


  #config user
  #docker exec -ti --user root dockercompose_user_1 mkdir -p /usr/share/latency
  #docker cp user_latency.sh dockercompose_user_1:/usr/share/latency
  #docker exec -ti --user root dockercompose_user_1 chmod +x /usr/share/latency/user_latency.sh 
  #docker exec -ti --user root dockercompose_user_1 sh -c "/usr/share/latency/user_latency.sh start"

  #config catalouge
  #docker exec -ti --user root dockercompose_catalogue_1 mkdir -p /usr/share/latency
  #docker cp catalogue_latency.sh dockercompose_catalogue_1:/usr/share/latency
  #docker exec -ti --user root dockercompose_catalogue_1 chmod +x /usr/share/latency/catalogue_latency.sh 
  #docker exec -ti --user root dockercompose_catalogue_1 sh -c "/usr/share/latency/catalogue_latency.sh start"
  
  #config carts
  #docker exec -ti --user root dockercompose_carts_1 sh -c "apk update"
  #docker exec -ti --user root dockercompose_carts_1 sh -c "apk add iproute2"
  #docker exec -ti --user root dockercompose_carts_1 mkdir -p /usr/share/latency
  #docker cp carts_latency.sh dockercompose_carts_1:/usr/share/latency
  #docker exec -ti --user root dockercompose_carts_1 chmod +x /usr/share/latency/carts_latency.sh 
  #docker exec -ti --user root dockercompose_carts_1 sh -c "/usr/share/latency/carts_latency.sh start"

  #config order
  #docker exec -ti --user root dockercompose_orders_1 mkdir -p /usr/share/latency
  #docker cp order_latency.sh dockercompose_orders_1:/usr/share/latency
  #docker exec -ti --user root dockercompose_orders_1 chmod +x /usr/share/latency/order_latency.sh 
  #docker exec -ti --user root dockercompose_orders_1 sh -c "/usr/share/latency/order_latency.sh start"

  #docker exec -ti --user root dockercompose_front-end_1 /bin/sh -c "/usr/share/latency/frontend_latency.sh start"
  # web-server vs DB 
  # docker exec web_server tc qdisc add dev $INTERFACE parent 1:11 handle 11:0 netem delay 20ms
  # web-server vs memc
  # docker exec web_server tc qdisc add dev $INTERFACE parent 1:12 handle 12:0 netem delay 10ms 5ms 25% distribution normal

 

  # memc vs db
  # docker exec memcache_server tc qdisc add dev $INTERFACE parent 1:12 handle 12:0 netem delay 10ms 5ms 25% distribution normal 
   echo "successfull config network for all services"
}

function stop 
{
  #stop frontend latency
  #docker exec -ti --user root dockercompose_front-end_1 /usr/share/latency/frontend_latency.sh  stop 
  
  #stop edge router latency
  docker exec -ti --user root dockercompose_edge-router_1 /usr/share/latency/edge_frontend_latency.sh  stop
  
  #stop  user latency
  #docker exec -ti --user root dockercompose_user_1 /usr/share/latency/user_latency.sh  stop
  
  #stop  catalouge latency
  #docker exec -ti --user root dockercompose_catalogue_1 /usr/share/latency/catalogue_latency.sh  stop
  
  #stop  carts latency
  #docker exec -ti --user root dockercompose_carts_1 /usr/share/latency/carts_latency.sh  stop
  
   #stop  order latency
  #docker exec -ti --user root dockercompose_orders_1 /usr/share/latency/order_latency.sh  stop

}

function move 
{
  echo "folder name: $2"
  sudo chown -R amardeep:sudo /scratch/amardeep/default_faban_output/*
  mkdir -p /scratch/amardeep/$2
  mv /scratch/amardeep/default_faban_output/* /scratch/amardeep/$2 
}

function status 
{
  echo "container: $2"

  echo "Active Queue Disciplines for $INTERFACE"
  docker exec $2 tc -s qdisc show dev $INTERFACE
  echo 
  echo "Active Queueing Classes for $INTERFACE "
  docker exec $2 tc -s class show dev $INTERFACE
  echo 
  echo "Active Traffic Control Filters for $INTERFACE"
  docker exec $2 tc -s filter show dev $INTERFACE
}

function run
{
  start=`date +%s%N`;docker exec amar_client /etc/bootstrap.sh 172.20.240.2;end=`date +%s%N`;echo `expr $end - $start`
}
# main 
case "$1" in
  start)
    start $1
    ;;
  stop)
    stop
    ;;
  run)
    run $1
    ;;
  move)
    move $1 $2
    ;;
  status)
    status $1 $2
    ;;
  *)
    echo $"Usage: $0 {start|stop}"
    exit 1
esac

exit 0;

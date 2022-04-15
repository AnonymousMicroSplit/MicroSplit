#!/bin/bash

rm pods.txt
kubectl -n media-microsvc get po | awk '{print $1}'| sed 1d  >> pods.txt
rm svc_to_be_considered.txt
kubectl -n media-microsvc get svc | awk '{print $1}'| sed 1d | sed 7d  >> svc_to_be_considered.txt
rm frontend.txt
kubectl -n media-microsvc get svc nginx-web-server | awk '{print $3}' | sed 1d >> frontend.txt

pods=($(kubectl -n media-microsvc get po | awk '{print $1}'| sed 1d | tr '\n' ' '))
svcs=($(kubectl -n media-microsvc get svc | awk '{print $1}'| sed 1d | tr '\n' ' '))
echo $pods[1]
for p in "${pods[@]}" 
do
	#echo "pod: $p"
	os=$(kubectl -n media-microsvc exec -it $p cat /etc/os-release | grep 'ubuntu')
	echo $os
	if  [ -z "$os" ]; then
		#echo $os
		#echo "not ossssssssssssssss"
		kubectl -n media-microsvc exec -it  $p apk update
		kubectl -n media-microsvc exec -it $p apk add iproute2
	else
		#echo "is ubuntu"
		#echo $os
		kubectl -n media-microsvc exec -it $p apt-get update
		kubectl -n media-microsvc exec -it $p -- apt-get install -y iproute2
	fi
done


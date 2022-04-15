#!/bin/bash
app=social-network
rm pods.txt
kubectl -n $app get po | awk '{print $1}'| sed 1d  >> pods.txt
rm svc_to_be_considered.txt
kubectl -n $app get svc | awk '{print $1}'| sed 1d | sed 6d  >> svc_to_be_considered.txt
rm frontend.txt
kubectl -n $app get svc nginx-thrift | awk '{print $3}' | sed 1d >> frontend.txt

pods=($(kubectl -n $app get po | awk '{print $1}'| sed 1d | tr '\n' ' '))
svcs=($(kubectl -n $app get svc | awk '{print $1}'| sed 1d | tr '\n' ' '))
echo $pods[1]
for p in "${pods[@]}" 
do
	#echo "pod: $p"
	os=$(kubectl -n $app exec -it $p cat /etc/os-release | grep 'ubuntu')
	echo $os
	if  [ -z "$os" ]; then
		#echo $os
		#echo "not ossssssssssssssss"
		kubectl -n $app exec -it  $p apk update
		kubectl -n $app exec -it $p apk add iproute2
	else
		#echo "is ubuntu"
		#echo $os
		kubectl -n $app exec -it $p apt-get update
		kubectl -n $app exec -it $p -- apt-get install -y iproute2
	fi
done


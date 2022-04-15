kubectl -n social-network get po | awk '{print $1}'| sed 1d  >>  pods.txt
kubectl -n social-network get svc | awk '{print $1}'| sed 1d  >> svc_to_be_considered.txt
kubectl -n social-network  get svc nginx-thrift |  awk '{print $3}' |  sed 1d  >> frontend.txt

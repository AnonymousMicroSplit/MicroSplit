import os,subprocess

#Run setup_pod.sh
#do "kubectl -n social-network get po | awk '{print $1}'| sed 1d " and save the result into pods.txt
#do "kubectl -n social-network get svc | awk '{print $1}'| sed 1d  " and save the result into svc_to_beconsidered.txt
#Add front-end svc ip to frontend.txt
#add those you want to be deployed on the cloud side  in cloud.txt 
#Run this code
lines=[]
app='social-network'
e2c='30ms'
u2e='10ms'
frontend='nginx-thrift'
with open('./svc_to_be_considered.txt') as f:
    svcs = f.read().splitlines() #list of service names
with open('./pods.txt') as f:
    pods = f.read().splitlines() #list of pod names

svc_ips=[]
svc_pod=[]
#Service ips
for i in range(len(svcs)):
    _ip=os.popen("kubectl -n "+app+" get svc  "+svcs[i]+" |awk '{print $3}' | sed 1d").read()#.format(svcs[i])).read() #service ip
    svc_ips.append(_ip[:-1])

#List of pod names located in the cloud resources
with open('./cloud.txt') as f:
    cloud_pods = f.read().splitlines() #list of pod names located in the cloud

#Remove previous latency setup and add new setup for latency
commands=['tc qdisc del dev eth0 handle 1: root ',
        'tc qdisc add dev eth0 handle 1: root htb default 12',
        'tc class add dev eth0 parent 1: classid 1:1 htb rate 100Mbps',
        'tc class add dev eth0 parent 1:1 classid 1:11 htb rate 100Mbps',
        'tc class add dev eth0 parent 1:1 classid 1:12  htb rate 100Mbps',
        'tc class add dev eth0 parent 1:1 classid 1:13  htb rate 100Mbps',
        'tc qdisc add dev eth0 parent 1:11 handle 10:  netem delay '+e2c,
        'tc qdisc add dev eth0 parent 1:12 handle 20:  netem',
        'tc qdisc add dev eth0 parent 1:13 handle 30:  netem delay '+u2e]
for i in range(len(pods)):
    for j in range(len(commands)):
        comm="kubectl -n {0} exec {1} -it -- bash -c \" {2} \"".format(app,pods[i],commands[j])
        print(comm)
        os.system(comm)
    if svcs[i]==frontend: #U2E latency
        os.system("kubectl -n {0} exec  {1} -it -- bash -c \" tc filter add dev eth0 protocol ip parent 1: prio 1 u32 match ip src 192.168.235.192 flowid 1:13 \" ".format(app,pods[i]))
        os.system("kubectl -n {0}  exec  {1} -it  -- bash -c \" tc filter add dev eth0 protocol ip parent 1: prio 1 u32 match ip dst 192.168.235.192 flowid 1:13 \" ".format(app,pods[i]))

#Add latency for Edge->Cloud or Cloud->Edge services
for i in range(len(cloud_pods)):
    for j in range(len(svcs)):
        if cloud_pods[i]==pods[j]: # is not the same
            break
        if(pods[j] not in cloud_pods):  #check j is not in the CLOUD
            print('From {0} to {1}'.format(cloud_pods[i],pods[j]))
            #Get cloud_svc ip
            cloud_svc_ip=svc_ips[pods.index(cloud_pods[i])]
            svc_ip=svc_ips[j]
            print('{0} to {1}'.format(cloud_svc_ip,svc_ip))
            #Add latenct to FROM:
            comm="kubectl -n "+app+" exec "+  cloud_pods[i]+"  -it --  tc filter add dev eth0 protocol ip parent 1: prio 1 u32 match ip src " +svc_ip+" flowid 1:11 "
            print(comm)
            os.system(comm)
            comm="kubectl -n "+app+" exec "+  cloud_pods[i]+"  -it --  tc filter add dev eth0 protocol ip parent 1: prio 1 u32 match ip dst " +svc_ip+" flowid 1:11 "
            os.system(comm)
            #Add latency to TO:
            #We comment this serction because we just want to add latency from edge to cloud, not from cloud to edge!
            #comm="kubectl -n media-microsvc exec "+pods[j]+ " -it --  tc filter add dev eth0 protocol ip parent 1: prio 1 u32 match ip src "+cloud_svc_ip+ " flowid 1:11 "
            #print(comm)
            #os.system(comm)
            #comm="kubectl -n media-microsvc exec "+pods[j]+ " -it --  tc filter add dev eth0 protocol ip parent 1: prio 1 u32 match ip dst "+cloud_svc_ip+ " flowid 1:11 "
            #os.system(comm)

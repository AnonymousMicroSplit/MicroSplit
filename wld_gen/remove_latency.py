import os,subprocess

#print(os.system("pwd"))
#pods=os.popen("kubectl -n social-network get po | awk '{print $1}'| sed 1d | tr '\n' ' ' ").read().split()  #pod names list
#svcs=os.popen("kubectl -n social-network get svc | awk '{print $1}'| sed 1d | tr '\n' ' ' ").read().split() #service name list
#svc_ips=os.popen("kubectl -n social-network get svc | awk '{print $3}'| sed 1d | tr '\n' ' '").read().split() #service ip list
lines=[]

with open('./svc_to_be_considered.txt') as f:
    svcs = f.read().splitlines() #list of service names
with open('./pods.txt') as f:
    pods = f.read().splitlines() #list of pod names

svc_ips=[]
svc_pod=[]
#Service ips
for i in range(len(svcs)):
    _ip=os.popen("kubectl -n social-network get svc  "+svcs[i]+" |awk '{print $3}' | sed 1d").read()#.format(svcs[i])).read() #service ip
    svc_ips.append(_ip)

with open('./cloud.txt') as f:
    cloud_pods = f.read().splitlines() #list of pod names located in the cloud

#remove previous latency setup and add new setup for latency
commands=['tc qdisc del dev eth0 handle 1: root ']
for i in range(len(pods)):
    for j in range(len(commands)):
        #print("testttttttttttttttt\n")
        comm="kubectl -n social-network exec {0} -it -- bash -c \" {1} \"".format(pods[i],commands[j])
        print(comm)
        os.system(comm)



import http.client,time,sys,timeit,random
from multiprocessing import Pool,Process,Lock
import multiprocessing as mp,string, csv

output = mp.Queue()

def f(frontend,s,x,n,t,req,output):
    start=timeit.default_timer()
    sum_latency=0.0
    f1= open('./logs/'+s+'_mu'+str(t)+'rt'+str(req+3)+'_r'+str(n)+'_u'+str(x),'w')
    for i in range(n):    
        if req==1:
            r="/wrk2-api/home-timeline/read?"
        elif req==2:
            r="/wrk2-api/user-timeline/read?"
        idx=random.randint(1,962)
        start=random.random()*100
        stop=start+10
        r+='user_id='+str(idx)+'&start='+str(start)+'&stop='+str(stop)
        start=timeit.default_timer()
        conn = http.client.HTTPConnection(frontend+":8080")
        conn.request("GET", r)
        r1=conn.getresponse()
        end=timeit.default_timer()
        f1.write(str(end-start)+'\n')
        sum_latency+=(end-start)
        r1.read()
        time.sleep(random.random()*1.5+0.5)
        conn.close()
    f1.close()
    output.put(sum_latency)
    return
# num request, num users(thread), request_type
if __name__ =='__main__':
    print("Your arguments should have been 1-n(number of requests per user), 2-t ( number of users/threads), 3-scenario (i.e. edge/cloud/mix), and 4-req (i.e. 1-read-home-timeline 2-read-user-timeline)") 
    n=int(sys.argv[1])
    t=int(sys.argv[2])
    s=sys.argv[3]
    req=int(sys.argv[4])
    _s=open("frontend.txt",'r')
    fr=_s.read().split('\n')
    _s.close()
    print('Front end:' +fr[0]+":8080")
    processes = [mp.Process(target=f, args=(fr[0],s, x,n, t, req, output)) for x in range(t)]
    for p in processes:
        p.start()
    print("Start threads joining")
    for p in processes:
        p.join()
        time.sleep(random.random())
    results = [output.get() for p in processes]
    average=[_sum / n for _sum in results]
    print("Total latency of all requests for individual threads: ",results)
    print("Average latency of single request for individual threads: ",average)
    print("-----------------------------------------------------")
    print("Average latency of single request in all threads:",str(sum(average)/len(average)))
    print("Average total latency of all requests for threads",str(sum(results)/len(results)))

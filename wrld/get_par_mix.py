import http.client,time,sys,timeit,random
from multiprocessing import Pool,Process,Lock
import multiprocessing as mp,string, csv

output = mp.Queue()

def f(s,x,n,t,req,output):
    start=timeit.default_timer()
    sum_latency=0.0
    start=time.time()
    if req==1:
        r="/"
    elif req==3:
        r="/product/1YMWWN1N4O"
    elif req==4:
        r="/cart"
    else:
        r="F.."
    f1= open('./logs/'+s+'_mu'+str(t)+'rt'+str(req)+'_r'+str(n)+'_u'+str(x),'w')
    for i in range(n):    
        start=timeit.default_timer()
        conn = http.client.HTTPConnection("10.102.243.173:80")  
        conn.request("GET", r)
        r1=conn.getresponse()
        end=timeit.default_timer()
        f1.write(str(end-start)+'\n')
        sum_latency+=(end-start)
        r1.read()
        time.sleep(0.5+random.random()*1.5)
        conn.close()
    f1.close()
    output.put(sum_latency)
    return
# num request, num users(thread), request_type
if __name__ =='__main__':
    print("Your arguments should have been 1-n(number of requests per user), 2-t ( number of users/threads), 3-scenario (i.e. edge/cloud/mix), and 4-req (i.e. 1-index 3-browseProduct 4-viewCart)") 
    n=int(sys.argv[1])
    t=int(sys.argv[2])
    s=sys.argv[3]
    req=int(sys.argv[4])
    processes = [mp.Process(target=f, args=(s, x,n, t, req, output)) for x in range(t)]
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

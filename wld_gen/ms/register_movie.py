import http.client,time,sys,timeit,urllib,random
from multiprocessing import Pool,Process,Lock
import multiprocessing as mp
import string

output = mp.Queue()

def f(fr,s,x,n,output):
    headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}
    f1= open('./logs/'+s+'_mu'+str(t)+'rt2'+'_r'+str(n)+'_u'+str(x),'w')
    sum_latency=0
    for i in range(n):
        idx=str(random.randint(10000,1000000))
        letters = string.ascii_lowercase
        movie_id='movie_'+str(random.randint(1,900000))#'1179651'
        title=''.join(random.choice(letters) for i in range(256))
        params=urllib.parse.urlencode({'title':title,'movie_id':movie_id})
        start=time.time()
        conn = http.client.HTTPConnection(fr+":8080")
        conn.request("POST","/wrk2-api/movie/register",params,headers)
        r1=conn.getresponse()
        diff=time.time()-start
        f1.write(str(diff)+'\n')
        sum_latency+=diff
        r1.read()
        time.sleep(random.random()*1.5+0.5)#1.5+.5)
        conn.close()
    f1.close()
    output.put(sum_latency)

# num request, num users(thread), request_type
if __name__ =='__main__':
    print("Your arguments should have been n(number of requests per user), t ( number of users/threads), command") 
    n=int(sys.argv[1])
    t=int(sys.argv[2])
    s=sys.argv[3]
    _s=open("frontend.txt",'r')
    fr=_s.read().split('\n')
    _s.close()
    print('Front end:' +fr[0]+":8080")
    processes = [mp.Process(target=f, args=(fr[0],s,x,n,output)) for x in range(t)]
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

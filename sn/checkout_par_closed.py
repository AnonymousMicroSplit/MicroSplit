import http.client,time,sys,timeit,urllib,random
from multiprocessing import Pool,Process,Lock
import multiprocessing as mp
import string

output = mp.Queue()

def f(fr,s,x,n,output):
    params=urllib.parse.urlencode({'email':'someone@example.com',
                                   'street_address':'1600 Amphitheatre Parkway',
                                   'zip_code':'94043',
                                   'city':'Mountain view',
                                   'state':'CA',
                                   'country':'United States',
                                   'credit_card_number':'4432-8015-6152-0454',
                                   'credit_card_expiration_month':'1',
                                   'credit_card_expiration_year':'2039',
                                   'credit_card_cvv':'672'})
    headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}
    sum_latency=0
    f1= open('./logs/'+s+'_mu'+str(t)+'rt6'+'_r'+str(n)+'_u'+str(x),'w')
    for i in range(n):
        start=time.time()
        conn = http.client.HTTPConnection(fr+":80")
        conn.request("POST","/cart/checkout",params,headers)
        r1=conn.getresponse()
        diff=time.time()-start
        f1.write(str(diff)+'\n')
        sum_latency+=diff
        r1.read()
        time.sleep(random.random()*1.5+0.5)
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
    print('Front end:' +fr[0]+":80")
    processes = [mp.Process(target=f, args=(fr[0],s,x,n, output)) for x in range(t)]
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

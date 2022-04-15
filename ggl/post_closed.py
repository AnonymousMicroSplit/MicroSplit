import http.client,time,sys,urllib.parse
start=time.time()
n=int(sys.argv[1])
print("Parameters should have been n( number of requests)") 
params=urllib.parse.urlencode({'currency_code':'AUDdd'})
headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}
sum_latecy=0
start=time.time()
for i in range(10):
    start=time.time()
    conn = http.client.HTTPConnection("10.102.243.173:80")
    conn.request("POST","/setCurrency",params,headers)
    r1=conn.getresponse()
    sum_latency+=time.time()-start
    r1.read()
conn.close()
print("Average per request latency:",str(sum_latency/n))
print("Total latency:",sum_latency)

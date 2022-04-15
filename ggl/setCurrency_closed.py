import http.client,time,sys,urllib.parse
start=time.time()
#s=sys.argv[1]
n=int(sys.argv[1])
print("parameters must be n(number of requests)")
params=urllib.parse.urlencode({'currency_code':'EUR'})
headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}
sum_latency=0
for i in range(n):
    start=time.time()
    conn = http.client.HTTPConnection("10.102.243.173:80")
    conn.request("POST","/setCurrency",params,headers)
    r1=conn.getresponse()
    sum_latency+=(time.time()-start)
    r1.read()
    conn.close()
print("Average per request latency:",str(sum_latency/n))
print("Total latency:",sum_latency)

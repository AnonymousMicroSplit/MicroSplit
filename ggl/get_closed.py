import http.client,time,sys
start=time.time()
s=sys.argv[2]
n=int(sys.argv[1])
sum_latency=0.0
start=time.time()
for i in range(n):    
    start=time.time()
    conn = http.client.HTTPConnection("10.102.243.173:80")
    conn.request("GET", s)
    r1=conn.getresponse()
    end=time.time()
    count=end-start
    #print("latency=",count)
    sum_latency+=count
    r1.read()
conn.close()
print("Sum latency:", sum_latency)
print("Avg latency:",str(sum_latency/n))

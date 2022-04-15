import http.client,time,sys,urllib.parse
start=time.time()
#s=sys.argv[1]
n=int(sys.argv[1])
print("parameters must be n(number of requests)")
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
for i in range(n):
    start=time.time()
    conn = http.client.HTTPConnection("10.102.243.173:80")
    conn.request("POST","/cart/checkout",params,headers)
    r1=conn.getresponse()
    sum_latency+=(time.time()-start)
    r1.read()
    conn.close()
print("Average per request latency:",str(sum_latency/n))
print("Total latency:",sum_latency)

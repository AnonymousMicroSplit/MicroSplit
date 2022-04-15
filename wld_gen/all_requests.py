import http.client,time,sys,timeit,urllib,random
from multiprocessing import Pool,Process,Lock
import multiprocessing as mp
import string, json

output = mp.Queue()

def decRandom(length):
    a=['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    if(length>0):
        return decRandom(length-1)+a[random.randint(0,9)]
    else:
        return ''
def f(fr,s,x,n,output):
    headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}
    letters = string.ascii_lowercase
    f1= open('./logs/'+s+'_mu'+str(t)+'rt1'+'_r'+str(n)+'_u'+str(x),'w')
    sum_latency=0.0
    for i in range(n):
        command=random.randint(1,5) #we use 1,5 for edge scenario
        diff=0.0
        if command==1:
            idx=str(random.randint(10000,1000000))
            first_name='first_name_'+idx
            last_name='last_name'+idx
            username='username_'+idx
            password='password_'+idx
            user_id='user_id_'+idx
            params=urllib.parse.urlencode({'first_name':first_name,'last_name':last_name,'username':username,'password':password,'user_id':user_id})
            start=time.time()
            conn = http.client.HTTPConnection(fr+":8080")
            conn.request("POST","/wrk2-api/user/register",params,headers)
            r1=conn.getresponse()
            diff=time.time()-start
            f1.write(str(diff)+'\n')
            sum_latency+=diff
            r1.read()
            time.sleep(random.random()*1.5+0.5)#1.5+.5)
            conn.close()
        elif command==2:
            idx1=str(random.randint(1,962))
            username='user_name_'+idx1
            idx2=str(random.randint(1,962))
            followee='user_name_'+idx2
            params=urllib.parse.urlencode({'user_name':username,'followee_name':followee})
            start=time.time()
            conn = http.client.HTTPConnection(fr+":8080")
            conn.request("POST","/wrk2-api/user/follow",params,headers)
            r1=conn.getresponse()
            #response=requests.post('http://'+fr+':8080'+"/wrk2-api/user/follow",data=params)
            #diff=response.elapsed.total_seconds()
            r1.read()
            diff=time.time()-start
            f1.write(str(diff)+'\n')
            sum_latency+=diff
            #r1.read()
            time.sleep(random.random()*1.5+0.5)
            conn.close()    
        elif command==3:
            idx=str(random.randint(1,962))
            username='user_name_'+idx
            user_id=idx
            letters = string.ascii_lowercase
            text= ''.join(random.choice(letters) for i in range(256))
            num_media=random.randint(0,4)
            num_urls=random.randint(0,5)
            num_user_mentions=random.randint(0,5)
            media_ids='['
            media_types='['
            for i in range(num_user_mentions):
                user_mention_id=0
                while(True):
                    user_mention_id=random.randint(1,962)
                    if user_id != user_mention_id:
                        break
                text= text+"@username_"+str(user_mention_id)
            for i in range(num_urls):
                text=text+" http://"+''.join(random.choice(letters) for i in range(64))
            for i in range(num_media):
                media_id=decRandom(18)
                media_ids=media_ids+"\""+media_id+"\","
                media_types= media_types+"\"png\","
            if num_media>0:
                media_ids=media_ids[:-1]
                media_types=media_types[:-1]
            media_ids=media_ids+']'
            media_types=media_types+']'
            #print('media_ids=',media_ids)
            #print('media_types=',media_types)
            params=""
            if num_media ==0:
                params=urllib.parse.urlencode({'username':username,'user_id':user_id,'text':text,'media_ids':media_ids,'post_type':'0'})
            else:
                params=urllib.parse.urlencode({'username':username,'user_id':user_id,'text':text,'media_ids':media_ids,'media_types':media_types,'post_type':'0'})
            headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
            start=time.time()
            conn = http.client.HTTPConnection(fr+":8080")
            conn.request("POST","/wrk2-api/post/compose",params,headers)
            #diff=time.time()-start
            r1=conn.getresponse()
            diff=time.time()-start
            f1.write(str(diff)+'\n')
            sum_latency+=diff
            r1.read()
            time.sleep(random.random()*1.5+0.5)
            conn.close()
        elif command==4:
            r="/wrk2-api/home-timeline/read?"
            idx=random.randint(1,962)
            start=random.random()*100
            stop=start+10
            r+='user_id='+str(idx)+'&start='+str(start)+'&stop='+str(stop)
            start=timeit.default_timer()
            conn = http.client.HTTPConnection(fr+":8080")
            conn.request("GET", r)
            r1=conn.getresponse()
            end=timeit.default_timer()
            f1.write(str(end-start)+'\n')
            sum_latency+=(end-start)
            r1.read()
            time.sleep(random.random()*1.5+0.5)
            conn.close()
        elif command==5:
            r="/wrk2-api/user-timeline/read?"
            idx=random.randint(1,962)
            start=random.random()*100
            stop=start+10
            r+='user_id='+str(idx)+'&start='+str(start)+'&stop='+str(stop)
            start=timeit.default_timer()
            conn = http.client.HTTPConnection(fr+":8080")
            conn.request("GET", r)
            r1=conn.getresponse()
            end=timeit.default_timer()
            f1.write(str(end-start)+'\n')
            sum_latency+=(end-start)
            r1.read()
            time.sleep(random.random()*1.5+0.5)
            conn.close()
        f1.write(str(diff)+'\n')
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

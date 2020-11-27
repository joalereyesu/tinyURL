from redis import Redis
import os
#from redisworks import Root
import random, string
import json
from datetime import date, datetime

#conn = Redis('localhost')
REDIS_HOST = os.getenv("REDIS_HOST", None)
conn = Redis(host=REDIS_HOST, port=6379, decode_responses=True)

def generateRandomKey ():
    key = string.ascii_lowercase + string.digits
    randomKey = ''.join((random.choice(key) for i in range(8)))
    return randomKey


def setNewLink (token, link):
    visits = 0
    today_date = datetime.now()
    now = today_date.strftime("%d/%m/%Y %I:%M%p")
    dic = {'url': link, 'visits': visits, 'time': now}
    val = json.dumps(dic)
    conn.hset("linkServer", token, val)
 
def getLink (token):
    miniDic = conn.hget("linkServer", token)
    pyDic = json.loads(miniDic)
    return pyDic['url']

def getInfo (token):
    miniDic = conn.hget("linkServer", token)
    pyDic = json.loads(miniDic)
    return pyDic

def getAllLinks ():
    redisDic = conn.hgetall("linkServer")
    for key, val in redisDic.items():
        redisDic[key] = json.loads(val)
    return redisDic


def deleteURL (token):
    conn.hdel("linkServer", token)

def setNewVisit (token):
    miniDic = conn.hget("linkServer", token)
    pyDic = json.loads(miniDic)
    visit = pyDic['visits']
    newVisit = visit + 1
    pyDic['visits'] = newVisit
    strDic = json.dumps(pyDic)
    conn.hset("linkServer", token, strDic)



#print(link)
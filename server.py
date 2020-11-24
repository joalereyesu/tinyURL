from redis import Redis
#from redisworks import Root
import random, string
import json

#conn = Redis('localhost')
conn = Redis(host = 'localhost', port = 6379, charset="utf-8", decode_responses = True)    

def generateRandomKey ():
    key = string.ascii_lowercase + string.digits
    randomKey = ''.join((random.choice(key) for i in range(8)))
    return randomKey


def setNewLink (token, link):
    visits = 0
    dic = {'url': link, 'visits': visits}
    val = json.dumps(dic)
    conn.hset("linkServer", token, val)

def getLink (token):
    miniDic = conn.hget("linkServer", token)
    pyDic = json.loads(miniDic)
    return pyDic['url']

def getAllLinks ():
    nuevo = {}
    redisDic = conn.hgetall("linkServer")
    for key, val in redisDic.items():
        redisDic[key] = json.loads(val)
    return redisDic


def deleteURL (token):
    conn.hdel("linkServer", token)
    #conn.hdel("linksVisits", token)

def setNewVisit (token):
    miniDic = conn.hget("linkServer", token)
    pyDic = json.loads(miniDic)
    visit = pyDic['visits']
    newVisit = visit + 1
    pyDic['visits'] = newVisit
    strDic = json.dumps(pyDic)
    conn.hset("linkServer", token, strDic)

def getVisit (token):
    return conn.hget("linksVisits", token)

def getAllLinksVisits():
    return conn.hgetall("linksVisits")

#print(link)
from redis import Redis
import random, string

#conn = Redis('localhost')
conn = Redis(host = 'localhost', port = 6379, charset="utf-8", decode_responses = True)
linksServer = {}
#conn.hmset("linkServer", linksServer)

def generateRandomKey (domain):
    key = string.ascii_lowercase + string.digits
    randomKey = ''.join((random.choice(key) for i in range(8)))
    result = domain + randomKey
    return result

def generateOptionalKey (optional, domain):
    result = domain + optional
    return result

def setNewLink (token, link):
    conn.hset("linkServer", token, link)

def getLink (token):
    return conn.hget("linkServer", token)

def getAllLinks ():
    return conn.hgetall("linkServer")




print(conn.hgetall("linkServer"))
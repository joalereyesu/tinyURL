from redis import Redis
import random, string

#conn = Redis('localhost')
conn = Redis(host = 'localhost', port = 6379, charset="utf-8", decode_responses = True)

def generateRandomKey ():
    key = string.ascii_lowercase + string.digits
    randomKey = ''.join((random.choice(key) for i in range(8)))
    return randomKey


def setNewLink (token, link):
    conn.hset("linkServer", token, link)
    visits = 0
    conn.hset("linksVisits", token, visits)

def getLink (token):
    return conn.hget("linkServer", token)

def getAllLinks ():
    return conn.hgetall("linkServer")

def deleteURL (token):
    conn.hdel("linkServer", token)

def setNewVisit (token):
    visits = getVisit(token)
    visits =+1
    conn.hset("linksVisits", token, visits)

def getVisit (token):
    return conn.hget("linksVisits", token)

def getAllLinksVisits():
    return conn.hgetall("linksVisits")

#print(link)

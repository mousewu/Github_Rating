import pymongo as pm
from pymongo import MongoClient
import json

client=MongoClient("mongodb://localhost:27017/")
db=client.rating
def get_cursor(collection):
    return db[collection]

def get_num(a):
    l=0
    for i in a:
       l+=len(i)
    return l
    
def get_server_cursor(collection):
    uri='mongodb://longhashdba:longhash123QAZ@47.96.30.45/data_service'
    remote_client=MongoClient(uri)
    return remote_client['data_service'][collection]
def get_remote_cursor(collection):
    uri='mongodb://longhashdba:longhash123QAZ@47.96.30.45/bitcoin'
    remote_client=MongoClient(uri)
    return remote_client[collection]
if __name__=="__main__":
    c=get_cursor('sss')
    contrs=c.find()
    l=[]
    for i in contrs:
        ss=i.get('contributors',[[]])
        for j in ss:
            for t in j:
                l.append(t['id'])
        
    related=get_cursor('related_repos_contributors')
    l2=[]
    relates=related.find()
    for i in relates:
        if i.get('id'):
            l2.append(i.get('id'))
    l1=set(l)
    l3=set(l2)
    print(l2)
    lap=0
    print(len(l1))
    print(len(l3))
    
    
    
    for member in l1:
        if member in l3:
            lap+=1
    print(lap)

    
    

import sys
sys.path.append("/home/ywsun/")


from Github_rating.connect_tools import *
import requests
import json
from Github_rating.tools import *
cursor=get_server_cursor('members')

start=21
num=100
members=cursor.find().skip(start).limit(num)
members=list(members)
print(len(members))
for member in members:
    print(member['id'])
    if member.get('update'):
        continue
        
    repos=[]
    for reps in member['repos']:
        for rep in reps:
            events_url=rep['events_url'].split('{')[0]
            subscribers_url=rep['subscribers_url'].split('{')[0]
            commits_url=rep['commits_url'].split('{')[0]
            comments_url=rep['comments_url'].split('{')[0]
            issue_comments_url=rep['issue_comment_url'].split('{')[0]
            issues_url=rep['issues_url'].split('{')[0]
            rep['events_count']=get_page_num(events_url)
            rep['subscribers_count']=get_page_num(subscribers_url)
            rep['commits_count']=get_page_num(commits_url)
            rep['comments_count']=get_page_num(comments_url)
            rep['issue_comments_count']=get_page_num(issue_comments_url)
            rep['issues_count']=get_page_num(issues_url)
            repos.append(rep)
            #print(rep)
    cursor.update_many({'id':member['id']},{'$set':{'repos':repos}})
    cursor.update_many({'id':member['id']},{'$set':{'update':True}})
    start+=1
    print('********Here is the index!**********',start)
            
            
    

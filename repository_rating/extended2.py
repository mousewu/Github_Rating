import sys
import time
import traceback
sys.path.append("/home/ywsun/")
from requests.exceptions import ConnectionError
from pymongo.errors import CursorNotFound
from Github_rating.connect_tools import *
import requests
import json
from Github_rating.tools import *
cursor=get_server_cursor('members')
new_cursor=get_server_cursor('selected_members')
num = int(sys.argv[1])
try:
    with open('save{}.json'.format(num) )as f:
        j=json.load(f)
except:
    j=[200]

def get_rep_num(repos):
    n=0
    for reps in repos:
        n+=len(reps)
    return n
    

start = j[-1]
nums = 2000
while start < (num-1)*10000:
    try:
        members = cursor.find().skip(start).limit(nums)
        for member in members:
            try:
                print(member.get('id'))
                if member.get('update'):
                    start+=1
                    continue
                n=get_rep_num(member['repos'])
                repos=[]
                n_rep=0
                for reps in member['repos']:
                    for rep in reps:
                        n_rep+=1
                        if n_rep%5==0:
                            print(n_rep,'/',n,end=' ')
                        try:
                            if isinstance(rep,dict):
                                if(rep['stargazers_count'] or rep['watchers_count']
                                 or rep['forks'] ):
                                    
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
                                    print(rep['events_url'], time.asctime(time.localtime(time.time())))
                        except ConnectionError as r:
                            print('********connect ERROR*******')
                            time.sleep(10)
                        #print(rep)
                member['repos']=repos
                member.pop('_id')
                new_cursor.insert_one(member)
                try:
                    cursor.update_many({'id':member['id']},{'$set':{'update':True}})
                except Exception as e:
                    traceback.print_exc()
                    print('cursor_update_error')
                start+=1
                print('********Here is the index! at member loop**********',start)
            except Exception as e:
                print(e)
                start += 1
                print('iter_error!')
                traceback.print_exc()
    except CursorNotFound as ce:
        print('********pymongo not found cursor error*******')
        time.sleep(10)
        continue
    else :
        traceback.print_exc()
        print('********Here is the index! at last**********',start)
        print('all_structure_problem')
        j.append(start)
       
        with open('save{}.json'.format(num), 'w')as f:
            json.dump(j, f)

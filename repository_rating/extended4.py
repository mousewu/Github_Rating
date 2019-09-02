import sys
sys.path.append("/home/ywsun/")
import trackback


from Github_rating.connect_tools import *
import requests
import json
from Github_rating.tools import *
cursor=get_server_cursor('members')
new_cursor=get_server_cursor('selected_members')
try:
	with open('save4.json')as f:
		j=json.load(f)
except:
	j=[20000]
start=j[-1]
num=2000
members=cursor.find().skip(start).limit(num)
try:
	for member in members:
		print(member.get('id'))
		if member.get('update'):
			start+=1
			continue
			
		repos=[]
		for reps in member['repos']:
			for rep in reps:
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
						print(rep['events_url'])						
				#print(rep)
		member['repos']=repos
		member.pop('_id')
		new_cursor.insert_one(member)
		try:
		  cursor.update_many({'id':member['id']},{'$set':{'update':True}})
		except:
		  pass
		start+=1
		print('********Here is the index!**********',start)
except Exception as e:
	trackbcak.print_exc()
	print('********Here is the index!**********',start)
	j.append(start)
	with open('save4.json','w')as f:
		json.dump(j,f)
            
    

            
    

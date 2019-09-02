import json
import requests
import random
import re
import time
s=requests.Session()
id=['sunyiwei24601']
s.auth=('sunyiwei24601','d6cd802b17e4382c1bcea961e1f6cd4ee0fa8a35')

def get_headers():
    tokens=[
        # '9a9c1d46c47f75f57aa382d76b0b0ed98b71ffcc',
        'd6cd802b17e4382c1bcea961e1f6cd4ee0fa8a35',
        '37778db34015b99bdb6ba164e93ef7f105fac4cc',
    ]
    headers={
        'Authorization':'token '+random.choice(tokens),
        'Accept'       :'application/vnd.github.v3.star+json,'
                        'application/vnd.github.symmetra-preview+json,'
                        'application/vnd.github.squirrel-girl-preview,'
                        'application/vnd.github.hellcat-preview+json,'
                        'application/vnd.github.mercy-preview+json,'
        
    }
    return headers

def get_tools(url):
    r=requests.get(url,headers=get_headers())
    j=json.loads(r.text)
    return j

def page_preview(link):
    if link :
        try:
            c=re.findall('.+page=(.+)>; rel="last"',link)
            return int(c[0])
        except:
            print(link)
            return 1
    else: return 1
    
    
def pages_tool(url):
    next=[url]
    n=0
    while(len(next)!=0):
        if(n%20==0):
            print(url)
        n+=1
        
        url=next[0]
        r=requests.get(url,headers=get_headers())
        j=json.loads(r.text)
        
        if(isinstance(j,dict) and j.get('message')):
            return []
        h=r.headers
        head=dict(h)
        if n==1:
            t=page_preview(head.get('Link',None))
            
            # if t>20:
            #     print(t)
            #     print(url)
            #     print('too long to catch ')
            #     return []
            #     break
        if(head.get('Link')):
            link=head['Link']
            next=re.findall('.*<(.*?)>; rel="next"',link)
            yield json.loads(r.text)
        else:
            yield j
            next=[]
#获取user的内容
def get_user(name):
    url='https://api.github.com/users/'+name
    print(url)
    response=requests.get(url,headers=get_headers())
    
    j=json.loads(response.text)
    return j
#得到user或org的repos
def get_repos(type,name):
    url='https://api.github.com/'+type+'/'+name+'/repos'
    print(url)
    response=requests.get(url,headers=get_headers())
    
    j=json.loads(response.text)
    return j
#根据组织名得到他的详细信息，如果不是就转到getuser
def get_ogz(org):
    url='https://api.github.com/orgs/'+org
    print(url)
    response=requests.get(url,headers=get_headers())
    
    j=json.loads(response.text)
    if (j.get('type')):
        return j
    else:
        return (get_user(org))
#得到具体的repos的细节
def get_repos_details(repo):
    basic=['id','node_id','name','full_name','owner','html_url','private','created_at','updated_at',
              'pushed_at','size','stargazers_count','watchers_count','forks']
    url_name=['url','teams_url','events_url','issue_events_url','assignees_url','languages_url'
              ,'contributors_url','stargazers_url','merges_url','issues_url','milestones_url',
              ]
    'collaborators_url'
    
    repo['detail']=get_tools(repo['url'])
    for u in url_name[1:]:
        repo[u[:-4]]=list(pages_tool(repo[u].split('{')[0]))
#获取用户的细节
def get_user_details(name):
    details={}
    url='https://api.github.com/users/{}'.format(name)
    detail=get_tools(url)
    details['detail']=detail
    basic=['followers_url','starred_url','subscriptions_url']
    for url in basic:
        #通过对{进行分割来得到前面无损的url
        uu=detail[url].split('{')[0]
        details[url[:-4]]=list(pages_tool(uu))
    return details
#获取大致的数量，3页以内精确计算，三页以上n*30模糊计算
def get_page_num(url):
    response=requests.get(url,headers=get_headers())
    headers=response.headers
    
    link=headers.get('Link')
    
    page_num=page_preview(link)
    n=(page_num-1)*30
    last_url=url+'?page='+str(page_num)
    #print(last_url,end=' ')
    j=get_tools(last_url)
    if random.random()<0.01:
        if len(j)>0:
           print(j[0])
    n=n+len(j)
    #print(n)
    return n
    
    
    
if __name__=='__main__':
    link='https://api.github.com/repos/ethereum/go-ethereum/commits'
    a=get_page_num(link)
    print(a)
    

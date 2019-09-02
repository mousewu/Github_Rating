# -*- coding: utf-8 -*-
import scrapy
import sys
import random
import time
import json
import threading
from scrapy import Request
import re
import requests
from lxml import etree

S = 'issues_detail'
sys.path.append(r'/home/ywsun/')
from Github_rating.tools import *
from Github_rating.connect_tools import *

# from Gitrating.connect_tools import *
# from Gitrating.tools import *


def get_headers():
    tokens = [
        # '9a9c1d46c47f75f57aa382d76b0b0ed98b71ffcc',
        'd6cd802b17e4382c1bcea961e1f6cd4ee0fa8a35',
        '37778db34015b99bdb6ba164e93ef7f105fac4cc',
    ]
    headers = {
        'Authorization': 'token ' + random.choice(tokens),
        'Accept':        'application/vnd.github.v3.star+json,'
                         'application/vnd.github.symmetra-preview+json,'
                         'application/vnd.github.squirrel-girl-preview,'
                         'application/vnd.github.hellcat-preview+json,'
                         'application/vnd.github.mercy-preview+json,'
        
    }
    return headers


def thr_get_num(url, rep, name):
    rep[name] = get_page_num(url)
    
    
class FeatureSpider(scrapy.Spider):
    name = 'feature'
    allowed_domains = ['api.github.com']
    cursor = get_server_cursor('members')
    i_cursor = get_server_cursor('member_rep')
    members = list(cursor.find().skip(30100).limit(1000))
    repos = []
    
    def start_requests(self):
        n = 0
        for member in self.members:
            print(n)
            n+=1
            if not member.get('update'):
                for reps in member.get('repos'):
                    for rep in reps:
                        if isinstance(rep, dict):
                            if (rep['stargazers_count'] or rep['watchers_count']
                                    or rep['forks']):
                                url = 'http://www.baidu.com'
                                r = Request(url=url, meta={'rep': rep}, callback=self.parse, dont_filter=True)
                                yield r
                self.cursor.update_many({'id': member['id']}, {'$set': {'update': True}})
    


    def parse(self, response):
        a=time.time()
        rep = response.meta['rep']
        events_url = rep['events_url'].split('{')[0]
        subscribers_url = rep['subscribers_url'].split('{')[0]
        commits_url = rep['commits_url'].split('{')[0]
        comments_url = rep['comments_url'].split('{')[0]
        issue_comments_url = rep['issue_comment_url'].split('{')[0]
        issues_url = rep['issues_url'].split('{')[0]
        # threads = []
        #
        # threads.append(threading.Thread(target=thr_get_num, args=(events_url, rep, 'events_count')))
        # threads.append(threading.Thread(target=thr_get_num, args=(subscribers_url, rep, 'subscribers_count')))
        # threads.append(threading.Thread(target=thr_get_num, args=(commits_url, rep, 'commits_count')))
        # threads.append(threading.Thread(target=thr_get_num, args=(comments_url, rep, 'comments_count')))
        # threads.append(threading.Thread(target=thr_get_num, args=(issue_comments_url, rep, 'issue_comments_count')))
        # threads.append(threading.Thread(target=thr_get_num, args=(issues_url, rep, 'issues_count')))
        #
        # for jj in threads:
        #     jj.start()
        rep['events_count'] = get_page_num(events_url)
        rep['subscribers_count'] = get_page_num(subscribers_url)
        rep['commits_count'] = get_page_num(commits_url)
        rep['comments_count'] = get_page_num(comments_url)
        rep['issue_comments_count'] = get_page_num(issue_comments_url)
        rep['issues_count'] = get_page_num(issues_url)
        # for jj in threads:
        #     jj.join()
        rep['login'] = rep.get('owner').get('login')
        b=time.time()
        
        print(rep['events_url'], time.asctime(time.localtime(time.time())), print(b-a))
        self.i_cursor.insert_one(rep)

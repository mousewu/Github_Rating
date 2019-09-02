import numpy
import pymongo
import pandas
from Gitrating.connect_tools import *
cursor=get_cursor('members')
members=cursor.find().skip(20).limit(100)
data=pandas.DataFrame()
for member in list(members):
    
    for reps in member['repos']:
        for rep in reps:
            columns=['id','fork','size','stargazers_count','forks_count',
                     'open_issues_count','language']
            r={}
            for col in columns:
                r[col]=rep[col]
            d=pandas.Series(r)
            print(d)
            data=data.append(d,ignore_index=True)

            
            
            
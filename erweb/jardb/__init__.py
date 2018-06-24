'''
Jardb is a small document oriented database, which is Nosql, easy to use and tiny.
It is suitable for local applications to save data and configurations.

Jardb use no more than Python Standard Library.

Usage:

>>> import jardb

# Open databse
>>> db = jardb.jardb('json://database.db') 

>>> content = {"Users":[{},[{"Name": "123", "ps": "123"}, {"Name": "1234", "ps": "1234"}]],\
        "Article":[{}, [{"Name": "xxx", "Author": "123"}]], "config": {"user": 1, "secure": 2}}

# Use dict to initialize
>>> db.create(content)

# Create table 
>>> db.create_table('Blog',{'id':['AutoIncrease','Unique'],'data':['NotNull','Unique']})

# Select table
>>> col = db.get_table('Blog')

# Insert
>>> col.add({'data':1,'star':True,'admin':False,'Username':'1'})

# Easy to query
>>> 

# Use python-like language to select and remove
>>> col.filter("$data %3 == 0").remove()

# Change records
>>> col.update({'star':False,'ad':True})

# Close database
>>> db.close


Copyright (c) 2018, Chen Lutong.
License: MIT
'''


__author__ = 'Chen Lutong'
__license__ = 'MIT'
__version__ = '0.0.5'

from erweb.jardb.jardb import jardb
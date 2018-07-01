'''
middleware.py
~~~~~~~~~~~~~~
This is middleware.py

'''

from erweb.erweb import defaultapp

class middleware:
    def __init__(self):
        self.core = defaultapp
        self.middleware = []

    def add_middleware(self,mid):
        self.middleware.append(mid)

    
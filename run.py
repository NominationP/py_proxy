#!/usr/bin/env python
# coding:utf8

'''

function : clean_proxy (collecct--->check---->save)
author   : Zhangze
date     : 2016-12-15

'''


import sys
reload(sys)
sys.setdefaultencoding('utf8')
import threading
import urllib2
import urllib
import time
import threading
import json
from bs4 import BeautifulSoup
from multiprocessing import pool
from multiprocessing.dummy import Pool as ThreadPool
from save_mysql import Mysql
from clean_proxy import Clean_proxy
from agent import Proxy


# get proxy ip from diff url save to proxy.txt
pr = Proxy()
pr.run()

# collect and check proxy ip from source file and database and update database
cl = Clean_proxy()
cl.run()





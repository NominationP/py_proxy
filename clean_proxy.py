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

'''

class name  : Clean_proxy

method      :   __init__
                check_proxy
                collect_proxy
                thread_check
                save_proxy
                run
'''

class Clean_proxy:

    def __init__(self):


        self.lock = threading.Lock()

        self.sum_count = 0
        self.work_count = 0
        self.bad_count = 0
        # proxy source
        self.fr = open('proxy.txt', 'r')
        # good proxy save local add
        self.fw = fw = open('proxy_clean.txt', 'w')
        # unique set()  ---> temp proxy save
        self.prv = set()
        self.sql = Mysql()
        self.hrd = hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


    # check proxy ip (if connect taobao.com use proxy ip)
    def check_proxy(self,proxy_tmp):

        self.sum_count = self.sum_count + 1
        print self.sum_count,


        # get
        request = urllib2.Request(url="https://www.taobao.com/",headers=self.hrd)

        try:

            proxy_temp = urllib2.ProxyHandler({'https': proxy_tmp})
            opener = urllib2.build_opener(proxy_temp)
            urllib2.install_opener(opener)
            response = urllib2.urlopen(request, timeout=2)
        except Exception,e:
            # print proxy_tmp +"  " +"XXXXXX"
            self.bad_count += 1


        else :
            self.work_count += 1


            # if ok , write a file or save database dirly
            # i choose write a file , beacause i think it's not efficency save database reqeat
            # or don't care

            self.lock.acquire() # thread blocks at this line until it can obtain lock
            print "["+str(self.work_count)+"]"+"*",
            self.fw.write(proxy_tmp.strip()+"\n")

            self.lock.release()



    # collecct proxy from proxy source && database
    def collect_proxy(self):


        '''
        proxy from proxy source

        '''
        for line in self.fr:

            if (line.strip() == " ") :
                continue

            ll = line.split("^")

            proxy_tmp =  ll[0]+":"+ll[1].strip()
            self.prv.add(proxy_tmp)

        print 'proxy source number :' + str(len(self.prv))

        '''
        proxy from database

        '''

        proxy_tmp_mysql = self.sql.get_proxy()
        print 'database numbers : ' +str(len(proxy_tmp_mysql))

        for i in xrange(0,len(proxy_tmp_mysql)):
            proxy_ip = proxy_tmp_mysql[i]['ip']+":"+proxy_tmp_mysql[i]['port']
            self.prv.add(proxy_ip)

        # I delete all proxy of database ,
        # and if you want to delete fake ip only, you could rem fake number and delete by one by
        #                               or change this model (divide totally database and file source )
        self.sql.delete_all()

        print 'sum unique numbers : ' + str(len(self.prv))


    # set six thread to run ,call check_proxy()
    def thread_check(self):


        pool = ThreadPool(6)

        pool.map(self.check_proxy,self.prv)


    # when check_proxy() over, the good proxy ip save to a file
    # this function save the file to mysql
    def save_proxy(self):

        self.fw.close()
        self.fr.close()
        self.sql.save_file_proxy()
        print 'work_count numbers : ' + str(self.work_count)
        print 'bad_count numbers : ' + str(self.bad_count)

    # run ----->
    #           1. collect_proxy()
    #           2. thread_check() --> check_proxy()
    #           3. save_proxy()
    def run(self):

        self.collect_proxy()
        self.thread_check()
        print "\n"
        self.save_proxy()






# cl = Clean_proxy()
# cl.run()







#!/usr/bin/env python
# coding:utf8

'''

function : find proxy IP
author   : Zhangze
date     : 2016-12-14

'''


import sys
reload(sys)
sys.setdefaultencoding('utf8')

import urllib2
import urllib
import time
import inspect
import json
from bs4 import BeautifulSoup

class Proxy:

    def __init__(self):
        self.User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
        self.header = {}
        self.header['User-Agent'] = self.User_Agent

        self.f = open("proxy.txt","w")

        self.proxy_url = ["kuaidaili","xicidaili"]

    def run (self):

        # there , i want to call each url about self.proxy_url ,
        # but when i use : "self.method_name+"()"", it's wrong
        # so , i want to get all method and to match with self.proxy_url XXXXXXXXXXXX
        # I find "getattr(Proxy,method)(self)" perfect

        # get all method about this class XXXXXXXXXXXXX
        # method_list = inspect.getmembers(Proxy, predicate=inspect.ismethod)

        for method in self.proxy_url:
            # Proxy().method()
            print 'find' + " " + method
            getattr(Proxy,method)(self)

        # this line is very import  !!! if not close , if next use this file , would debug
        self.f.close()




    # init diff url
    #
    def url_soup(self,url):

        req = urllib2.Request(url,headers=self.header)
        res = urllib2.urlopen(req).read()
        soup = BeautifulSoup(res)
        return soup


    # http://www.xicidaili.com/nn/
    #
    def xicidaili(self):
        for i in xrange(1,4):
            url = 'http://www.xicidaili.com/nn/'+str(i)
            soup = self.url_soup(url)
            ips = soup.findAll('tr')

            for x in range(1,len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                ip_temp = tds[1].contents[0]+"^"+tds[2].contents[0]+"\n"
                # print tds[2].contents[0]+"\t"+tds[3].contents[0]
                self.f.write(ip_temp)
            # print str(i) + "  " + url
            print i,
        print "\n"


    # http://www.kuaidaili.com/proxylist
    #
    def kuaidaili(self):

        for i in xrange(1,4):
            url = 'http://www.kuaidaili.com/proxylist/'+str(i)
            soup = self.url_soup(url)
            ips = soup.findAll('tr')

            for x in range(1,len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                ip_temp = tds[0].contents[0]+"^"+tds[1].contents[0]+"\n"
                self.f.write(ip_temp)
            # print str(i) + "  " + url
            print i,
        print "\n"


    def __exit__ (self):

        self.f.close()



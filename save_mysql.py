#!/usr/bin/env python
# coding:utf8

'''
    proxy ip save to mysql
    author: Zhangze
    email: 605166577@qq.com
    date: 2016/12/14
'''
import MySQLdb
import MySQLdb.cursors

class Mysql:

    def __init__(self):

        db = MySQLdb.connect(host='localhost', user='root', passwd='#mJl&dcs.6(O', db='proxy', port=8889, charset='utf8', cursorclass = MySQLdb.cursors.DictCursor)
        db.autocommit(True)
        self.cursor = db.cursor()



    def get_proxy(self):

        self.cursor.execute('select ip,port from good_proxy')

        return self.cursor.fetchall()

    def delete_all(self):

        self.cursor.execute('delete from good_proxy')




    def save_file_proxy(self):

        inputFile = 'proxy_clean.txt'
        fr = open(inputFile, 'rw')

        count = 0

        array = []

        print "*************"+'save_mysql'+"*************"

        for line in fr:

            # print line

            if (line.strip() == ""):
                print "continue"
                continue

            if line in array :
                # print "dup"
                continue
            else:
                array.append(line)
                line = line.split(':')
                # print line
                ip= line[0]
                port = line[1]
                # print ip + " " + port

                self.cursor.execute('insert into good_proxy(ip,port) values(%s,%s)',[ip,port])

                count = count + 1
                # print count

# sql =Mysql()
# sql.save_file_proxy()

# # fr.close()
# db.close()
# cursor.close()
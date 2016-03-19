#!python2
#coding=utf-8
import bs4
import flask
import urllib,urllib2,cookielib
import re
from bs4 import BeautifulSoup
import htmllib,formatter
import os,sys
import os.path as op

import StringIO
import gzip

from flask import Flask, redirect, render_template, request, g, url_for, session, flash, abort, Response, json, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

#Create App
app = Flask(__name__)
#app.debug = True

# Configure
app.secret_key = 'herh5h4h4her6rs6yre6hrejes5r7mk547njsj74s57mk54n7s7b3a7m69,80.t78km5ew737 3neeb5n54m86rm'
app.config['DATABASE_FILE'] = os.path.join(app.root_path, 'duanzi.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = False

db = SQLAlchemy(app)

class Duanzi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pageid = db.Column(db.Unicode(50))
    duanzi = db.Column(db.UnicodeText)
    oo = db.Column(db.Integer)
    xx = db.Column(db.Integer)
    myoo = db.Column(db.Integer)
    myxx = db.Column(db.Integer)

    def __unicode__(self):
        return self.duanzi[:10]

db.create_all()

def getHtml(url, req_timeout):
    req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept':'text/html;q=0.9,*/*;q=0.8',
    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding':'gzip',
    'Connection':'close',
    'Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
    }
    #req_timeout = 5
    request = urllib2.Request(url,None,req_header)
    response = urllib2.urlopen(request,None,req_timeout)

    isGzip = response.headers.get('Content-Encoding')
    #html = response.read()
    if isGzip :
        compresseddata = response.read()
        compressedstream = StringIO.StringIO(compresseddata)
        gzipper = gzip.GzipFile(fileobj=compressedstream)
        data = gzipper.read()
    else:
        data = response.read()
    return data

def OnlyDigit(mytext):
    if mytext=='':
        return 0
    else:
        if filter(lambda ch: ch in '0123456789.', mytext)=='':
            return 0
        else:
            return(filter(lambda ch: ch in '0123456789.', mytext))

duan = getHtml("http://jandan.net/duan", 10)
duansoup = BeautifulSoup(duan)
MaxPage = int(OnlyDigit(duansoup.find_all('span', attrs={"class": "current-comment-page"})[0].text))

kaishi = 1
if sys.argv.__len__() == 2:
    kaishi = int(sys.argv[1])
else:
    kaishi = MaxPage-5

for page in range(kaishi,MaxPage+1):
    html = getHtml("http://jandan.net/duan/page-" + str(page), 10)

    soup = BeautifulSoup(html)

    DuanAll=soup.find_all('div', attrs={"class": "text"})

    if DuanAll.__len__()>=1:
        for duan in DuanAll:
            try:
                span=duan.find_all('span')
                support = int(span[2].text)
                unsupport = int(span[3].text)
                if True:#support > unsupport:
                    duanzi_str = duan.p.text
                    #建立数据库
                    duanzi = Duanzi.query.filter_by(duanzi=duanzi_str)
                    if duanzi.count() == 0:
                        print u"正在插入数据库" + u"-----当前页面：" + str(page)
                        db.session.add(Duanzi(pageid=str(page), duanzi=duanzi_str, oo=support, xx=unsupport, myoo=0, myxx=0))
                    else:
                        print u"库中已有，跳过" + u"-----当前页面：" + str(page)
                else:
                    print u"跳过xx过多的段子" + u"-----当前页面：" + str(page)
            except:
                pass
    db.session.commit()
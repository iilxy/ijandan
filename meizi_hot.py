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
app.secret_key = 'herh5h4h4her6rsgfjfjfjfjgfjgfjgfjgfjgfjgfjgfjfj'
app.config['DATABASE_FILE'] = os.path.join(app.root_path, 'meizi_hot.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = False

db = SQLAlchemy(app)

class Meizi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    foldername = db.Column(db.Unicode(50))
    picname = db.Column(db.Unicode(50))
    picurl = db.Column(db.UnicodeText)
    oo = db.Column(db.Integer)
    xx = db.Column(db.Integer)
    myoo = db.Column(db.Integer)
    myxx = db.Column(db.Integer)
    nsfw = db.Column(db.Boolean)

    def __unicode__(self):
        return self.picname

db.create_all()

# Create directory for file fields to use
down_path = op.join(op.dirname(__file__), 'meizi_hot')
try:
    os.mkdir(down_path)
except OSError:
    pass

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
    
    # request = urllib2.Request(url)
    # request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
    # request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    # request.add_header('Accept-Charset','utf-8;')
    # request.add_header('Accept-Encoding','gzip,deflate')
    # request.add_header('Connection','close')
    # request.add_header('Referer', None)
    # response = urllib2.urlopen(request)
    
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

def downloadImage(url):
    path = op.join(op.dirname(__file__), 'meizi_hot')
    try:
        os.mkdir(path)
    except:
        pass
    try:
        cont = getHtml(url, 10) #urllib2.urlopen(url).read()
        #patter = '[0-9]*\.jpg';
        #match = re.search(patter,url);
        name = url.split(u"/")[-1]
        # if match:
        print u'正在下载文件：', name
        filename = path+os.sep+name
        f = open(filename,'w+b')
        f.write(cont)
        f.close()
    except:
        pass

def OnlyDigit(mytext):
    if mytext=='':
        return 0
    else:
        if filter(lambda ch: ch in '0123456789.', mytext)=='':
            return 0
        else:
            return(filter(lambda ch: ch in '0123456789.', mytext))


html = getHtml("http://jandan.net/top", 10)

soup = BeautifulSoup(html)

#ImgAll = soup.find_all('div', attrs={"id": "girl"})

ImgAll=soup.find_all('div', attrs={"class": "text"})

if ImgAll.__len__()>=1:
    for image in ImgAll:
        try:
            link = image.find_all('a')
            if link[0].attrs["href"] == u'http:/pic':
                print u"跳过无聊图"
            else:
                imgs = image.find_all('img')
                span=image.find_all('span')
                nsfw=False
                if re.search(u'NSFW',image.find_all('p')[0].text):
                    nsfw = True
                support = int(span[2].text)
                unsupport = int(span[3].text)
                if True:#support > unsupport:
                    if imgs.__len__()==1:
                        imgsrc = image.img.attrs['src']
                        if imgsrc.split(u".")[-1].upper() == "GIF":
                            imgsrc = image.img.attrs["org_src"]
                        if os.path.exists(op.join(op.dirname(__file__), 'meizi_hot', imgsrc.split(u"/")[-1])):
                            print u"正在跳过" + imgsrc
                        else:
                            downloadImage(imgsrc)
                        #建立数据库
                        pic = Meizi.query.filter_by(picurl=imgsrc)
                        if pic.count() == 0:
                            print u"正在插入数据库"
                            db.session.add(Meizi(foldername="meizi_hot", picname=imgsrc.split(u"/")[-1], picurl=imgsrc, oo=support, xx=unsupport, nsfw=nsfw, myoo=0, myxx=0))
                        else:
                            print u"库中已有，跳过"
                    else:
                        for ii in imgs:
                            imgsrc = ii.attrs['src']
                            if imgsrc.split(u".")[-1].upper() == "GIF":
                                imgsrc = ii.attrs["org_src"]
                            if os.path.exists(op.join(op.dirname(__file__), 'meizi_hot', imgsrc.split(u"/")[-1])):
                                print u"正在跳过" + imgsrc
                            else:
                                downloadImage(imgsrc)
                            #建立数据库
                            pic = Meizi.query.filter_by(picurl=imgsrc)
                            if pic.count() == 0:
                                print u"正在插入数据库"
                                db.session.add(Meizi(foldername="meizi_hot", picname=imgsrc.split(u"/")[-1], picurl=imgsrc, oo=support, xx=unsupport, nsfw=nsfw, myoo=0, myxx=0))
                            else:
                                print u"库中已有，跳过"
                else:
                    print u"跳过xx过多的图"
        except:
            pass
db.session.commit()
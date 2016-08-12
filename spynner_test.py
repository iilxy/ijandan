#!python2
#coding=utf-8

#Ghost.py 一个基于webkit的页面渲染器
#from ghost import Ghost

import spynner
import pyquery
import os,sys
import os.path as op
import urllib,urllib2,cookielib
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


def downloadImage(url,dir2down):
    path = op.join(op.dirname(__file__), dir2down)
    try:
        os.mkdir(path)
    except:
        pass
    try:
        cont = getHtml(url, 10)  # urllib2.urlopen(url).read()
        # patter = '[0-9]*\.jpg';
        # match = re.search(patter,url);
        name = url.split(u"/")[-1]
        # if match:
        print u'正在下载文件：', name
        filename = path + os.sep + name
        f = open(filename, 'w+b')
        f.write(cont)
        f.close()
    except:
        pass

browser = spynner.Browser(debug_level=spynner.DEBUG,download_directory="meizi_hot")
# 设置代理
#browser.set_proxy('http://host:port')
#browser.create_webview()
#browser.show()
browser.set_html_parser(pyquery.PyQuery)
#browser.load("http://jandan.net")
try:
    browser.load(url='http://jandan.net/top', load_timeout=120, tries=1,headers=[('User-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'),
                     ('Host','jandan.net')])
except spynner.SpynnerTimeout:
    print 'Timeout.'
else:
    #browser.wait_load()
    allimg = browser.soup("img")
    for img in allimg:
        print img.attrib['src']
    alldiv = browser.soup("div")
    for div in alldiv:
        try:
            if div.attrib['id'] == "girl":
                d = pyquery.PyQuery(div)
                allgridimg = d('img')
                for girl in allgridimg:
                    # 建立数据库
                    pic = Meizi.query.filter_by(picurl=girl.attrib['src'])
                    if pic.count() == 0:
                        print u"正在插入数据库"
                        db.session.add(Meizi(foldername="meizi_hot", picname=girl.attrib['src'].split(u"/")[-1],
                                             picurl=girl.attrib['src'], oo=0, xx=0, nsfw=True, myoo=0, myxx=0))
                        if girl.attrib['src'][-3:].upper() == "GIF":
                            downloadImage(girl.attrib['org_src'], 'meizi_hot')
                        else:
                            downloadImage(girl.attrib['src'],'meizi_hot')
                    else:
                        print u"库中已有，跳过"
        except :
            pass
db.session.commit()


#d = pyquery.PyQuery(browser.html)
# browser.select("#esen")
# browser.fill("input[name=w]", "hola")
# browser.click("input[name=B10]")
# browser.wait_load()
# print "url:", browser.url
#
# # Soup is a PyQuery object
# browser.soup.make_links_absolute(base_url=browser.url)
# print "html:", browser.soup("#Otbl").html()
#
# # Demonstrate how to download a resource using PyQuery soup
# imagedata = browser.download(browser.soup("img:first").attr('src'))
# print "image length:", len(imagedata)
#browser.close()

# 这个是底层的QtWebKit相关库里 用的是Qt的QString  spynner在将QString转为Python的通用字符串时，没有考虑到中文编码这一块的问题。
#
# 原创声明：我这两天抓取动态页面，也遇到这个问题，通过调试发现是QString问题后从google找到了QString的正确转换方法。
# 你把Python27\Lib\site-packages\spynner\browser.py 下的函数 (大概是477行)
# def _get_html(self):
#     return six.u(self.webframe.toHtml())
# 改成下面这样
# def _get_html(self):
#     return unicode(self.webframe.toHtml().toUtf8(), 'utf-8', 'ignore')

    # def _get_html(self):
    #     #return six.u(self.webframe.toHtml())
        # return unicode(self.webframe.toHtml().toUtf8(), 'utf-8', 'ignore')
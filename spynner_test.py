#!python2
#coding=utf-8

import spynner
import pyquery

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
                    print girl.attrib['src']
                    debug=1
        except :
            print 'no id'

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
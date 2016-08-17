# -*- coding: utf-8 -*-

from ghost import Ghost
import lxml.html

agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36'
ghost = Ghost()
#ghost.set_proxy('socks5', '192.168.1.111', 1080)  # 使用socks5代理
with ghost.start() as session:
    page, extra_resources = session.open('http://www.jandan.net', timeout=20, user_agent=agent)
    assert page.http_status == 200 and 'iilxy' in page.content

    html = lxml.html.fromstring(page.content)
    e = html.xpath('//*[@]/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/table/tbody')[0]  #
    for tr in e.getchildren():
        print tr.getchildren()[3].text
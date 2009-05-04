#!/usr/bin/env python
# This file is part of Fedora Community.
# Copyright (C) 2008-2009  Red Hat, Inc.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import urllib2
import datetime
import time
import re

date_match = re.compile('<!--X-Date: ([^-|^>|.]*) -->')
subject_match = re.compile('<!--X-Subject: ([^-|^>|.]*) -->')
guid_match = re.compile('<!--X-Message-Id: (([.]|[^-^>])*) -->')

def get_messages(url):
    posts = []


    for i in xrange(5000):
        post = {'title': None,
            'url': None,
            'poster': None,
            'date': None,
            'body': None
           }

        msgurl = url % i
        try:
            r = urllib2.urlopen(msgurl)
            data = r.read()
            post['url'] = msgurl
            start = data.find('<!--X-Body-of-Message-->') + len('<!--X-Body-of-Message-->')
            end = data.find('<!--X-Body-of-Message-End-->')
            
            post['body'] = data[start: end]
            
            data = data[:start]
            post['title'] = subject_match.search(data).group(1).replace('&#45;','-')
            date = date_match.search(data).group(1).replace('&#45;','-')
            date = date[:-6]
            date = datetime.datetime(*time.strptime(date, "%a, %d %b %Y %H:%M:%S")[0:5])
            date = date.strftime("%a, %d %b %Y %H:%M:%S GMT")
            post['date'] = date
            
            post['guid'] = guid_match.search(data).group(1).replace('&#45;','-')

            start = data.find('<li><em>From</em>: ') + len('<li><em>From</em>: ')
            end = data.find('</li>', start)
            post['poster'] = data[start:end]

            posts.append(post)
        except urllib2.URLError:
            posts.reverse()
            return posts

    posts.reverse()
    return posts

def dump_rss(l):
    rsshead='''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:atom="http://www.w3.org/2005/Atom"
	xmlns:sy="http://purl.org/rss/1.0/modules/syndication/"
	xmlns:media="http://search.yahoo.com/mrss/"
	>

<channel>
	<title>fedora-announce</title>
	<link>https://www.redhat.com/archives/fedora-announce-list/</link>
	<description>Fedora Announcements</description>
	<generator>j5's mailman to rss python script</generator>
	<language>en</language>
'''
    
    rssitem = ''' 
	  <item>
		<title>%s</title>
        <guid>%s</guid>
		<link>%s</link>
		<pubDate>%s</pubDate>
			<content:encoded><![CDATA[<p>posted by %s</p>%s]]></content:encoded>

	</item>
'''

    rssfoot = '''
    </channel>
</rss>
'''
    rss = rsshead

    for i in l:
        c = rssitem % (i['title'], i['guid'], i['url'], i['date'], i['poster'], i['body'])
        rss += c

    rss += rssfoot

    return rss


url = "http://www.redhat.com/archives/fedora-announce-list/%Y-%B/"

now = datetime.date.today()
m = now.month - 1
y = now.year
if m == 0:
    m = 12
    y -= 1

last_month = datetime.date(y,m, 1)

now_url = now.strftime(url) + "msg%05i.html"
last_month_url = last_month.strftime(url) + "msg%05i.html"

msg_list = []

msg_list.extend(get_messages(now_url))
msg_list.extend(get_messages(last_month_url))

print dump_rss(msg_list)

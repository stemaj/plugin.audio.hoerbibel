#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import re
import httplib
import socket

def getUrl(url):
    error = ''
    link = ''
    req = urllib2.Request(url, headers={'accept': '*/*'})
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:19.0) Gecko/20100101 Firefox/19.0')
    try:
        response = urllib2.urlopen(req)
        if not response:
            error = 'No response - Please try again'
    except urllib2.HTTPError as e:
        error = 'Error code: ', e.code
    except urllib2.URLError as e:
        error = 'Reason: ', e.reason
    except Exception as e:
        if e.message:
            error = e.message
        else:
            error = 'Other reason'
    if not error:
        try:
            link = response.read()
            if not link:
                error = 'No data - Please try again'
        except httplib.IncompleteRead as e:
            error = e.message
        except Exception as e:
            error = e.message
    
    if not error:
        if response:
            response.close()

    return (link, error)

def getBooks():
    bookSite = getUrl('http://www.bibleserver.com/overlay/selectBook')
    if not bookSite[0]:
        return bookSite[1]
    bookSite = bookSite[0].split("booknames\":{")
    bookSite = bookSite[1].split("},\"trl_cols")
    bookSite = bookSite[0]
    bookSite = bookSite.split(',')
    books = []
    for entry in bookSite:
        books.append(str(entry.split(':')[1]).replace("\"",""))
    return books

def chapterCount(book):
    return 50

def getAudioLink(book, chapter):
    link = getUrl('http://www.bibleserver.com/text/ABV/' + book + str(chapter))
    link = link[0].split('file: \'')
    link = link[1].split('config:')
    link = link[0].split('\',')[0]
    link = 'http://m.bibleserver.com/' + str(link)
    return link

#getBooks()
#link = getAudioLink('1.Könige',7)

#i = 5


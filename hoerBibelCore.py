#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import re
import httplib
import socket
from stemajUrl import StemajUrl

def getBooks():
    stUrl = StemajUrl()
    bookSite = stUrl.getUrl('http://www.bibleserver.com/overlay/selectBook', True)
    if len(stUrl.error) > 0:
        return

    bookSite = bookSite.split("pageMain\">")[1]
    books = re.compile("\">(.+?)</a></li>", re.DOTALL).findall(bookSite)
    return books

def chapterCount(book):
    return 50

def getText(uebersetzung, book, chapter):
    stUrl = StemajUrl()
    link = stUrl.getUrl('http://m.bibleserver.com/text/' + uebersetzung + '/' + book + str(chapter), True)
    link = link.split("class=\"content\"")[1]
    link = link.split('verseNumber">')
    link.pop(0)
    verses = []
    for entry in link:
        temp = entry.split('</span>')
        temp = temp[1].split('</div>')
        verses.append(str(temp[0]))
    return verses

def getAudioLink(book, chapter):
    stUrl = StemajUrl()
    link = stUrl.getUrl('http://www.bibleserver.com/text/ABV/' + book + str(chapter), True)
    if 'bible_player' in link:
        link = re.compile("bible_player\"><a href=\"(.+?)\"", re.DOTALL).findall(link)[0]
        link = 'http://www.bibleserver.com/' + link
        return link
    return ""

#books = getBooks()
#link = getAudioLink(books[67],1)
#verse = getText('NLB','Judit',2)
#i = 5


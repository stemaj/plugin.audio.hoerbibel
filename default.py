#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import socket
import urllib
import hoerBibelCore

addonID = 'plugin.audio.hoerbibel'
addon = xbmcaddon.Addon(id=addonID)
socket.setdefaulttimeout(30)
pluginhandle = int(sys.argv[1])
translation = addon.getLocalizedString
addonDir = xbmc.translatePath(addon.getAddonInfo('path'))
icon = os.path.join(addonDir ,'icon.png')
tempPath = addon.getSetting("tempPath")

if (len(tempPath) == 0):
    nameAddon = "Hörbibel" # translation(30101) #"Hörbibel"
    bittePfad = "Bitte Pfad in Einstellungen festlegen" # translation(30103) #"Bitte Pfad in Einstellungen festlegen"
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(nameAddon, bittePfad, 4500, icon))
    sys.exit(0)
    
def index():
    books = hoerBibelCore.getBooks()
    for book in books:
        addDir(book, book, "listChapters")
    #addDir('Rut', 'http://www.bibleserver.com/text/ABV/Rut1', "listChapters")
    xbmcplugin.endOfDirectory(pluginhandle)

def listChapters(book):
    cnt = hoerBibelCore.chapterCount(book)
    for i in range(1, cnt, 1):
        addLink(str(i), book, 'playAudio')
    xbmcplugin.endOfDirectory(pluginhandle)

def addDir(name, url, mode):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+urllib.quote_plus(mode)+"&fanart="+urllib.quote_plus(icon)
    ok = True
    liz = xbmcgui.ListItem(name, icon, thumbnailImage=icon)
    liz.setInfo(type="Audio", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

def addLink(name, url, mode):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+urllib.quote_plus(mode)+"&name="+urllib.quote_plus(name)
    liz=xbmcgui.ListItem(name, iconImage="DefaultAudio.png", thumbnailImage=icon)
    liz.setInfo(type="Audio", infoLabels={"Title": name})
    liz.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)

def playAudio(book,chapter):
    import SimpleDownloader as downloader
    downloader = downloader.SimpleDownloader()
    link = hoerBibelCore.getAudioLink(book,chapter)
    params = { "url": link, "download_path": tempPath }
    tempFileName = "myvideo.mp3"
    if os.path.isfile(tempPath + tempFileName):
        os.remove(tempPath + tempFileName)
    downloader.download(tempFileName, params)
    while not os.path.isfile(tempPath + tempFileName):
        time.sleep(.100)
    listitem = xbmcgui.ListItem(path= tempPath + tempFileName)
    listitem.setInfo( type="Audio", infoLabels={ "Title": name } )
    listitem.setProperty("mimetype", 'audio/mpeg')
    return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

params = parameters_string_to_dict(sys.argv[2])
mode = urllib.unquote_plus(params.get('mode', ''))
url = urllib.unquote_plus(params.get('url', ''))
name = urllib.unquote_plus(params.get('name', ''))
fanart = urllib.unquote_plus(params.get('fanart', ''))

if mode == "playAudio":
    playAudio(url,name)
elif mode == "listChapters":
    listChapters(url)
else:
    index()

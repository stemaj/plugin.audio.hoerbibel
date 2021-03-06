﻿#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import urllib
import hoerBibelCore

addonID = 'plugin.audio.hoerbibel'
addon = xbmcaddon.Addon(id=addonID)
pluginhandle = int(sys.argv[1])
translation = addon.getLocalizedString
addonDir = xbmc.translatePath(addon.getAddonInfo('path'))
icon = os.path.join(addonDir ,'icon.png')

def index():
    books = hoerBibelCore.getBooks()
    for book in books:
        addDir(book, "listChapters")
        #addDir('Rut', 'http://www.bibleserver.com/text/ABV/Rut1', "listChapters")
    xbmcplugin.endOfDirectory(pluginhandle)
        
def listChapters(buch):
    cnt = hoerBibelCore.chapterCount(buch)
    for i in range(1, cnt, 1):
        addLink(str(i), buch, 'playAudio')
    xbmcplugin.endOfDirectory(pluginhandle)
                
def addDir(buch, mode):
    u = sys.argv[0]+"?buch="+urllib.quote_plus(buch)+"&mode="+urllib.quote_plus(mode)
    ok = True
    liz = xbmcgui.ListItem(buch, icon, thumbnailImage=icon)
    liz.setInfo(type="Audio", infoLabels={"Title": buch})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

def addLink(kapitel, buch, mode):
    u = sys.argv[0]+"?kapitel="+urllib.quote_plus(kapitel)+"&mode="+urllib.quote_plus(mode)+"&buch="+urllib.quote_plus(buch)
    liz=xbmcgui.ListItem(kapitel, iconImage="DefaultAudio.png", thumbnailImage=icon)
    liz.setInfo(type="Audio", infoLabels={"Title": buch + ' ' + str(kapitel)})
    liz.setProperty('IsPlayable', 'true')
    liz.addContextMenuItems([('Text: Luther 2017', 'RunPlugin(plugin://'+addonID+'/?mode=showText&buch='+buch+'&kapitel='+kapitel+'&uebersetzung=LUT)'),
                             ('Text: Luther 1984', 'RunPlugin(plugin://'+addonID+'/?mode=showText&buch='+buch+'&kapitel='+kapitel+'&uebersetzung=LUT84)'), 
                             ('Text: Elberfelder', 'RunPlugin(plugin://'+addonID+'/?mode=showText&buch='+buch+'&kapitel='+kapitel+'&uebersetzung=ELF)'), 
                             ('Text: Hoffnung für Alle', 'RunPlugin(plugin://'+addonID+'/?mode=showText&buch='+buch+'&kapitel='+kapitel+'&uebersetzung=HFA)'), 
                             ('Text: Schlachter 2000', 'RunPlugin(plugin://'+addonID+'/?mode=showText&buch='+buch+'&kapitel='+kapitel+'&uebersetzung=SLT)'),
                             ('Text: Neue Genfer Übs.', 'RunPlugin(plugin://'+addonID+'/?mode=showText&buch='+buch+'&kapitel='+kapitel+'&uebersetzung=NGÜ)'), 
                             ('Text: Gute Nachricht', 'RunPlugin(plugin://'+addonID+'/?mode=showText&buch='+buch+'&kapitel='+kapitel+'&uebersetzung=GNB)'), 
                             ('Text: Einheitsübs.', 'RunPlugin(plugin://'+addonID+'/?mode=showText&buch='+buch+'&kapitel='+kapitel+'&uebersetzung=EU)'), 
                             ('Text: Neues Leben', 'RunPlugin(plugin://'+addonID+'/?mode=showText&buch='+buch+'&kapitel='+kapitel+'&uebersetzung=NLB)'),
                             ('Text: Neue evangelistische Übs.', 'RunPlugin(plugin://'+addonID+'/?mode=showText&buch='+buch+'&kapitel='+kapitel+'&uebersetzung=NeÜ)')])
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)

def playAudio(book,chapter):
    link = hoerBibelCore.getAudioLink(book,chapter)
    params = { "url": link }
    listitem = xbmcgui.ListItem(path=link)
    listitem.setInfo( "music", { "title": book + " " + chapter } )
    url = xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

def showText(buch,kapitel,uebersetzung):
    #siehe kodi.wiki/view/Window_IDs
    xbmc.executebuiltin('ActivateWindow(%d)' % 10147)
    window = xbmcgui.Window(10147)
    xbmc.sleep(200)
    #1 ist das label
    window.getControl(1).setLabel(buch + ' ' + kapitel)
    text = ""
    verse = hoerBibelCore.getText(uebersetzung,buch,kapitel)
    for i in range(0, len(verse), 1):
        text = text + '[B]'+str(i+1)+'[/B]' + ' ' + verse[i] + '\n'
    #5 ist die box
    window.getControl(5).setText(text)

   
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
buch = urllib.unquote_plus(params.get('buch', ''))
kapitel = urllib.unquote_plus(params.get('kapitel', ''))
uebersetzung = urllib.unquote_plus(params.get('uebersetzung', ''))

if mode == "playAudio":
    playAudio(buch,kapitel)
elif mode == "listChapters":
    listChapters(buch)
elif mode == "showText":
    showText(buch,kapitel,uebersetzung)
else:
    index()

#!/usr/bin/python3

import requests ,json, sys, re, os, shutil
from bs4 import BeautifulSoup
from optparse import OptionParser
import urllib.request

class SkipChapter(Exception): pass
class StopHere(Exception): pass

def show_language(option, opt, value, parser):
    print("Here the list of the language handle by the MangaDex website: \nArabic\nBengali\nBulgarian\nBurmese\nCatalan\nChinese (Simp)\nChinese (Trad)\nCzech\nDanish\nDutch\nEnglish\nFilipino\nFinnish\nFrench\nGerman\nGreek\nHebrew\nHindi\nHungarian\nIndonesian\nItalian\nJapanese\nKorean\nLithuanian\nMalay\nMongolian\nNorwegian\nOther\nPersian\nPolish\nPortuguese (Br)\nPortuguese (Pt)\nRomanian\nRussian\nSerbo-Croatian\nSpanish (Es)\nSpanish (LATAM)\nSwedish\nThai\nTurkish\nUkrainian\nVietnamese\nOther")
    exit(0)

parser = OptionParser()
parser.add_option("-i","--id",type="int", help="the id of the mangaDex manga")
parser.add_option("-b","--range_min",type="int", help="Begining of the chapter to download (an int)")
parser.add_option("-e","--range_max",type="int", help="End of the chapter to download (an int)")
parser.add_option("-l","--language", help="language of the scan", type="choice", choices=["Arabic","Bengali","Bulgarian","Burmese","Catalan","Chinese (Simp)","Chinese (Trad)","Czech","Danish","Dutch","English","Filipino","Finnish","French","German","Greek","Hebrew","Hindi","Hungarian","Indonesian","Italian","Japanese","Korean","Lithuanian","Malay","Mongolian","Norwegian","Other","Persian","Polish","Portuguese (Br)","Portuguese (Pt)","Romanian","Russian","Serbo-Croatian","Spanish (Es)","Spanish (LATAM)","Swedish","Thai","Turkish","Ukrainian","Vietnamese","Other"])
parser.add_option("-L","--show_language",action="callback", callback=show_language, help="show the list of languages that works on MangaDex")

(opts, args) = parser.parse_args()


def getFromApi(mangaName, listId):
    for id in listId:
        r = requests.get("https://mangadex.org/api/?id=" + id  +"&server=null&saver=1&type=chapter", None)
        jason = json.loads(r.text)
        volume = jason["volume"]
        chapter = jason['chapter']
        if not os.path.exists(mangaName + "/" + volume):
            os.makedirs(mangaName + "/" + volume)
        if not os.path.exists(mangaName +"/"+ volume +"/chapter_" + chapter):
            os.makedirs(mangaName +"/"+ volume +"/chapter_" + chapter)
        url = jason['server'] + jason['hash'] 
        index = 0
        print("Saving volume " + volume +".chapter " + chapter + " of " + mangaName);
        number = 0
        maxNumber = len(jason['page_array'])
        for file in jason['page_array']:
            number += 1 
            if os.path.exists(mangaName + "/" + volume +"/chapter_" + chapter + "/" + file):
                print("Already having " + mangaName + "/" + volume +"/chapter_" + chapter+ " part " + str(number) + " of " + str(maxNumber))
                continue
            print("\tpart " + str(number) + " of " + str(maxNumber))
            r = requests.get( url + "/" + file)
            r.raw.decode_content = True
            with open(mangaName + "/" + volume +"/chapter_" + chapter + "/" + file, 'wb') as f:
                f.write(r.content)

def getListId(mangaName, webpageHtml, begin , end, languageRequire):
    listId = []
    listChapter = []
    fid=urllib.request.urlopen(webpageHtml)
    webpage=fid.read().decode('utf-8')
    soup = BeautifulSoup(webpage,features="html.parser")

    col = soup.findAll("div", {"class":"chapter-row d-flex row no-gutters p-2 align-items-center border-bottom odd-row"})

    for div in reversed(col):
        divPhoto = div.find("div",{"class":"chapter-list-flag col-auto text-center order-lg-4"})
        if(divPhoto):
            language = divPhoto.find("span")["title"]
            if(language != languageRequire):
                continue
        divChapter = div.find("div",{"class":"col col-lg-5 row no-gutters align-items-center flex-nowrap text-truncate pr-1 order-lg-2"})
        if(divChapter):
            divChapter = divChapter.find("a")
            href = divChapter["href"].split("/")[2]
            chapter = divChapter.text.split("-")[0].strip().split(" ")[-1]
            if(begin is not None and float(begin) > float(chapter) ):
                continue
            if (end and float(chapter) > end):
                break

            if(chapter and chapter in listChapter):
                continue
            else:
                listChapter.append(chapter)
                listId.append(href)
    getFromApi(mangaName, listId)

def main():
    if(opts.id is None):
        parser.error("Please provide an Id")
        parser.print_help()
        exit(-1)
    if(opts.range_min and opts.range_max and opts.range_min > opts.range_max):
        print("wrong chapter range !!!")
        exit(-1)
    if(opts.language is None):
        ###Because english good 
        opts.language = "English"

    fid=urllib.request.urlopen('https://mangadex.org/manga/' + str(opts.id))
    webpage=fid.read().decode('utf-8')
    soup = BeautifulSoup(webpage,features="html.parser")
    mangaName = soup.findAll("span",{"class":"mx-1"})[0].text

    listChapters = soup.findAll("li",{"class":"page-item paging"})
    if not listChapters:
        getListId(mangaName, "https://mangadex.org/manga/" + str(opts.id), opts.range_min, opts.range_max, opts.language)
    else:
        html = listChapters[0]
        href = [i.findAll('a', href=True) for i in soup.findAll("li",{"class":"page-item paging"})][0][0]["href"]
        mangaRaw = href.split('/')[2]
        maxChapter = href.split('/')[5]
        for x in range(int(maxChapter),0,-1):
            print("Downloading on https://mangadex.org/title/" + str(opts.id) + "/" + mangaRaw + "/chapters/" + str(x))
            getListId(mangaName, "https://mangadex.org/title/" + str(opts.id) + "/" + mangaRaw + "/chapters/" + str(x), opts.range_min, opts.range_max,opts.language)

if (__name__ == "__main__"):
    main()

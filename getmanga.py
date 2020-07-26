import requests ,json, sys, re, os, shutil
from bs4 import BeautifulSoup
import urllib.request

class StopLookingForThings(Exception): pass

def dl(webpageHtml):
    fid=urllib.request.urlopen(webpageHtml)
    webpage=fid.read().decode('utf-8')
    for line in reversed(webpage.splitlines()):
        try:
            def doDownload():
                if ("/chapter/" in line):
                    if ("comments" not in line):
                        listid = line.split("'")[1].split("/")[2]
                        for id in listid.splitlines():
                           r = requests.get("https://mangadex.org/api/?id=" + id  +"&server=null&saver=1&type=chapter", None)
                           jason = json.loads(r.text)
                           if(jason['lang_code'] != 'gb'):
                               raise StopLookingForThings()
                           volume = jason["volume"]
                           if not os.path.exists(mangaName + "/" + volume):
                            os.makedirs(mangaName + "/" + volume)
                           chapter = jason['chapter']
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
            doDownload()
        except (StopLookingForThings):
               continue

fid=urllib.request.urlopen('https://mangadex.org/manga/' + sys.argv[1])
webpage=fid.read().decode('utf-8')
soup = BeautifulSoup(webpage,features="html.parser")
mangaName = soup.findAll("span",{"class":"mx-1"})[0].text
listChapters = soup.findAll("li",{"class":"page-item paging"})
if not listChapters:
    dl('https://mangadex.org/manga/' + sys.argv[1])
else:
    html = listChapters[0]
    href = [i.findAll('a', href=True) for i in soup.findAll("li",{"class":"page-item paging"})][0][0]["href"]
    mangaRaw = href.split('/')[2]
    maxChapter = href.split('/')[5]
    for x in range(int(maxChapter),0,-1):
        print("Downloading on https://mangadex.org/title/" + sys.argv[1] + "/" + mangaRaw + "/chapters/" + str(x))
        dl("https://mangadex.org/title/" + sys.argv[1] + "/" + mangaRaw + "/chapters/" + str(x))


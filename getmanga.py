import requests ,json, sys, re, os, shutil
from bs4 import BeautifulSoup
from optparse import OptionParser
import urllib.request

class SkipChapter(Exception): pass
class StopHere(Exception): pass

parser = OptionParser()
parser.add_option("-i","--id",type="int", help="the id of the mangaDex manga")
parser.add_option("-l","--language", help="language of the scan")
parser.add_option("-b","--range_min",type="int", help="Begining of the chapter to download (an int)")
parser.add_option("-e","--range_max",type="int", help="End of the chapter to download (an int)")

(opts, args) = parser.parse_args()
print(opts)

if(opts.id is None):
    print("Please provide an Id")
    parser.print_help()
    exit(-1)
if(opts.range_min and opts.range_max and opts.range_min > opts.range_max):
    print("wrong chapter range !!!")
    exit(-1)

listChapter = []
def getFromApi(listId):
    for id in listId.splitlines():
        r = requests.get("https://mangadex.org/api/?id=" + id  +"&server=null&saver=1&type=chapter", None)
        jason = json.loads(r.text)
        if(jason['lang_code'] != 'gb'):
            raise SkipChapter()
        volume = jason["volume"]
        if not os.path.exists(mangaName + "/" + volume):
            os.makedirs(mangaName + "/" + volume)
        chapter = jason['chapter']
        if(chapter in listChapters):
            continue
        listChapters.append(chapter)
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

def doDownload(line,lastChapter, begin, end):
    if ("/chapter/" in line and "comments" not in line):
        p = re.compile("<(.*)>(.*)</a>")
        result = p.search(line).group(2)
        if("Vol." in result):
            p = re.compile("Vol\. ([0-9]+) Ch. ([0-9]+)*")
            result2 = p.search(result)
            volume = result2.group(1)
            actualChapter = result2.group(2)
        else:
            p = re.compile("Ch. ([0-9]+)*")
            result2 = p.search(result)
            actualChapter = result2.group(1)
            volume = '0'
        if((begin is None and lastChapter != None and int(actualChapter) < int(lastChapter)) or (begin is not None and begin > int(actualChapter) )):
            raise SkipChapter()
        if (end and int(actualChapter) > end):
            raise StopHere()
        listId = line.split("'")[1].split("/")[2]
        fileChapter.seek(0)
        fileChapter.write(actualChapter)
        fileChapter.truncate()
        getFromApi(listId)

def dl(webpageHtml,lastChapter, begin , end):
    fid=urllib.request.urlopen(webpageHtml)
    webpage=fid.read().decode('utf-8')
    for line in reversed(webpage.splitlines()):
        try:
            doDownload(line,lastChapter, begin ,end)
        except (SkipChapter):
               continue
        except (StopHere):
               break

fid=urllib.request.urlopen('https://mangadex.org/manga/' + str(opts.id))
webpage=fid.read().decode('utf-8')
soup = BeautifulSoup(webpage,features="html.parser")
mangaName = soup.findAll("span",{"class":"mx-1"})[0].text
if not os.path.exists(mangaName):
    os.makedirs(mangaName)
if os.path.exists(mangaName + "/.currentDownload"):
    print("has current downloaddd")
    lastChapter = ''
    fileChapter = open(mangaName + "/.currentDownload", "r+")
    if(fileChapter.mode == 'r+'):
        while True:
            c = fileChapter.read(1)
            if not c:
                break
            lastChapter += c 
    if(lastChapter == ''):
        lastChapter = None
else:
    fileChapter = open(mangaName + "/.currentDownload", "w+")
    lastChapter = None

listChapters = soup.findAll("li",{"class":"page-item paging"})
if not listChapters:
    dl("https://mangadex.org/manga/" + str(opts.id) ,lastChapter, opts.range_min, opts.range_max)
else:
    html = listChapters[0]
    href = [i.findAll('a', href=True) for i in soup.findAll("li",{"class":"page-item paging"})][0][0]["href"]
    mangaRaw = href.split('/')[2]
    maxChapter = href.split('/')[5]
    for x in range(int(maxChapter),0,-1):
        print("Downloading on https://mangadex.org/title/" + str(opts.id) + "/" + mangaRaw + "/chapters/" + str(x))
        dl("https://mangadex.org/title/" + str(opts.id) + "/" + mangaRaw + "/chapters/" + str(x),lastChapter, opts.range_min, opts.range_max)
fileChapter.close()
os.remove(mangaName + "/.currentDownload")

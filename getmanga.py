import requests ,json, sys, re, os, shutil
import urllib.request
fid=urllib.request.urlopen('https://mangadex.org/manga/' + sys.argv[1])
webpage=fid.read().decode('utf-8')


for line in webpage.splitlines():
    if("class=\"mx-1\"" in line):
        mangaName = re.findall(r'<span class="mx-1">(.+?)</span>',line)[0]
        if os.path.exists(mangaName):
            shutil.rmtree(mangaName)
for line in webpage.splitlines():
    if ("/chapter/" in line):
        if ("comments" not in line):
            listid = line.split("'")[1].split("/")[2]
            for id in listid.splitlines():
               r = requests.get("https://mangadex.org/api/?id=" + id  +"&server=null&saver=1&type=chapter", None)
               jason = json.loads(r.text)
               chapter = jason['chapter']
               if not os.path.exists(mangaName + "/" + chapter):
                    os.makedirs(mangaName + "/" + chapter)
               url = jason['server'] + jason['hash'] 
               index = 0
               print("Saving chapter " + chapter + " of " + mangaName);
               for file in jason['page_array']:
                   print(url + "/" + file)
                   r = requests.get( url + "/" + file)
                   r.raw.decode_content = True
                   """urllib.request.urlretrieve( url + "/" + file, mangaName + "/" + chapter + "/" + file)"""
                   with open(mangaName + "/" + chapter + "/" + file, 'wb') as f:
                       f.write(r.content)


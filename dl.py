#!/usr/bin/env python
import requests, urllib2, os, shutil, sys, futures
from time import sleep

download_board = sys.argv[1]

def download(**kwargs):
    with open('./'+download_board+'/'+kwargs['filename'], 'wb') as handle:
        request = requests.get(kwargs['url'], stream=True)

        for block in request.iter_content(1024):
            if not block:
                break
            handle.write(block)

if os.path.exists("stopcron.txt"):
    print "stopcron.txt exists, downloader is aborting"
    exit()

if not os.path.exists(download_board+"-modified.txt"):
    shutil.copy(".backup_modified.txt", download_board+"-modified.txt")

if os.path.getsize(download_board+"-modified.txt") == 0:
    shutil.copy(".backup_modified.txt", download_board+"-modified.txt")

pages = []
with open(download_board+"-modified.txt", 'r') as f:
    modified = [s.strip("\n") for s in f.readlines()]

realch = 0
for a in xrange(15):
    p = requests.get("http://a.4cdn.org/"+download_board+"/%s.json" % str(a), headers={'If-Modified-Since': str(modified[a])})
    if p.status_code == 200 or len(modified[a]) == 0:
        pages.append(p.json())
        modified[a] = p.headers['Last-Modified'] 
        sleep(1.0)
    a = a + 1

with open(download_board+"-modified.txt", 'w') as f:
    for a in modified:
        f.write(a+"\n")
links = []

already = 0
links = []
filenames = []
for page in pages:
    for thread in page['threads']:
        for post in thread['posts']:
            if u'filename' in post:
                filename_clean = post[u'filename']
                ext_clean = post[u'ext']
                if 'filename' in post and not os.path.exists("./"+download_board+"/"+filename_clean+ext_clean):
                    links.append("http://i.4cdn.org/"+download_board+"/"+filename_clean+ext_clean)
                    filenames.append(filename_clean+ext_clean)

if not os.path.exists("./"+download_board+"/"):
    os.makedirs("./"+download_board+"/")

with futures.ThreadPoolExecutor(max_workers=10) as e:
    for i in xrange(len(links)):
        e.submit(download, url=links[i], filename=filenames[i])
print "[chanrip] %s downloaded" % (str(len(links)))

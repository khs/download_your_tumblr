import re
import sys
from   subprocess import call
from os import mkdir
 
# Name of the tumblr.
username = sys.argv[1]
 
# Download all the pages into a directory called Pages.
#call(["mkdir", "Pages"])
mkdir("Pages")
next_page   = 1
page_exists = True
while page_exists:
    #Figure out a way to replace this with urllib
    call(["wget", "http://"+username+".tumblr.com/page/"+str(next_page),\
          "-O", "Pages/page"+str(next_page)+".html"])
    page_exists = False
    # Read through current page looking for link to next page,
    # to see if it exists.
    pg1 = re.compile("http://"+username+".tumblr.com/page/"+str(next_page+1))
    pg2 = re.compile("<a href=\"/page/"+str(next_page+1)+"\">")
    f  = open("Pages/page"+str(next_page)+".html", "r")
    while True:
        # Read line.
        line = f.readline()
        if not line:
            break
        # Search line for correct URL.
        m1 = pg1.search(line)
        m2 = pg2.search(line)
        if m1 or m2:
            page_exists = True
    f.close()
    next_page += 1
 
# Go through all the pages.  Make a set of all the posts.
posts = set()
total_pages = next_page - 1
pst1 = re.compile("http://"+username+".tumblr.com/post/([0-9]*)[^0-9]")
pst2 = re.compile("<a href=\"/post/([0-9]*)/")
# For each page:
for page in range(total_pages):
    f  = open("Pages/page"+str(page+1)+".html", "r")
    # Scan page for mentions of posts.
    while True:
        # Read line.
        line = f.readline()
        if not line:
            break
        # Search line for mentions of posts.
        m1 = pst1.findall(line)
        m2 = pst2.findall(line)
        if len(m1) > 0:
            for num in m1:
                posts.add(num)
        if len(m2) > 0:
            for num in m2:
                posts.add(num)
    f.close()
 
# Download each post identified.
mkdir("Pages")
for p in posts:
    call(["wget", "http://"+username+".tumblr.com/post/"+p+"/",\
          "-O", "Posts/"+p])

import re
from sys import argv
from urllib.request import urlopen
from os import mkdir
from os import listdir

# Name of the tumblr.
username = argv[1]


def getPosts(contents, username, posts):
    pst1 = re.compile("http://"+username+".tumblr.com/post/([0-9]*)[^0-9]")
    pst2 = re.compile("<a href=\"/post/([0-9]*)/")
    for pst in [pst1, pst2]:
        m = pst.findall(contents)
        if len(m) > 0:
            for num in m:
                posts.add(num)
    return posts

if __name__ == "__main__":
    incremental = False
    try:
        mkdir(username)
        mkdir(username+"/Pages")
        mkdir(username+"/Posts")
    except FileExistsError:
        try:
            mkdir(username+"/Pages")
            mkdir(username+"/Posts")
            raise Exception(username+" is already a folder, but it wasn't made by this program.")
        except FileExistsError:
            incremental = True
            print("Tumblr previously downloaded. Continuing download. Pages will reflect new arrangement.")
    next_page   = 1
    page_exists = True
    posts       = set()
    while page_exists:
        # Figure out a way to replace this with urllib
        u = urlopen("http://"+username+".tumblr.com/page/"+str(next_page))
        with open(username+"/Pages/page"+str(next_page)+".html", "wb") as f:
            h = u.read()
            f.write(h)
        page_contents = str(h)
        # Read through current page looking for link to next page,
        # to see if it exists.
        pg1 = re.compile("http://"+username+".tumblr.com/page/"+str(next_page+1))
        pg2 = re.compile("<a href=\"/page/"+str(next_page+1)+"\">")
        m1 = pg1.search(page_contents)
        m2 = pg2.search(page_contents)
        if m1 or m2:
            page_exists = True
        else:
            page_exists = False
        posts = getPosts(page_contents, username, posts)
        next_page += 1
        if next_page > 10000:
            raise Exception("Program is not terminating on "+username+" and has collected 10000 pages already.")
    if next_page < 3:
        print("Probable bug: less than two pages saved.")
        print(username)
    # Download each post identified.
    existing = os.listdir(username+"/Posts")
    difference = [m for m in posts if m not in existing]
    for p in existing:
        u = urlopen("http://"+username+".tumblr.com/post/"+p)
        with open(username+"/Posts/"+p+".html", "wb") as f:
            f.write(u.read())

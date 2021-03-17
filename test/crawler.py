from bs4 import BeautifulSoup
import urllib.request
import re
import os
import ssl

url = 'https://vnexpress.net'
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
page = urllib.request.urlopen(url, context=ctx)
soup = BeautifulSoup(page, 'html.parser')
nav = soup.find(class_='main-nav')
li_list = nav.find_all("li")
dir_name = '/Users/shvu/Documents/school/LTMNC/crawl_exercise/data'
f = open(dir_name + '/data.txt', "w+", encoding='utf-8')
for li in li_list:
    link = li.find("a").get('href')
    title = li.find("a").get('title')
    if re.search('^/\w+', link):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        count = 0
        while True:
            sub_url = url + link
            page = urllib.request.urlopen(sub_url, context=ctx)
            sub_soup = BeautifulSoup(page, 'html.parser')
            new_feeds = sub_soup.findAll(class_='title-news')
            for nfeed in new_feeds:
                feed = nfeed.find("a")
                feed_title = feed.get('title')
                feed_link = feed.get('href')
                if feed_title == None or feed_title == "" or feed_link == None:
                    continue
                try:
                    f.write('\"' + feed_title + '\",' + title + '\n')
                    print(dir_name, count)
                    count += 1
                except:
                    pass
            next_page = sub_soup.find(class_='btn-page next-page')
            if next_page == None or count > 1000:
                break
            link = next_page.get('href')
f.close()
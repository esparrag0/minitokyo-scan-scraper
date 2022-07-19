import requests, bs4, sys, re
from pathlib import Path

def link_getter(res_link, link_segment):    
    res = requests.get(res_link)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content, 'lxml')
    links = soup.select('a')
    all_links = []
    for link in links:
        if link_segment in str(link):
            all_links.append(link)
    return all_links


res = requests.get('http://www.minitokyo.net/Darling in the FranXX')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.content, 'lxml')
links = soup.select('a')
all_links = []
for link in links:
    if 'http://browse.minitokyo.net/gallery/?tid=' in str(link):
        all_links.append(link)
scans_link = all_links[-1].get('href')

res = requests.get(scans_link)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.content, 'lxml')
all_links = soup.select('a')
links_list = []
for link in all_links:
    if 'http://gallery.minitokyo.net/view/' in str(link):
        image_link = link.get('href')
        res = requests.get(image_link)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.content, 'lxml')
        all_links = soup.select('a')
    if 'index=3&page=' in str(link):
        links_list.append(link)




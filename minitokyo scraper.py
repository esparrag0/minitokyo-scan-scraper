import requests, bs4, sys, re
from pathlib import Path

res = requests.get('http://www.minitokyo.net/Darling in the FranXX')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.content, 'lxml')
links = soup.select('a')
images_links = []
for link in links:
    if 'http://browse.minitokyo.net/gallery/?tid=' in str(link):
        images_links.append(link)
url = re.compile(r'http(.*)index=3')
scans_link = url.search(str(images_links[-1])).group()
scans_link = scans_link.split('amp;')
scans_link = scans_link[0] + scans_link[-1]

res = requests.get(scans_link)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.content, 'lxml')
images_links = soup.select('a')


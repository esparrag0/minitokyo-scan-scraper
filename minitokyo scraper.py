import requests, bs4, sys, os
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
os.makedirs('Darling in the Franxx')
scans_link = link_getter('http://www.minitokyo.net/Darling+in+the+FranXX', 'http://browse.minitokyo.net/gallery/?tid=')[-1].get('href')
image_link = link_getter(str(scans_link), 'http://gallery.minitokyo.net/view/')
for i, link in enumerate(image_link):
    image_link[i] = link.get('href')

download_links = []
for link in image_link:
    download_links.append(link_getter(str(link), 'http://static.minitokyo.net/downloads/')[0].get('href'))

for image in download_links:
    res = requests.get(image)
    res.raise_for_status()
    a = os.path.join('Darling in the Franxx', os.path.basename(image))
    print(a.replace('\\', ' '))
    imageFile = open(a.replace('\\', ' '),'wb')
    for chunk in res.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()


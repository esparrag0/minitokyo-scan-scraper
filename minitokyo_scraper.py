import requests, bs4, sys, os, re

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

    #Returns all the links of interest (the ones that contain link_segment) in the page given by res_link

def image_downloader(image_link):   
    for i, link in enumerate(image_link):
        image_link[i] = link.get('href')

    download_links = []
    for link in image_link:
        download_links.append(link_getter(str(link), 'http://static.minitokyo.net/downloads/')[0].get('href'))

    for image in download_links:
        res = requests.get(image)
        res.raise_for_status()
        imageFile = open(os.path.join(sys.argv[1], os.path.basename(image)),'wb')
        # Sets the pathfile in the .\sys.argv[1] directory and the filename as the basename of the image link.

        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()
    
    #Localizes all the scans of the page and downloads them in full size

os.makedirs(sys.argv[1], exist_ok=True)
scans_link = link_getter('http://www.minitokyo.net/' + sys.argv[1], 'http://browse.minitokyo.net/gallery/?tid=')[-1].get('href')

#Makes a directory for the scans and finds the url of the first scans' page

res = requests.get(scans_link)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.content, 'lxml')
page_range = str(soup.select('span[style="margin-right: 1em; "]')[0].getText)
page_regex = re.compile(r'">(.*)\n<i>')
page_range = page_regex.search(page_range).group(1)
last_page = page_range.split(' ')[-1]

#Finds the value of the last page of scans 

for i in range(1, int(last_page) + 1):
    page_link = scans_link + '&page=' + str(i)
    image_link = link_getter(str(page_link), 'http://gallery.minitokyo.net/view/')
    image_downloader(image_link)

#Loops through the different pages of scans and downloads each one of them
import os
import requests
from bs4 import BeautifulSoup

def crawl_image(image_url, image_local_path):
    r = requests.get(image_url, stream=True)
    with open(image_local_path, "wb") as f:
        f.write(r.content)

def gen_doc(first_url):
    doc_name = "_".join(first_url.split("/")[-3:-1])
    try:
        os.removedirs(doc_name)
    except:
        pass
    os.mkdir(doc_name)
    return "_".join(first_url.split("/")[-3:-1])

def crawl_image_list(raw_url):
    res = requests.get(raw_url)
    soup = BeautifulSoup(res.text, "html5lib")
    img_list = soup.find_all("div", class_="content")
    page_list = soup.find_all("div", class_="page")
    total_num = page_list[0].find_all("a")[-2].text
    first_url = img_list[0].a.img["src"]
    img_type = first_url.split('.')[-1]
    url_prefix = '/'.join(first_url.split('/')[:-1])
    img_url_list = []
    for i in range(1, int(total_num) + 1):
        img_url_list.append(url_prefix + "/" + str(i) + "." + img_type)
    return gen_doc(first_url), img_url_list

def crawl(mzid):
    raw_url = "http://www.mmjpg.com/mm/" + str(mzid)
    doc_name, img_url_list = crawl_image_list(raw_url)
    for img_url in img_url_list:
        local_path = "_".join(img_url.split('/')[-3:])
        crawl_image(img_url, doc_name + "/" + local_path)

if __name__ == '__main__':
    for i in range(1, 701):
        crawl(i)

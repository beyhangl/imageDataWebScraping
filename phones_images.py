import os
import re
import time
import argparse
import requests
import io
import hashlib
import itertools
import base64
from PIL import Image
from multiprocessing import Pool
from selenium import webdriver



def ensure_directory(path):
    if not os.path.exists(path):
        os.mkdir(path)

def largest_file(dir_path):
    def parse_num(filename):
        match = re.search('\d+', filename)
        if match:
            return int(match.group(0))

    files = os.listdir(dir_path)
    if len(files) != 0:
        return max(filter(lambda x: x, map(parse_num, files)))
    else:
        return 0

def fetch_image_urls(query, images_to_download):
    image_urls = set()

    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    browser = webdriver.Firefox(executable_path=r'C:\Users\asus\Documents\Bireysel_Projeler\Sahibinden\geckodriver.exe')

    browser.get(search_url.format(q=query))
    def scroll_to_bottom():
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    image_count = len(image_urls)
    delta = 0
    while image_count < images_to_download:
        print("Found:", len(image_urls), "images")
        scroll_to_bottom()

        images = browser.find_elements_by_css_selector("img.rg_ic")
        for img in images:
            image_urls.add(img.get_attribute('src'))
        delta = len(image_urls) - image_count
        image_count = len(image_urls)

        if delta == 0:
            print("Can't find more images")
            break

        fetch_more_button = browser.find_element_by_css_selector(".ksb._kvc")
        if fetch_more_button:
            browser.execute_script("document.querySelector('.ksb._kvc').click();")
            scroll_to_bottom()

    browser.quit()
    return image_urls

def persist_image(dir_image_src):
    label_directory = dir_image_src[0]
    image_src = dir_image_src[1]

    size = (256, 256)
    try:
        image_content = requests.get(image_src).content
    except requests.exceptions.InvalidSchema:
        # image is probably base64 encoded
        image_data = re.sub('^data:image/.+;base64,', '', image_src)
        image_content = base64.b64decode(image_data)
    except Exception as e:
        print("could not read", e, image_src)
        return False

    image_file = io.BytesIO(image_content)
    image = Image.open(image_file).convert('RGB')
    resized = image.resize(size)
    with open(label_directory + hashlib.sha1(image_content).hexdigest() + ".jpg", 'wb')  as f:
        resized.save(f, "JPEG", quality=85)

    return True

if __name__ == '__main__':
    label = []
    query = []
    count = 200
    with open('C:/Users/asus/Documents/Bireysel_Projeler/Sahibinden/Objeler/fasterrcnn_data.txt', 'r') as f:
        for phone in f:
            label.append(phone)
            query.append(phone)

    for i,x in enumerate(label):
        ensure_directory('F:/ResimlerTest/')

        query_directory = 'F:/ResimlerTest/' + str(label[i].replace("\n","")) + "/"
        ensure_directory(query_directory)

        image_urls = fetch_image_urls(query[i], count)

        values = [item for item in zip(itertools.cycle([query_directory]), image_urls)]

        print("image count", len(image_urls))

        pool = Pool(12)
        results = pool.map(persist_image, values)
        print("Images downloaded: ", len([r for r in results if r]))


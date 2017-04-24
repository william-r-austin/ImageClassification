from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from base64 import b64decode
from base64 import b64encode
from urllib.request import urlopen
import sys, os
from io import StringIO
from PIL import Image
import re
import unicodedata
from datetime import date
import time
from _datetime import datetime
from os import listdir
from os.path import isfile, join
import random
from asn1crypto._ffi import null
from edu.gmu.cs.ai.cs580.project.imageclassification import Constants

def slugify(value):
    slugified = "".join(x for x in value if (x.isalnum() or "-() ".find(x) >= 0))
    return slugified

def resize_photo(file_source, file_dest, newSize):
    try:
        im = Image.open(file_source)

        if im.mode != "RGB":
            im = im.convert("RGB")

        imthumb = im.resize(newSize, Image.ANTIALIAS)
        imthumb.save(file_dest, "JPEG")
    except Exception as exception:
        print("Exception for " + str(file_dest) + " is: " + str(exception))

def download_photo(img_url, filename):
    try:
        image_on_web = urlopen(img_url)
        if str(image_on_web.headers).index('Content-Type: image') >= 0:
            buf = image_on_web.read()
            # resize_photo(buf, filename)
            downloaded_image = open(filename, "wb")
            downloaded_image.write(buf)
            downloaded_image.close()
            image_on_web.close()
        else:
            return False
    except:
        return False
    return True

def execute_search(query, carIndicator):
    normalized = re.sub(' +', ' ', query)
    encodedQuery = normalized.replace(" ", "+")

    browser = webdriver.Firefox()
    url = 'https://images.google.com/?q=' + encodedQuery
    # print("Search URL is: " + url)
    browser.get(url)

    elem = browser.find_element_by_id('lst-ib')
    elem.send_keys(Keys.RETURN)

    sleep(1)
    # print("Initial sleep.")

    for i in range(250):
        browser.execute_script("window.scrollBy(0, 100)")
        sleep(0.1)

    # print("Done sleeping 1")

    more_elements_success = False
    try:
        elem = browser.find_element_by_id('smb')
        elem.click()
        more_elements_success = True
    except Exception as exception:
        print("Exception while finding/clicking smb element: " + str(exception))

    if more_elements_success:
        # print("Initial sleep 2.")

        for i in range(250):
            browser.execute_script("window.scrollBy(0, 100)")
            sleep(0.1)

        # print("Done sleeping 2, begin download.")

    content = browser.find_elements_by_css_selector('img.rg_ic.rg_i')

    download_images(content, query, carIndicator)
    browser.quit()

def create_thumbnails(rootDirectory, thumbnailSizes):
    imgDir = rootDirectory + 'Originals/'

    imageList = [f for f in os.listdir(imgDir) if isfile(join(imgDir, f))]

    for thumbSize in thumbnailSizes:

        thumbDir = rootDirectory + 'Thumbnails_' + str(thumbSize[0]) + '_' + str(thumbSize[1]) + '/'

        if not os.path.exists(thumbDir):
            os.makedirs(thumbDir)

        for originalImage in imageList:
            resize_photo(join(imgDir, originalImage), join(thumbDir, originalImage), thumbSize)

def create_annotation_file(rootDirectory, query, carIndicator, imageCount):
    with open(rootDirectory + 'annotation.txt', "w") as annotation_file:
        annotation_file.write(query + "\n")
        annotation_file.write(str(carIndicator) + "\n")
        annotation_file.write(str(imageCount) + "\n")

def download_images(content, query, carIndicator):

    current_time = datetime.now()
    folder_name = current_time.strftime("%Y-%m-%d %H-%M-%S (" + slugify(query) + ")")
    rootFolder = Constants.BASE_DATASET_FOLDER + folder_name + '/'
    originalsFolder = rootFolder + 'Originals/'

    if not os.path.exists(rootFolder):
        os.makedirs(rootFolder)

    if not os.path.exists(originalsFolder):
        os.makedirs(originalsFolder)

    imageCount = len(content)

    for j in range(imageCount):
        src_string = content[j].get_attribute('src')

        filename = originalsFolder + str(j + 1).zfill(4) + '.jpg'

        if src_string.startswith('data:image/jpeg;base64,'):
            base64Data = src_string.split(',')[1]
            # print("Base 64 Data " + str(j) + ": " + str(base64Data))
            imgdata = b64decode(bytearray(base64Data, "utf-8"))

            with open(filename, 'wb') as f:
                f.write(imgdata)

        elif src_string.startswith('https'):
            # print("URL Data " + str(j) + ": " + src_string)
            download_photo(src_string, filename)

    print("Successfully downloaded " + str(imageCount) + " images.")

    thumbSizes = [(150, 100), (75, 50), (36, 24)]
    create_thumbnails(rootFolder, thumbSizes)
    create_annotation_file(rootFolder, query, carIndicator, imageCount)

def retrieve_dataset():
    full_list = []

    for j in Constants.CARS_ITEMS:
        full_list.append((j, 1))

    for k in Constants.NOT_CARS_ITEMS:
        full_list.append((k, 0))

    random.shuffle(full_list)

    for g in full_list:
        current = datetime.now()
        date_str = current.strftime("%m/%d/%y %H:%M:%S")
        print(date_str + " => Executing search, query is: '" + g[0] + "', cars indicator is: " + str(g[1]))
        execute_search(g[0], g[1])

def main():
    retrieve_dataset()

if __name__ == "__main__":
    main()

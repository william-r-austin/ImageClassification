from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from base64 import b64decode
from base64 import b64encode
from urllib.request import urlopen
import sys, os
from io import StringIO
from PIL import Image

def resize_photo(file_path, file_dest):
    size = 150, 120
    try:
        im = Image.open(file_path)
        imthumb = im.resize((150, 100), Image.ANTIALIAS)
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



# filename = 'C:/imageDownloads/test.jpg'
# with open(filename, 'rb') as f:
#    encoded_string = b64encode(f.read())
#    print(encoded_string)

browser = webdriver.Firefox()

browser.get('https://images.google.com/?q=Buick+Verano')
# assert 'Yahoo' in browser.title


# download_photo("https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcShoSITepsK9gXmoGMYVgq3oB2MIrbLOBY6lairCVSkkEO1QQrb6g", "C:/imageDownloads/abc.jpg")
# quit()

# elem = browser.find_element_by_name('p')  # Find the search box
elem = browser.find_element_by_id('lst-ib')
elem.send_keys(Keys.RETURN)

sleep(1)
print("Initial sleep.")

for i in range(250):
    browser.execute_script("window.scrollBy(0, 100)")
    # print("Sleep #" + str(i))
    sleep(0.1)


print("Done sleeping 1")

elem = browser.find_element_by_id('smb')
elem.click()

print("Initial sleep 2.")

for i in range(250):
    browser.execute_script("window.scrollBy(0, 100)")
    # print("Sleep #" + str(i))
    sleep(0.1)



print("Done sleeping 2, begin download.")
content = browser.find_elements_by_css_selector('img.rg_ic.rg_i')

for j in range(len(content)):
    src_string = content[j].get_attribute('src')

    if src_string.startswith('data:image/jpeg;base64,'):
        base64Data = src_string.split(',')[1]
        print("Base 64 Data " + str(j) + ": " + str(base64Data))
        imgdata = b64decode(bytearray(base64Data, "utf-8"))
        filename = 'C:/imageDownloads/Originals/some_image_' + str(j) + '.jpg'  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
            f.write(imgdata)

        thumbname = 'C:/imageDownloads/Thumbnails/some_image_' + str(j) + '.jpg'
        resize_photo(filename, thumbname)


    elif src_string.startswith('https'):
        print("URL Data " + str(j) + ": " + src_string)
        filename = 'C:/imageDownloads/Originals/some_image_' + str(j) + '.jpg'
        download_photo(src_string, filename)
        thumbname = 'C:/imageDownloads/Thumbnails/some_image_' + str(j) + '.jpg'
        resize_photo(filename, thumbname)


# print("Content length = " + str(len(content)) + ", element 0 = " + str(content[0]))
# elem.send_keys(Keys.RETURN)

browser.quit()

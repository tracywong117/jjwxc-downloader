# -*- coding:utf8 -*-
import requests
import lxml.html
from itertools import product
from time import sleep
import random
import pathlib
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from txt2epub import Txt2Epub

chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# on windows, use the path to the chromedriver.exe
if sys.platform == 'win32':
    svc = webdriver.ChromeService(executable_path='./chromedriver.exe')
else:
    svc = webdriver.ChromeService()
    
driver = webdriver.Chrome(service=svc, options=chrome_options)


def jj_Download(chapters_url, chapters_title, novel_name):
    i = 0
    for u, t in product(chapters_url, chapters_title):
        i += 1
        if len(chapters_url) < i:
            return
        print(t + " Downloading......")

        driver.get(chapters_url[i - 1])

        # Wait for the noveltext div to appear (JS renders content into it)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.noveltext'))
            )
        except Exception:
            print(f"WARNING: timed out waiting for noveltext div for chapter: {t}")
            continue

        # Find the content child div: the one with the most text among noveltext's children
        try:
            noveltext_el = driver.find_element(By.CSS_SELECTOR, 'div.noveltext')
            child_divs = noveltext_el.find_elements(By.XPATH, './div')
            content_el = max(child_divs, key=lambda el: len(el.text.strip()), default=None)
            content_text = content_el.text.strip() if content_el and content_el.text.strip() else ''
        except Exception as e:
            print(f"WARNING: could not extract content for chapter: {t} ({e})")
            continue

        if not content_text:
            print(f"WARNING: empty content for chapter: {t}")
            continue

        # print(content_text)
        name = t
        content = '\n' + "##" + name + '\n' + content_text
        with open(novel_name, 'a', encoding="utf-8") as f:
            f.write(content)
            f.write('\n')
            f.close()
        sleep(random.random()*3+random.random())

id = input("Enter novelid:")
url = "http://www.jjwxc.net/onebook.php?novelid=" + id

res = requests.get(url).content
tree = lxml.html.fromstring(res)

chapters_url = tree.xpath('//tr[@itemprop="chapter"]//a/@href | //tr[@itemprop="chapter newestChapter"]//a/@href')

chapters_title = tree.xpath('//tr[@itemprop="chapter"]//a/text() | //tr[@itemprop="chapter newestChapter"]//a/text()')

novel = tree.xpath('//span[@itemprop="articleSection"]/text()')[0]

author = tree.xpath('//span[@itemprop="author"]/text()')[0]

print(f"Download {novel} by {author}")

novel_name = novel + ".txt"

image_element = tree.xpath('//img[@class="noveldefaultimage"]')[0]
image_url = image_element.get('src')

# downlaod the cover image  
response = requests.get(image_url)
filename = novel + '.jpg'
with open(filename, 'wb') as file:
    file.write(response.content)

print('Cover image downloaded successfully!')

jj_Download(chapters_url, chapters_title, novel_name)

driver.quit()

book = Txt2Epub(book_author=author)
book.create_epub(input_file=pathlib.Path(novel_name))
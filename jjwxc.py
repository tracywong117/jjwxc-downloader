# -*- coding:utf8 -*-
import requests
import lxml.html
from itertools import product

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

svc = webdriver.ChromeService(executable_path='./chromedriver')
driver = webdriver.Chrome(service=svc, options=chrome_options)


def jj_Download(chapters_url, chapters_title, novel_name):
    i = 0
    for u, t in product(chapters_url, chapters_title):
        i += 1
        if len(chapters_url) < i:
            return
        print(t + " Downloading......")

        # html = requests.get(chapters_url[i - 1]).content

        driver.get(chapters_url[i - 1])

        html = driver.page_source

        # print(html)
        # print(type(html))

        selector = lxml.html.fromstring(html)

        # clear_div = selector.xpath('//div[@style="clear:both;"]')
        # print(clear_div)
        # content_text = clear_div[0].xpath('following::text()[preceding::div[@style="clear:both;"]]')

        # Use XPath to select the content between <div style="clear:both;"></div> and <div align="right"></div>
        clear_div = selector.xpath('//div[@style="clear:both;"]')[0]  # Select the first <div> with style="clear:both;"
        right_div = clear_div.xpath('following::div[@align="right"]')[0]  # Select the <div> following the clear_div

        # Extract the text content between the two divs
        content_text = right_div.xpath('preceding-sibling::text()')
        if content_text:
            content_text = '\n'.join(content_text).strip()  # Join the text elements and remove leading/trailing whitespace

        # print(content_text)
        name = t
        content = '\n' + "##" + name + '\n' + content_text
        with open(novel_name, 'a', encoding="utf-8") as f:
            f.write(content)
            f.write('\n')
            f.close()

id = input("Enter novelid：")
url = "http://www.jjwxc.net/onebook.php?novelid=" + id

res = requests.get(url).content
tree = lxml.html.fromstring(res)

chapters_url = tree.xpath('//tr[@itemprop="chapter"]//a/@href | //tr[@itemprop="chapter newestChapter"]//a/@href')

chapters_title = tree.xpath('//tr[@itemprop="chapter"]//a/text() | //tr[@itemprop="chapter newestChapter"]//a/text()')

novel = tree.xpath('//span[@itemprop="articleSection"]/text()')[0]

author = tree.xpath('//span[@itemprop="author"]/text()')[0]

novel_name = novel + " " + author + ".txt"

jj_Download(chapters_url, chapters_title, novel_name)

driver.quit()


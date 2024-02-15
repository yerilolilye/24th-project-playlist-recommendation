from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from keybert import KeyBERT
from kiwipiepy import Kiwi
from transformers import BertModel
import json


url = input('도서 구매 사이트 url를 입력하세요(교보문고/yes24): ')

chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches",["enable-logging"])
chrome_options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
driver = webdriver.Chrome(options=chrome_options)

driver.get(url)
driver.implicitly_wait(2)

if url.startswith('https://product.kyobobook.co.kr'):
    book_inside = driver.find_element(By.CLASS_NAME, 'product_detail_area.book_inside')
    book_text = book_inside.find_element(By.CLASS_NAME, 'info_text').text
elif url.startswith('https://www.yes24.com'):
    book_inside = driver.find_element(By.ID, 'infoset_inBook')
    book_text = book_inside.find_element(By.CLASS_NAME, 'infoWrap_txt').text
else:
    print('지원하지 않는 도서 구매 사이트입니다.')
driver.close()


kiwi = Kiwi()

# 명사, 어근, 형용사 추출 함수
def main_extractor(text):
    results = []
    result = kiwi.analyze(text)
    for token, pos, _, _ in result[0][0]:
        if len(token) != 1 and pos.startswith('N') or pos.startswith('SL') or pos.startswith('XR') or pos.startswith('VA'):
            results.append(token)
    return results

book_text_extract = main_extractor(book_text)
book_keyword = [' '.join(book_text_extract)]
kw_model = KeyBERT(model='paraphrase-multilingual-MiniLM-L12-v2')
keywords = kw_model.extract_keywords(book_keyword, keyphrase_ngram_range=(1, 1),
                        use_mmr=True, diversity=0.3, top_n=10, stop_words=None)
keyword_text = [keyword[0] for keyword in keywords]
keyword_json = {"keywords": keyword_text}
with open('./data/keyword.json', 'w') as f:
    json.dump(keyword_json, f, ensure_ascii=False)

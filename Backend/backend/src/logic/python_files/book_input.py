import re
import sys
import requests
from bs4 import BeautifulSoup

from keybert import KeyBERT
from kiwipiepy import Kiwi

# 크롤링 함수
def book_crawling(site):
    url = "https://www.yes24.com/Product/Goods/" + site.split('/')[-1]
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    book_title = soup.find('h2',class_ = 'gd_name' ).text
    book_inside = soup.find('div', {'id': 'infoset_inBook'})
    book_review = soup.find('div', {'id': 'infoset_pubReivew'})
    book_intro = soup.find('div', {'id': 'infoset_introduce'})
    if book_inside is not None:
        book_text = book_inside.find('div', {'class': 'infoWrap_txt'}).text
    elif book_review is not None:
        book_text = book_review.find('div', {'class': 'infoWrap_txt'}).text
    elif book_intro is not None:
        book_text = book_intro.find('div', {'class': 'infoWrap_txt'}).text
    else:
        True
    book_text = re.sub(r'\n|\r|\t', '', book_text)

    return book_text, book_title


# 명사, 어근, 형용사 추출 함수
def main_extractor(book_text):
    kiwi = Kiwi()
    results = []
    result = kiwi.analyze(book_text)
    for token, pos, _, _ in result[0][0]:
        if len(token) != 1 and pos.startswith('N') or pos.startswith('SL') or pos.startswith('XR') or pos.startswith('VA'):
            results.append(token)
    return results


# 키워드 추출
def keybert_infernece(results):

    book_keyword = [' '.join(results)]
    kw_model = KeyBERT(model='paraphrase-multilingual-MiniLM-L12-v2')
    keywords = kw_model.extract_keywords(book_keyword, keyphrase_ngram_range=(1, 1),
                                         use_mmr=True, diversity=0.3, top_n=10, stop_words=None)
    keywords = ' '.join([keyword[0] for keyword in keywords])

    return keywords

# 메인
def keyword_extraction(site):

    book_text, book_title = book_crawling(site)
    results = main_extractor(book_text)
    keywords = keybert_infernece(results)

    return keywords, book_title

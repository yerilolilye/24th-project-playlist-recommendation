import re
import requests
from bs4 import BeautifulSoup

from keybert import KeyBERT
from kiwipiepy import Kiwi

# 크롤링 함수
def book_crawling():
    url = input('도서 구매 사이트 url를 입력하세요(yes24): ')
    if url.startswith('https://www.yes24.com'):
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
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
            print('해당 사이트에서 책 정보를 찾을 수 없습니다.')
        book_text = re.sub(r'\n|\r|\t', '', book_text)
    else:
        print('지원하지 않는 도서 구매 사이트입니다.')

    return book_text


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
def keyword_extraction():

    book_text = book_crawling()
    results = main_extractor(book_text)
    keywords = keybert_infernece(results)

    return keywords

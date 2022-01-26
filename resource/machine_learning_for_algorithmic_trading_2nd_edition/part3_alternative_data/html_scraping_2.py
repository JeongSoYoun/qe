
# Machine Learning For Algorithmic Trading 2nd Edition
# Steffen Jenson
# Part3 - Alternative Data

from email.mime import base
from urllib.parse import urljoin
from pathlib import Path
from bs4 import BeautifulSoup as bs
from furl import furl
from selenium import webdriver
import re
import random
import time

TRANSCRIPT_PATH = Path('transcript')
URL = 'https://seekingalpha.com/'
TRANSCRIPT = re.compile('Earnings Call Transcript')
DRIVER_DIR = '/Users/yoon/dev/qe/chromedriver'
SPEAKER_TYPES = ['Executives','Analysts']

def parse_html(html):

    print("parsing!")
    item, participants, content = {}, [], []
    date_pattern = re.compile(r'(\d{2})-(\d{2})-(\d{2})')
    quarter_pattern = re.compile(r'(\bQ\d\b)')
    parser = bs(html, 'lxml')
    
    headline = parser.find('h1', {'data-test-id': 'post-title'}).text
    # Kinder Morgan, Inc (KMI) CEO Steven Kean on Q4 2021 Results - Earnings Call Transcript
    item['company'] = headline[:headline.find('(')].strip()
    item['symbol'] = headline[headline.find('(') + 1:headline.find(')')]

    match = quarter_pattern.search(headline)
            
    if match: 
        item['quarter'] = match.group(0)

    qa = 0
    for header in [p.parent for p in parser.find_all('strong')]:

        text = header.text.strip()
        print(text)

        if text.lower().startswith('copyright'):
            continue

        elif text.lower().startswith('question-and'):
            qa = 1
            continue
        # SPEAKER_TYPES = ['Executives','Analysts']
        elif any(type in text for type in SPEAKER_TYPES):
            for participant in header.find_next_siblings('p'):
                if participant.find('strong'):
                    break
                else:
                    participants.append([text, participant.text])

        else:
            p = []
            for participant in header.find_next_siblings('p'):
                if participant.find('strong'):
                    break
                else:
                    p.append(participant.text)
            content.append([header.text, qa, '\n'.join(p)])
    
    print(content)
    return item, participant, content


if __name__ == '__main__':

    next_page = True
    page = 1
    driver = webdriver.Chrome(DRIVER_DIR)
    
    while next_page:

        url = f'/earnings/earnings-call-transcripts?page={page}'
        driver.get(urljoin(base=URL, url=url))
        html = driver.page_source
        page += 1
        parser = bs(html, 'lxml')
        links = parser.find_all(name='a', string=TRANSCRIPT)

        if len(links) == 0:
            next_page = False
        
        else:
            for link in links:
                
                transcript_url = link.attrs.get('href')
                article_url = furl(urljoin(URL, transcript_url)).add({'part': 'single'})
                driver.get(url=article_url.url)
                html = driver.page_source
                (item, participant, content) = parse_html(html=html)
                item['link'] = link
                time.sleep(2)

    driver.close()

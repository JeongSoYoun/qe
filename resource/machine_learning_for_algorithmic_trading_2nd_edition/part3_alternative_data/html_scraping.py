
# Machine Learning For Algorithmic Trading 2nd Edition
# Steffen Jenson
# Part3 - Alternative Data

import enum
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from time import sleep
from re import search 
import pandas as pd

DRIVER_DIR = '/Users/yoon/dev/qe/chromedriver'
URL = 'https://www.opentable.com/new-york-restaurant-listings'

def parse_html(html):

    # Initialize dataframe & item to store data from parsing HTML 
    (data, item) = pd.DataFrame(), {} 
    parser = bs(html, 'lxml')

    for (index, store) in enumerate(parser.find_all('div', {'class': 'rest-row-info'})):

        item['name'] = store.find('span', {'class': 'rest-row-name-text'}).text
        booking = store.find('div', {'class': 'booking'})
        item['booking'] = search('\d+', booking.text) if booking else 'NA'
        rating = store.find('div', class_='star-rating-score')
        item['rating'] = float(rating['aria-label'].split()[0]) \
            if rating else 'NA'
        reviews = store.find('span', class_='underline-hover')
        item['reviews'] = int(search('\d+', reviews.text).group()) \
            if reviews else 'NA'
        item['price'] = int(store.find('div', class_='rest-row-pricing')
                            .find('i').text.count('$'))
        cuisine_class = 'rest-row-meta--cuisine rest-row-meta-text sfx1388addContent'
        item['cuisine'] = store.find('span', class_=cuisine_class).text
        location_class = 'rest-row-meta--location rest-row-meta-text sfx1388addContent'
        item['location'] = store.find('span', class_=location_class).text
        data[index] = pd.Series(item)

    return data.T

if __name__ == '__main__':

    restaurants_df = pd.DataFrame()
    driver = webdriver.Chrome(DRIVER_DIR)
    
    # Open URL
    driver.get(URL)

    # Get HTML for URL
    while True: 

        sleep(1)
        html = driver.page_source
        new_data = parse_html(html=html)
        restaurants_df = pd.concat([restaurants_df, new_data], ignore_index=True)

        try:
            driver.find_element_by_link_text('Next').click()
        except Exception:
            print("No more pages")
            break
    
    print(restaurants_df)
    driver.close()
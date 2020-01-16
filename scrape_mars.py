from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd
import sys


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    # return Browser("chrome", **executable_path, headless=False)
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()

    url = f"https://mars.nasa.gov/news"
    browser.visit(url)
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    db = client.mars_db
    collection = db.news

    collection.drop()

    for x in range(1, 2):
        # Splinter can capture a page's underlying html and use pass it to BeautifulSoup to allow us to scrape the content
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # Using BS, we can execute standard functions to capture the page's content
        results = soup.find_all('div', class_='image_and_description_container')
    
        # The below loop will print out the current page number and the quote's text
        for result in results:
            try:
                # Identify and return title of listing
                date = result.find('div', class_='list_date').text
                title = result.find('div', class_='content_title').text
                article = result.find('div', class_='article_teaser_body').text
            
                # Run only if title, article content 
                if (title and article):
                    # Print results
                    # print('------------- Page -', x)
                    # print('news_date = ', date)
                    # print('news_title =', title)
                    # print('news_p =',article)

                    # Dictionary to be inserted as a MongoDB document
                    post = {
                        'news_date': date,
                        'news_title': title,
                        'news_p': article,
                    }
                    # Insert result into collection
                    collection.insert_one(post)

            except Exception as e:
                print(e)
    try:
        browser.click_link_by_href('#')    
    except Exception as e:
        x = 10
        print(e)    
    db = client.mars_db
    collection = db.figure

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')    
    browser.click_link_by_partial_text('more info')    

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('figure', class_='lede')
    print(results)

    for result in results:
    #        print(result.text)
            try:
                # Identify and return title of listing
                featured_image_url = 'https://www.jpl.nasa.gov' + result.find('a')['href']
                print(f'featured_image_url = ', featured_image_url)
                post = {
                        'featured_image_url': featured_image_url
                }
                # Insert result into collection
                collection.insert_one(post)
            except Exception as e:
                print(e)

    db = client.mars_db
    collection = db.weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div', class_='js-tweet-text-container')
    print(results[0], file=sys.stderr)
    try:
        # Identify and return title of listing
        fulltext = results[0].find('p', class_='TweetTextSize').text
        atext = results[0].find('a').text
        weather = fulltext.replace(atext, '')
        print(f'mars_weather = ', weather, file=sys.stderr)
        post = {
                'mars_weather': weather
        }
        # Insert result into collection
        collection.insert_one(post)
    except Exception as e:
        print(e)


    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    print(len(tables), file=sys.stderr)
    # print(type(tables))
    # print(type(tables[0]))
    df = tables[0]
    # df.head()
    # html_table = df.to_html(index=False)
    # html_table

    # html_table.replace('\n', '')

    df.rename(columns = {0:'Mars'}, inplace = True)
    df.rename(columns = {1:'Value'}, inplace = True)
    db = client.mars_db
    collection = db.facts
    df.reset_index(inplace=True)
    collection.insert_many(df.to_dict('records'))      

    db = client.mars_db
    collection = db.hemisphere
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Populate the list and get title
    hemi_title = []

    results = soup.find_all('h3')
    #print(results)

    for hemi in results:
        hemi_title.append(hemi.text)
    print(results[0], file=sys.stderr)
    # hemi_title
# st
    hemi_image_urls = []
    browser.visit(url)

    # Loop through the hemisphere links to obtain the images
    for hemi in hemi_title:
        # Initialize a dictionary for the hemisphere
        try:
            hemi_dict = {}

            # Click on the link with the corresponding text
            browser.click_link_by_partial_text(hemi)
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            results = soup.find_all('div', class_='content')
            #print(results)    
            browser.visit(url)
            for result in results:
                # Identify and return URL
                dts = result.find_all('dt')[1]
                hemi_image = result.find_all('dd')[1].find('a')['href']
                #print(hemi_image)
        
                # Run only if title and URL content 
                if (title and url):
                    # Print results
                    # print(f'-----------')
                    # print(f'title: ', hemi)
                    # print(f'img_url: ', hemi_image)
                    post = {
                            'title': hemi,
                            'img_url': hemi_image
                    }
                    # Insert result into collection
                    collection.insert_one(post)

        except Exception as e:
            print(e)        



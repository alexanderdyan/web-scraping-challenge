# Dependencies
import requests
import re 
import os
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs 
from splinter import Browser
from selenium import webdriver
import pymongo

def initBrowser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = initBrowser()
    newsUrl = 'https://mars.nasa.gov/news/'
    
    browser.visit(newsUrl)
        
    html=browser.html
    soup = bs(html, 'html.parser')
    newsTitle = soup.find('div', class_='content_title').text
    newsP = soup.find('div', class_='rollover_description_inner').text
    browser.quit()
    print(newsTitle)
    print(newsP)

    browser = initBrowser()
    jplNasaUrl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jplNasaUrl)
    html = browser.html
    jplSoup = bs(html, 'html.parser')
    featuredImageDiv = jplSoup.find('article', class_='carousel_item')
    #print(featuredImageDiv)
    articleStyle = featuredImageDiv.get('style')
    #get url from within style entry
    extractedURL = articleStyle[articleStyle.find("('")+2:articleStyle.find("')")]
    #create full url
    featuredMarsImgURL = 'http://www.jpl.nasa.gov' + extractedURL
    print('Image URL for featured image on Mars')
    print(featuredMarsImgURL)
    #visit img
    browser.visit(featuredMarsImgURL)

    #scrape the latest Mars weather tweet from the page. Save the tweet text weather report as a variable called mars_weather
    tweetUrl = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweetUrl)

    browser.is_element_present_by_css("section.css-1dbjc4n > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > article:nth-child(1) > div:nth-child(1) > div:nth-child(2)",wait_time=10)
    tweets = browser.find_by_css("#react-root > div > div > div.css-1dbjc4n.r-13qz1uu.r-417010 > main > div > div > div > div > div > div > div > div > div:nth-child(3) > section > div > div > div:nth-child(1) > div > div > div > div > article > div > div.css-1dbjc4n.r-18u37iz.r-thb0q2 > div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-5f2r5o.r-1mi0q7o > div:nth-child(2) > div:nth-child(1) > div > span")
    marsTweet = tweets[0].text
    #use pandas to convert the data to a HTML table str
    marsFacts = requests.get("https://space-facts.com/mars/")
    marsTable = pd.read_html(marsFacts.text)
    marsDf = marsTable[0]
    marsDf.set_index(0, inplace=True)
    marsDfHtml = marsDf.to_html()
    marsDfHtml
    hemImgUrls = []
    marsData = {'newsTitle': newsTitle, 'newsParagraph': newsP, 'featuredImg': featuredMarsImgURL, 'marsWeather': marsTweet, 'marsFacts': marsDfHtml, 'hemisphereImageURLs': hemImgUrls}
    return marsData
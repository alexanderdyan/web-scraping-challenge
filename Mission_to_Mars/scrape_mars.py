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
    executable path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = initBrowser()

    newsUrl = ''
    browser.visit(newsUrl)
    html=browser.html

    

#basic variables
url = 'https://mars.nasa.gov/news/'
response = requests.get(url)
response

app.config["MONGO-URI"] = "mongodb://localhost:27017/mars"

mongo = PyMongo(app)


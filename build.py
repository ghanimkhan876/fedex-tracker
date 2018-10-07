from distutils.core import setup
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

import py2exe

setup(console=['trackingtimes.py'])
html=browser.page_source
soup=BeautifulSoup(html,"lxml")
print soup.prettify()

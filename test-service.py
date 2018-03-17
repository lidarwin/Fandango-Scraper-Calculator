# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 10:19:07 2018

@author: Darwin Li

Simple script to test running headless chrome as a service using:
    https://duo.com/decipher/driving-headless-chrome-with-python
    https://sites.google.com/a/chromium.org/chromedriver/getting-started
        Controlling Lifetime
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.chrome.service as service

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_driver = os.getcwd() +"\\chromedriver.exe"

service = service.Service(chrome_driver)
service.start()
capabilities = {'chrome.binary': chrome_driver}
#driver = webdriver.Remote(service.service_url, capabilities)
driver = webdriver.Remote(service.service_url,   desired_capabilities=chrome_options.to_capabilities())
driver.get('http://www.google.com/xhtml');
driver.get_screenshot_as_file("testService.png")
time.sleep(5) # Let the user actually see something!
driver.quit()
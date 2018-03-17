# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15, 2018

@author: Darwin Li
"""
import os
import requests
from bs4 import BeautifulSoup
import datetime
import time
import re

from selenium import webdriver
import selenium.webdriver.chrome.service as service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

#https://medium.com/@pyzzled/running-headless-chrome-with-selenium-in-python-3f42d1f5ff1d


#List of all urls to every theater in America that is on Fandango.com
theaterLinks=[]

#List of all urls to every movie at every movietime sold on Fandango.com
#This list will get output in text file on the fly in case something goes wrong
movieTicketLinks=[]

#Dictionary of every ticket price in USA that is purchasable on Fandango.
#Maps float dollar ammount to a list of theater links. The information of the movie itself and the type (Adult, Child, Senior) is lost
ticketPrices = {}
    
def soupLink(url, baseURL='', headers={}):
    """ Takes in a URL and proceeds to return a BeautifulSoup HTML parsed object. BASEURL is required when the URL does not have HTTPS://
    """
    r = requests.get(baseURL + url, data={})
    c = r.content
    return BeautifulSoup(c,'html.parser')

#We don't want to have to run the script to generate the theater links every time, so we check if the file exists
if (not os.path.isfile('TheaterLinks.txt')):
    #The starting URL. It has Fandango's list of states which are links to the theaters in the states
    startURL = 'https://www.fandango.com/site-index/movietheaters.html'
    
    soup = soupLink(startURL)
    
    #List of all links to the state webpages
    #We only want the states in USA, not Canada, and other islands
    stateLinks = soup.find_all("a")
    stateLinks = stateLinks[0:52]
    
    with open('TheaterLinks.txt', 'a') as the_file:
        #To traverse each of the states, we need this base url
        baseURL = 'https://www.fandango.com/site-index/'
        for astate in stateLinks:
            soupstate = soupLink(astate['href'], baseURL)
            stateTheaterLinks = soupstate.find_all("a")
            for aStateTheater in stateTheaterLinks:
                theaterLinks.append(aStateTheater['href'])
                the_file.write(aStateTheater['href'] + '\n')                
else:
    with open('TheaterLinks.txt', "r") as myfile:
        theaterLinks = myfile.readlines()
        
        
# instantiate a chrome options object so you can set the size and headless preference
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

# current directory
chrome_driver = os.getcwd() +"\\chromedriver.exe"

def getPrices(ticketingUrl, theaterLink, ticketPrices):
    """ Takes in a TICKETINGURL and proceeds to checkout with all possible ticket types (Adult, Child, Senior). Saves the price for each ticket (with fandang convenience fee) as keys in a dictionary TICKETPRICES with the values as the THEATERLINK
    """
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
    
    driver.get(ticketingUrl)
    
    #The below are the commands in javascript that we need to do in JS and translate into selenium
    #document.getElementById('AreaRepeater_TicketRepeater_0_quantityddl_0').selectedIndex=1;
    #document.getElementsByClassName('qtyDropDowns')[0]
    #document.getElementById('NewCustomerCheckoutButton').click()
    #document.getElementById('purchaseTotal').textContent
    
    dropDownElements = driver.find_elements_by_class_name('qtyDropDown')
    for i in range(0, len(dropDownElements)):
        dropDownElements=driver.find_elements_by_class_name('qtyDropDown')
        quantSelect = Select(dropDownElements[i])
        quantSelect.select_by_index(1)
        driver.find_element_by_id('NewCustomerCheckoutButton').click()
        eTotal = driver.find_element_by_id('purchaseTotal')
        usdTotal = eTotal.get_attribute('textContent')
        fTotal = float(usdTotal[1:])
        if fTotal in ticketPrices:
            break;
        ticketPrices[fTotal] = theaterLink
        print(str(fTotal))
        driver.quit()
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
        driver.get(ticketingUrl)
    driver.quit()
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
    driver.get(ticketingUrl)
    #The below are the commands in javascript that we need to do in JS and translate to selenium
    #document.getElementsByClassName('input_txt')[0].value=1
    textInputElements = driver.find_elements_by_class_name('input_txt')
    for i in range(0, len(textInputElements)):
        textInputElements=driver.find_elements_by_class_name('input_txt')
        textInputElement = textInputElements[i]
        textInputElement.clear()
        textInputElement.send_keys('1')
        driver.find_element_by_id('NewCustomerCheckoutButton').click()
        eTotal = driver.find_element_by_id('purchaseTotal')
        usdTotal = eTotal.get_attribute('textContent')
        fTotal = float(usdTotal[1:])
        if fTotal in ticketPrices:
            break;
        ticketPrices[fTotal] = theaterLink
        print(str(fTotal))
        driver.quit()
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
        driver.get(ticketingUrl)



#For formatting when doing the requests
sTomorrow = str(datetime.date.today() + datetime.timedelta(1))

#Since we need a header to make it look like we are visiting on a desktop
userAgentHeader = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
userAgentHeader={'User-agent': 'Mozilla/5.0'}

itest=0

rMovieTimes=False
rUnlocker=False

#Start the Selenium server with the headless chrome driver
service = service.Service(chrome_driver)
service.start()
#Start Selenium webdriver service on the server in headless mode
driver = webdriver.Remote(service.service_url,   desired_capabilities=chrome_options.to_capabilities())

with open('TicketTransactionLinks.txt', 'a') as the_file:
    #Now go through every Theater in America
    for theaterLink in theaterLinks:
#        if (itest==0):
#            itest = itest+1
#            continue
#        itest = itest+1
#        if itest == 3:
#            break;
        #Strip is necessary because there is a /n at the end
        theaterLink=theaterLink.strip()
        #Need to find the code in the theater url. In TheaterLinks.txt, it follows underscore, but underscores become hyphens after the URL redirects
        m = re.search('.*_(.*)\/theaterpage', theaterLink)
        theaterCode = m.group(1)
        theaterLink = requests.get(theaterLink).url
        #Filters out the CLOSED theaters
        if ('404' in theaterLink):
            continue
        theaterSoup = soupLink(theaterLink)
        theaterLinkReqMovieTime='https://www.fandango.com/napi/theaterMovieShowtimes/'+theaterCode+'?startDate='+sTomorrow+'&isdesktop=true'
        theaterLinkReqMovieTimeValue=theaterLink+'?date='+sTomorrow
        
        data={'referer':theaterLinkReqMovieTimeValue}
        headers = {**data, **userAgentHeader}
        
        #For some reason, we need to REQUEST.GET this url below with key/value so that our IP will be unlocked or something
        #r = requests.get('https://www.fandango.com/napi/nearbyTheaters?limit=7&zipCode=99515', data = {'referer':'https://www.fandango.com/regal-dimond-center-9-cinemas-aacwx/theater-page?date=2018-03-16'},headers=headers)
        #So, we basically need the zipcode of the theater
        zipElement=theaterSoup.find_all("div", {"class": "js-closestTheaters-lazy"})
        sZipCode=zipElement[0].get('data-theater-zip')
        theaterUnlockerLink = 'https://www.fandango.com/napi/nearbyTheaters?limit=7&zipCode=' + sZipCode
        rUnlocker = requests.get(theaterUnlockerLink, headers=headers)
        while(True):
            if ('Not Authorized' in rUnlocker.text):
                print('Not Authorized when requesting the zipcode link')
                time.sleep(0.5)
                rUnlocker = requests.get(theaterUnlockerLink, headers=headers)
            else:
                break
        rMovieTimes = requests.get(theaterLinkReqMovieTime, headers=headers)
        while(True):
            if ('Not Authorized' in rUnlocker.text):
                print('Not Authorized when getting the Movie times')
                time.sleep(0.5)
                rMovieTimes = requests.get(theaterLinkReqMovieTime, headers=headers)
            else:
                break
        jMovieTimes = rMovieTimes.json()
        #jMovieTimes['viewModel']['movies'][1]['variants'][0]['amenityGroups'][0]['showtimes'][1]['ticketingUrl']
        jMovieTimes=jMovieTimes['viewModel']['movies']
        for movie in jMovieTimes:
            showtimes = movie['variants'][0]['amenityGroups'][0]['showtimes']
            for showtime in showtimes:
                ticketingUrl=showtime['ticketingUrl']
                movieTicketLinks.append(ticketingUrl)
                the_file.write(ticketingUrl + '\n')
                getPrices(ticketingUrl, theaterLink, ticketPrices)

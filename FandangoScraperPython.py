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
import selenium.webdriver.chrome.service as serv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

    
def soupLink(url, baseURL='', headers={}):
    """ Takes in a URL and proceeds to return a BeautifulSoup HTML parsed object. BASEURL is required when the URL does not have HTTPS://
    """
    r = requests.get(baseURL + url, data={})
    c = r.content
    return BeautifulSoup(c,'html.parser')


def getPrices(ticketingUrl, theaterLink, ticketPrices):
    """ Takes in a TICKETINGURL and proceeds to checkout with all possible ticket types (Adult, Child, Senior). Saves the price for each ticket (with fandang convenience fee) as keys in a dictionary TICKETPRICES with the values as the TICKETINGURL
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
        fTotal = fTotal*100
        iTotal = int(fTotal)
        if iTotal in ticketPrices:
            break;
        ticketPrices[iTotal] = ticketingUrl
        print(str(iTotal))
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
        fTotal = fTotal*100
        iTotal = int(fTotal)
        if iTotal in ticketPrices:
            break;
        ticketPrices[iTotal] = ticketingUrl
        print(str(iTotal))
        driver.quit()
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
        driver.get(ticketingUrl)

def fandangoCalculate(target, prices, error):
    ''' Takes a TARGET value, and a dictionary PRICES for which we are only concerned with the integer keys of, and returns an array of PRICES (with duplicates) that sum up to a value that is between TARGET and TARGET-ERROR. Basically solves the unbounded knapsack problem with dynamic programming with equal weighting on all items
    '''
    dp=[0]*(target + 1)
    #Store the index of dp as the key and the value as an array of prices that are needed with duplicates
    dic = {}
    prices = list(prices.keys())
    prices = prices.sort()
    for i in range(0,target):
        for j in range(0, len(prices)):
            if (prices[j] <= i):
                if (dp[i] < dp[i - prices[j]] + prices[j]):
                    dp[i] = dp[i - prices[j]] + prices[j]
                    if (i in dic):
                        dic[i] = dic[i].append(prices[j])
                    else:
                        dic[i] = [prices[j]]
    print(dp[target])
    print(dic[target])
    if (target - error <= dp[target]):
        return dic[target]
    else:
        return False
    

def main():
    target = 0.
    error = 0.
    code = 'r'
    while(True):
        s = input('Please enter desired amount to spend on Fandango followed by an amount to deviate from this, and then -a,-r,-[state code] for scraping alphabetically by state, randomly, or limited to a specific state by its state code \n An example input for scraping Alaskan theaters without calculation would be: \n 0 0 -ak \n An example of calculating a target value of $100.00 USD with deviation of $1.01 scraping theaters in states of no particular order would be:\n 100 1.01 -r')
        ''' To get the list of state codes, use the follow javascript:
            stri = ''
            for (i=0; i < document.links.length; i++) {
                    i = stri + document.links[i].href.substring(45,47)+'|'
            }
            console.log(stri)
        '''
        m = re.search('([0-9\.]+)\s([0-9\.]+)\s-(ak|al|ar|az|ca|ca|co|ct|dc|de|fl|ga|hi|ia|id|il|in|ks|ky|la|ma|md|me|mi|mn|mo|ms|mt|nc|nd|ne|nh|nj|nm|nv|ny|oh|ok|or|pa|ri|sc|sd|tn|tx|ut|va|vt|wa|wi|wv|wy|a|r)', s)
        if (m is not None):
            target = float(m[1])
            error = float(m[2])
            code = m[3]
            print('Starting...')
            break
        print('Input not understood. Make sure to use only lower-case')
    
    #List of all urls to every theater in America that is on Fandango.com
    theaterLinks=[]
    
    #List of all urls to every movie at every movietime sold on Fandango.com
    #This list will get output in text file on the fly in case something goes wrong
    movieTicketLinks=[]
    
    #Dictionary of every ticket price in USA that is purchasable on Fandango.
    #Maps float dollar ammount to a list of theater links. The information of the movie itself and the type (Adult, Child, Senior) is lost
    ticketPrices = {}
    
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
    
    
    #For formatting when doing the requests
    sTomorrow = str(datetime.date.today() + datetime.timedelta(1))
    
    #Since we need a header to make it look like we are visiting on a desktop
    userAgentHeader = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    userAgentHeader={'User-agent': 'Mozilla/5.0'}
    
    itest=0
    
    rMovieTimes=False
    rUnlocker=False
    
    #Start the Selenium server with the headless chrome driver
    service = serv.Service(chrome_driver)
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
            for i in range(0,1000):
                if ('Not Authorized' in rUnlocker.text):
                    print('Not Authorized when requesting the zipcode link')
                    time.sleep(0.5)
                    rUnlocker = requests.get(theaterUnlockerLink, headers=headers)
                else:
                    break
            rMovieTimes = requests.get(theaterLinkReqMovieTime, headers=headers)
            for i in range(0,1000):
                if ('Not Authorized' in rUnlocker.text):
                    print('Not Authorized when getting the Movie times')
                    time.sleep(0.5)
                    rMovieTimes = requests.get(theaterLinkReqMovieTime, headers=headers)
                else:
                    break
            try:
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
                        fandangoCalculated = fandangoCalculate(target, ticketPrices, error)
                        if (fandangoCalculated):
                            return fandangoCalculated
            except KeyboardInterrupt:
                return
            except:
                continue
            
if __name__ == '__main__':
    main()
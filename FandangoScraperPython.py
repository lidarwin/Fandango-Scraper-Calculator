import os
import requests
from bs4 import BeautifulSoup
import datetime


#List of all urls to every theater in America that is on Fandango.com
theaterLinks=[]

    
def soupLink(url, baseURL=''):
    """ Takes in a URL and proceeds to return a BeautifulSoup HTML parsed object. BASEURL is required when the URL does not have HTTPS://
    """
    r = requests.get(baseURL + url)
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

#Day of week is indexed as Sunday->0, Saturday ->6
#We only want 1 weekday and 1 weekend; no need to check multiple weekdays
#From a pricing perspective, Sunday is considered a Weekday
dayOfWeekToday=datetime.datetime.today().weekday()
dayOfWeekTomorrow = dayOfWeekToday + 1
diff = 6-dayOfWeekTomorrow
if (diff <= 0):
    diff = 2

#TWODATES is an array for use when we are on the calender wheel on a theater
#First entry is 1 because that is TOMORROW on the calender wheel
twoDates = [1, 1+diff]

itest=0
#Now go through every Theater in America
for theaterLink in theaterLinks:
    itest = itest+1
    if itest == 2:
        break;
    #Strip is necessary because there is a /n at the end
    theaterLink=theaterLink.strip()
    soupTheater = soupLink(theaterLink)
    soupCarasoul = soupTheater.find_all("section", {"class": "date-picker carousel js-movie-calendar carousel-style-strip"})
    r = requests.post('http://httpbin.org/post', data = {'key':'value'})
    
    
    

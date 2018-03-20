# Fandango-Scraper-Calculator
Ever wanted to monitor the trends in ticket prices in US movie theaters on Fandango? This script scrapes every unique ticket price on a given date (default is tomorrow's date) in every theater in USA. The source for every theater link is found on Fandango's website: https://www.fandango.com/site-index/movietheaters.html

Everything is written in Python, and for the scraping that can be done without a browser (because nervoussummer.com eventually blocks non-browser HTML requests), python requests and beautifulsoup4 are used. For the headless browser scraping, ChromeDriver and Selenium are used.

This is also a script that takes in a number in US Dollars and returns the Movie Ticket(s) that should be purchased from Fandango.com to achieve the sum. Use case is to maximize spend of Fandango Credits without going over and having to use a credit card. This is basically a special case of the unbounded knapsack problem, also called the Subset Sum problem https://en.wikipedia.org/wiki/Subset_sum_problem

Requirements (Everything is available on Anaconda except ChromeDriver, which is available from Google)
requests 2.18.4
beautifulsoup4 4.6.0
selenium 3.9.0 
ChromeDriver 2.37

Instructions:
1) Install Python 3.6.4 (independently or throguh Anaconda)
2) Use pip or Anaconda to install requests, beautifulsoup4, and selenium
3) Download chromedriver.exe from https://sites.google.com/a/chromium.org/chromedriver/downloads
4) Run fandango_scraper_calculator.py and follow the prompt
5) Follow below instructions for user input
To drive the script, the prompt will ask:
Please enter desired amount to spend on Fandango followed by an amount to deviate from this, and then -a,-r,-[state code] for scraping alphabetically by state, randomly, or limited to a specific state by its state code

An example input for scraping Alaskan theaters without calculation would be:
0.00 0.00 -ak

An example of calculating a target value of $100.00 USD with deviation of $1.01 scraping theaters in states of no particular order would be:
100.00 1.01 -r

Make sure that the input that follows the hyphen is always lower case. If a state is not recognized or the numerical values do not have enough precision in terms of the cents, then the prompt will appear again.

A sample output

Input:
60.06 0.00 -r

Output:
Buy 2 times at price: $5.18 from the link below:
https://tickets.fandango.com/Transaction/Ticketing/ticketboxoffice.aspx?row_count=214711646&tid=aainz&sdate=2018-03-20+13:30&mid=208042&from=mov_det_showtimes

Buy 1 times at price: $7.80 from the link below:
https://tickets.fandango.com/Transaction/Ticketing/ticketboxoffice.aspx?row_count=214711615&tid=aainz&sdate=2018-03-20+16:20&mid=209874&from=mov_det_showtimes

Buy 3 times at price: $7.50 from the link below:
https://tickets.fandango.com/Transaction/Ticketing/ticketboxoffice.aspx?row_count=216545650&tid=aawdu&sdate=2018-03-20+11:30&mid=208220&from=mov_det_showtimes

Buy 1 times at price: $9.50 from the link below:
https://tickets.fandango.com/Transaction/Ticketing/ticketboxoffice.aspx?row_count=216545646&tid=aawdu&sdate=2018-03-20+13:30&mid=208042&from=mov_det_showtimes

Buy 1 times at price: $9.90 from the link below:
https://tickets.fandango.com/Transaction/Ticketing/ticketboxoffice.aspx?row_count=214711616&tid=aainz&sdate=2018-03-20+22:10&mid=209874&from=mov_det_showtimes
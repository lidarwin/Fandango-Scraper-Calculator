# Fandango-Calculator
Ever wanted to monitor the trends in ticket prices in US movie theaters on Fandango? This script scrapes every unique ticket price on a given date (default is tomorrow's date) in every theater in USA. The source for every theater link is found here on Fandango's website: https://www.fandango.com/site-index/movietheaters.html

Everything is written in Python, and for the scraping that can be done without a browser (because nervoussummer.com eventually blocks non-browser HTML requests), requests 2.18.4 and beautifulsoup4 4.6.0 are used. For the headless browser scraping, ChromeDriver 2.37 and Selenium 3.9.0 are used

This is also a script that takes in a number in US Dollars and returns the Movie Ticket(s) that should be purchased from Fandango.com to achieve the sum. Use case is to maximize spend of Fandango Credits without going over and having to use a credit card. This is basically a special case of the unbounded knapsack problem, also called the Subset Sum problem https://en.wikipedia.org/wiki/Subset_sum_problem

"""
TopUniversities.com QS World University Rankings Scraper

This code provides a tool which can be used to scrape data from TopUniversities.com's QS World University Rankings, such as https://www.topuniversities.com/university-rankings/university-subject-rankings/2020/engineering-technology

Authour: Ethan Baron
Date: February 2021

Instructions:
Fill in the url and filename and table_number below.
Then, follow the instructions as prompted by the script.
You will need to have installed the most recent chromedriver.exe from https://chromedriver.chromium.org/downloads.
"""

url = 'https://www.topuniversities.com/university-rankings/university-subject-rankings/2020/engineering-technology'
filename = '2020_Engineering_University_Rankings.csv'

# Packages
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver

# Prepare dataframe
df = pd.DataFrame(columns = ['University', 'City', 'Country', 'Rank', 'Score'])

# Function to load university details from html
def get_university_details(row):
    def get_rank(row):
        return row.find('div', {'class': "_univ-rank hide-this-in-mobile-indi"}).text
    def get_score(row):
        return row.find('span', {'class': "overall-score-span hide-this-in-mobile-indi"}).text
    def get_university(row):
        return row.find('div', {'class': "td-wrap"}).text.strip()
    def get_location(row):
        return row.find('div', {'class': "location"}).text.strip()
    def get_city(location):
        if ',' in location:
            return location.split(',')[0].strip()
        else:
            return None
    def get_country(location):
        if ',' in location:
            return location.split(',', maxsplit=1)[1].strip()
        else:
            return location.strip()

    return get_university(row), get_city(get_location(row)), get_country(get_location(row)), get_rank(row), get_score(row)

# Function to load pandas DataFrame froum beautiful soup
def get_dataframe_from_soup(soup):
    rows = soup.find('div', {'id': 'ranking-data-load'}).find_all('div', {'class': '_qs-ranking-data-row'})
    return pd.DataFrame([get_university_details(row) for row in rows], columns = ['University', 'City', 'Country', 'Rank', 'Score'])

# Load website
driver = webdriver.Chrome()
driver.get(url)
input("Please click the dropdown at the bottom of the table and select the option to show 100 results per page.\nWhen the page has finished re-loading, press enter here.")
num_pages = int(input("Please enter the number of pages in the table (see the bottom of the table): --> "))

# Iterate over each page in table and add data to dataframe
for i in range(num_pages):
    soup = bs(''.join(driver.execute_script('return document.body.innerHTML')), 'html.parser')
    df = pd.concat([df, get_dataframe_from_soup(soup)]).reset_index(drop=True)
    print(f"Finished loading page {i+1}.")
    if i < num_pages - 1:
        input(f"Please click the next page button and press enter here after page {i+2} has finished loading.")

# Close web driver and save data to file
driver.close()
df.to_csv(filename) # Exports table to CSV file (which can be opened in Excel)
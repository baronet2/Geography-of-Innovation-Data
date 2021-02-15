"""
WIPO Scraper

This code provides a tool which can be used to scrape data from WIPO statistical country profiles, such as https://www.wipo.int/ipstats/en/statistics/country_profile/profile.jsp?code=CA.

Authour: Ethan Baron
Date: February 2021

Instructions:
Fill in the url, filename and table_number below.
The table_number corresponds to the table you want from the page, as per the list below.
If you would like to load more than one table from the same webpage, copy and paste the code labelled "Loads table from page" and change the filename in between.

'IP Filings': 2,
'Patent Applications': 4,
'Patent Grants': 5,
'Patents in Force': 6,
'Utility Model Applications': 7,
'Classes in Trademark Applications': 9,
'Classes in Trademark Registrations': 10,
'Designs in Industrial Design Applications': 12,
'Designs in Industrial Design Applications': 13,
'International Applications': 15,
'PCT National Phase Entry': 16,
'PCT Top Applicants': 17,
'Madrid Top Applicants': 18,
'Hague Top Applicants': 19
"""

url = 'https://www.wipo.int/ipstats/en/statistics/country_profile/profile.jsp?code=CA'
filename = 'Data.csv'
table_number = 2


# Packages
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# Function to load tables from page
def get_data(ts, table_number):
    """ 
    Return pd.DataFrame of table with number as listed above """
    return pd.read_html(str(ts[table_number]), header=0)[0]


# Loads page
page = requests.get(url)
soup = bs(page.text, 'html.parser')
ts = soup.find_all('table')

# Loads table from page
df = get_data(ts, table_number)
df.to_csv(filename) # Exports table to CSV file (which can be opened in Excel)
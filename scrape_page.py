import urllib.request
from bs4 import BeautifulSoup
import pandas as pd


column_headings = ["HelmName", "Class", "PY", "SailNo", "Fleet", "Rank", "Elapsed", "Corrected", "Points", "Reg No.", "Reg Date"]

url = 'https://www.warsashsc.org.uk/results/18wa1.htm'

with urllib.request.urlopen(url) as response:
   html = response.read()

soup = BeautifulSoup(html)

tables = soup.findAll('table')

def get_dataframe_from(table):
    """Turn a table into a data frame."""
    table_rows = table.find_all('tr')
    l = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        l.append(row)
    df = pd.DataFrame(l, columns=column_headings)
    
    return df

for table in tables:
    print(get_dataframe_from(table))

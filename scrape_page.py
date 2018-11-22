import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.warsashsc.org.uk/results/18wa1.htm'

with urllib.request.urlopen(url) as response:
   html = response.read()

soup = BeautifulSoup(html)

table = soup.find('table', attrs={'class':'subs noBorders evenRows'})
table_rows = table.find_all('tr')

l = []
for tr in table_rows:
    td = tr.find_all('td')
    row = [tr.text for tr in td]
    l.append(row)
df = pd.DataFrame(l)

print(df)

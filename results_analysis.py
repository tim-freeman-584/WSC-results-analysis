"""Module of helper functions for analysing WSC dinghy racing results."""
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def scrape_race(url):
    """Scrape all the results for a single race."""
    print(url)
    with urllib.request.urlopen(url) as response:
        html = response.read()

    soup = BeautifulSoup(html)

    tables = soup.findAll('table')
    return tables[:4]


def get_dataframe_from(table):
    """Turn a table into a data frame."""
    table_rows = table.find_all('tr')
    l = []
    for tr in table_rows[1:]:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        l.append(row)

    df = pd.DataFrame(l, columns=[tr.text for tr in table_rows[0].find_all('th')])

    return df


def get_all_results_for_year(year):
    base_url = 'https://www.warsashsc.org.uk/results/{}'.format(year)
    series = ['wa', 'wb', 'wc', 'fa', 'fb', 'fc']

    all_races_frames = []
    race_on = []

    for s in series:
        for i in range(1, 9):
            try:
                race = scrape_race(base_url + s + str(i) + '.htm')

                for table in race:
                    df = get_dataframe_from(table)
                    df['Day'] = s[0]
                    df['Series'] = s[1]
                    df['Race'] = i

                    all_races_frames.append(df)

                race_on.append(True)
            except Exception as e:
                print(e)
                print('No racing')
                race_on.append(False)

    return (pd.concat(all_races_frames, sort=True), race_on)

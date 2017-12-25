import re
import sys
import csv
import time
import random
import json
import requests
from datetime import date
from lxml import html
from bs4 import BeautifulSoup


## TODO
## Output table into csv
## Combine CSV into single file for data exploration

## Iterate through top 200 coins and pull names into a list
base_url = "https://api.coinmarketcap.com/v1/ticker/?limit=200"
r = requests.get(url = base_url)
data = r.text
json_data = json.loads(data)
coins = []; 
for dict in json_data: # generate list of coins 
    coins.append(dict['id'])

print(coins)

## Use list to pull historical data for each coin 
end_date = str(date.today()).replace("-", "")
base_url = "https://coinmarketcap.com/currencies/{0}/historical-data/?start=20130428&end=" + end_date ; 

def get_data(coin):
    print("Currency :", coin) # todo change to 'coin'
    url = base_url.format(coin)
    html_response = requests.get(url).text.encode('utf-8')
    soup = BeautifulSoup(html_response, 'html.parser')
    table = soup.find_all('table')[0]
    elements = table.find_all("tr")
    with open(".{0}_price.csv".format(coin.replace("-","_")),"w") as ofile:
        writer = csv.writer(ofile)
        for element in elements:
                writer.writerow( element.get_text().strip().split("\n") )
        
if __name__ == "__main__":
    for coin in coins:
            print(coin)
            get_data(coin)
            pass  
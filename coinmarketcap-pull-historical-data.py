#! python3
## coinmarketcap-pull-historical-data.py
## Uses CoinMarketCap API to pull list of top 200 coins by marketcap, 
## then parses html of each coins historical page to generate consolidated table of historical price data.

import re, sys, csv, time, random, json, requests, os
from datetime import date
from lxml import html
from bs4 import BeautifulSoup
from tkinter import filedialog 
import pandas as pd

## TODO
## Combine CSV into single file for data exploration

## Iterate through top 200 coins and pull names into a list
base_url = "https://api.coinmarketcap.com/v1/ticker/?limit=200"
r = requests.get(url = base_url)
data = r.text
json_data = json.loads(data)
coins = []; 
for dict in json_data: # generate list of coins 
    coins.append(dict['id'])
num_coins = len(coins)

## Use list to pull historical data for each coin 
end_date = str(date.today()).replace("-", "")
base_url = "https://coinmarketcap.com/currencies/{0}/historical-data/?start=20130428&end=" + end_date ; 
def get_data(coin):
    print("Percentage complete: " + percentage + "% | " "Currency :", coin) 
    url = base_url.format(coin)
    html_response = requests.get(url).text.encode('utf-8')
    soup = BeautifulSoup(html_response, 'html.parser')
    table = soup.find_all('table')[0]
    elements = table.find_all("tr")
    with open("{0}_price.csv".format(coin.replace("-","_")),"w") as csvfile:
        ## Output table into csv
        writer = csv.writer(csvfile)
        for element in elements:
            writer.writerow([coin] +  element.get_text().strip().split("\n"))

# Generate new folder to store consolidated csv
cwd = str(os.getcwd())
if os.path.exists(cwd + '/' + 'CoinData_' + str(end_date)) == False: # Check to see if updated folder exists, otherwise generate new folder with today's date
    cwd = os.makedirs(cwd + '/' + 'CoinData_' + str(end_date)); 
    os.chdir(cwd)
else:
    os.chdir(cwd + '/' + 'CoinData_' + str(end_date))
    cwd = os.getcwd()

# generate csv files
i = 0
''' if __name__ == "__main__":
    print("Pulling data for " + str(num_coins) + " coins . . . ")
    for coin in coins:
            percentage = str(round((i/num_coins)*100, 2)) 
            get_data(coin)
            i += 1
            pass   '''
 
# Iterate through all csv files in directory 
cwd = os.getcwd()
consolidated_coin_data = []
for filename in os.listdir(cwd):
    if filename.endswith('.csv'):
        current_csv = open(filename)
        csv_reader = csv.reader(current_csv)
        for row in csv_reader:
            if csv_reader.line_num == 1: # skip headers when copying coin data, these are added at a later time
                continue          
            consolidated_coin_data.append(row)
        current_csv.close()  

# initialize consolidated coin data csv file and write headers
with open('consolidated_coin_data.csv', 'a') as outcsv:
    writer = csv.writer(outcsv)
    writer.writerow(["Currency", "Date", "Open", "High", "Low", "Close", "Volume", "Market Cap"])

# transform list into csv file
for line in consolidated_coin_data:
    with open('consolidated_coin_data.csv', "a") as consolidatedcsv:
        wr = csv.writer(consolidatedcsv)
        wr.writerow(line)

print("Complete! Don't forget to hodl.")
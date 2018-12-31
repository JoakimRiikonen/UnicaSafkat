import requests
import time
import datetime
from bs4 import BeautifulSoup
import lxml
import json
import os
import redis

# setting up redis
r = redis.from_url(os.environ.get("REDIS_URL") or "127.0.0.1:6379")

# links to the restaurants
links = ['assarin-ullakko',
         'brygge',
         'delica',
         'deli-pharma',
         'dental',
         'galilei',
         'macciavelli',
         'nutritio',
         'ruokakello',
         'tottisalmi']

# the data
data = {}

# the week
date = datetime.date.today()
# isocalendar returns tuple, week is the second value in that tuple
data["week"] = date.isocalendar()[1]

# get the menus in the restaurants
for link in links:
    data[link] = {}

    full_addr = "https://www.unica.fi/fi/ravintolat/" + link + "/"

    site = requests.get(full_addr)
    if site.status_code != 200:
        print("Error fetching site" + link + ", status code " + site.status_code)
        continue

    # using lxml because the html of the site is broken and html.parser doesnt work
    soup = BeautifulSoup(site.text, 'lxml')

    try:
        menuList = soup.find('div', {'class': 'menu-list'})
        accords = menuList.find_all('div', {'class': 'accord'})

        for accord in accords:
            day = accord.find('h4').text
            data[link][day] = []
            lunches = accord.find_all('td', {'class': 'lunch'})
            prices = accord.find_all('td', {'class': 'price quiet'})
            for i in range(len(lunches)):
                # food item
                lunch = lunches[i].text
                # price
                price = ' '.join(prices[i].text.split())
                data[link][day].append({"lunch": lunch, "price": price})

        print(link + ", data fetched")

        time.sleep(1)
    except:
        print(link + ", failed to retrieve data")
        continue

# saving data as string to redis
jsonString = json.dumps(data)
r.set("scrapedata", jsonString)

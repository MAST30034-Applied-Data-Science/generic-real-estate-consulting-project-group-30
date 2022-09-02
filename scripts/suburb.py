# import libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

# get URL
url = "https://www.domain.com.au/liveable-melbourne/melbournes-most-liveable-suburbs-2019/melbournes-307-suburbs-ranked-for-liveability-2019-898676"
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, "html.parser")


# all suburb names are tagged with <strong>
suburbs = soup.findAll("strong")


suburb_list = []
for i in range(len(suburbs)):
    suburb = suburbs[i].text
        
    # remove the number and other uneccessary(how do I spell this word?) characters
    text = re.search(r'[a-zA-Z\s]+', suburb)[0].strip()
    # Including the false positive texts we have picked up, which is only "Previous rank"
    if text == "Previous rank":
        continue
    else:
        suburb_list.append(text)

# save the list of suburbs to csv
df = pd.DataFrame({"suburb": suburb_list})
df.to_csv("../data/raw/suburb.csv", index=False)
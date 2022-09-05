"""
This program generates every single possible suburb URL using domain.com.au's autocomplete search feature
Outputs to csv
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from tqdm import tqdm
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

# NOTE: run suburb.py before running this script
suburbs = pd.read_csv("../data/raw/suburb.csv")

suburbs = suburbs["suburb"].tolist()

suburb_urls = []

d = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
delay = 5
for i in tqdm(range(len(suburbs))):
  suburb = suburbs[i]
  d.get('https://www.domain.com.au/rent/?ssubs=0')
  myElem = WebDriverWait(d, delay).until(EC.presence_of_element_located(("id", 'search-filters-typeahead-input')))
  e = d.find_element("id", 'search-filters-typeahead-input')
  WebDriverWait(d, 10).until(EC.element_to_be_clickable(
        ("id", 'search-filters-typeahead-input'))).click()
  for c in suburb:
    e.send_keys(c)
  time.sleep(2)
  WebDriverWait(d, 10).until(EC.element_to_be_clickable(
        ("id", 'search-filters-typeahead-input'))).click()
  e.send_keys(Keys.RETURN)
  e.send_keys(Keys.RETURN)
  # print("link", d.current_url)
  suburb_urls.append(d.current_url)
  
# save the list of suburbs to csv
df = pd.DataFrame({"suburb_url": suburb_urls})
df.to_csv("../data/raw/suburb_urls.csv", index=False)
  
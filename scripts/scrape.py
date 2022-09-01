"""
A very simple and basic web scraping script. Feel free to
use this as a source of inspiration, but, make sure to attribute
it if you do so.

This is by no means production code.
"""
# built-in imports
import re
from json import dump

from collections import defaultdict

# user packages
from bs4 import BeautifulSoup
from urllib.request import urlopen

# additional import required from discord announcement
import requests

# constants
BASE_URL = "https://www.domain.com.au"
N_PAGES = 3 # update this to your liking
PROPERTY_FEATURES = {"Bed", "Bath", "Park"}

# NOTE: IT'S LITERALLY GOING TO TAKE A REEEEEEAAAAALLLLYYY LONG TIME TO RUN THIS CODE. 
# Especially if there are many number of pages. BE PATIENT.

# begin code
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
url_links = []
property_metadata = defaultdict(dict)

# generate list of urls to visit
for page in range(1, N_PAGES):
    url = BASE_URL + f"/rent/?sort=dateupdated-desc&state=vic&page={page}"
    bs_object = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")

    # find the unordered list (ul) elements which are the results, then
    # find all href (a) tags that are from the base_url website.
    index_links = bs_object \
        .find(
            "ul",
            {"data-testid": "results"}
        ) \
        .findAll(
            "a",
            href=re.compile(f"{BASE_URL}/*") # the `*` denotes wildcard any
        )

    for link in index_links:
        # if its a property address, add it to the list
        if 'address' in link['class']:
            url_links.append(link['href'])

# for each url, scrape some basic metadata
for property_url in url_links[1:]:
    bs_object = BeautifulSoup(requests.get(property_url, headers=headers).text, "html.parser")

    # looks for the header class to get property name
    property_metadata[property_url]['name'] = bs_object \
        .find("h1", {"class": "css-164r41r"}) \
        .text

    # looks for the div containing a summary title for cost
    property_metadata[property_url]['cost_text'] = bs_object \
        .find("div", {"data-testid": "listing-details__summary-title"}) \
        .text

    # extract coordinates from the hyperlink provided
    # i'll let you figure out what this does :P
    # Andrew: well, ummm...the link in bs_object takes you to the location of the property in gmaps.
    property_metadata[property_url]['coordinates'] = [
        float(coord) for coord in re.findall(
            r'destination=([-\s,\d\.]+)', # use regex101.com here if you need to
                                          # Andrew: this is obviously the location 
                                          # coordinate written in the gmaps link.
            bs_object \
                .find(
                    "a",
                    {"target": "_blank", 'rel': "noopener noreferer"}
                ) \
                .attrs['href']
        )[0].split(',')
    ]

    
    # want to extract the number of beds, baths and parking spaces from the features displayed on website
    feature_data = bs_object \
        .find_all("span", class_= "css-lvv8is")
    
    # for each of the divs we have found
    for fd in feature_data:
        # check which feature it matches (this avoids typos)
        for feature in PROPERTY_FEATURES: 
            if feature in fd.text[1:]:
                # assign the values; '-' replaced with 0.
                property_metadata[property_url][feature] =  fd.text[0] if fd.text[0].isnumeric() else 0
                
    # the code below extracts property type
    p_type = bs_object \
        .find("div", {"data-testid":"listing-summary-property-type"}).text
    property_metadata[property_url]["property_type"] = p_type if p_type is not [] else "Not Listed"
    
    property_metadata[property_url]['desc'] = re \
        .sub(r'<br\/>', '\n', str(bs_object.find("p"))) \
        .strip('</p>')
    
    
    # TODO: Add code here that scans the webpage for units of sqkm /acres/ etc and then adds an "area" feature. 
    # Part 1: extract from given area info (not from desc)
    p_area = bs_object \
    .find(
        "ul",
        {"data-testid": "listing-summary-strip"}
    ) \
    .find_all(
        "li"
    )
    # p_area = [elem for elem in p_area if ("area" in elem)]
    for elem in p_area:
        if "m<sup>" in elem:
            print(elem)
    # print(p_area)
    # TODO: this doesnt work when searching for the substring area but does for the others idk why
    
    # Part 2: using the desc generated above, find if there are any area properties 
    
# output to example json in data/raw/
with open('../data/raw/example.json', 'w') as f:
    dump(property_metadata, f)
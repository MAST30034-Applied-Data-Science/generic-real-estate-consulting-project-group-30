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
import pandas as pd

# user packages
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests

# for testing purposes
from tqdm import tqdm


# constants
BASE_URL = "https://www.domain.com.au"
N_PAGES = 1 # update this to your liking
PROPERTY_FEATURES = {"Bed", "Bath", "Park"}
HA_TO_SQM = 10000
ACRES_TO_SQM = 4046.8564
EMPTY_FIELD = "Not Listed"

DEBUG = 0

# NOTE: IT'S LITERALLY GOING TO TAKE A REEEEEEAAAAALLLLYYY LONG TIME TO RUN THIS CODE. 
# Especially if there are many number of pages. BE PATIENT.

# begin code
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
url_links = set()
property_metadata = defaultdict(dict)

# NOTE: run search_suburbs.py before running this script
suburbs = pd.read_csv("../data/raw/suburb_urls.csv")

suburbs = suburbs["suburb_url"].tolist()


print("Start Collection of URLs")
for i in tqdm(range(len(suburbs))):
	suburb = suburbs[i]
	# generate list of urls to visit
	for page in range(1, N_PAGES+1):
		url = suburb + f"&page={page}"
		bs_object = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")

		if DEBUG: print(page)

		# find the unordered list (ul) elements which are the results, then
		# find all href (a) tags that are from the base_url website.
		try: 
			index_links = bs_object \
				.find(
					"ul",
					{"data-testid": "results"}
				) \
				.findAll(
					"a",
					href=re.compile(f"{BASE_URL}/*") # the `*` denotes wildcard any
					# TODO: cn theoretically vastly improve speed by checking if suburb keywords are in the link
				)

			for link in index_links:
				# if its a property address, add it to the list
				if 'address' in link['class']:
					link_found = link['href']
					#if suburb in re.sub(" ", "-", link_found).lower():
					#	if DEBUG: print(link_found)
					url_links.add(link['href'])
					
			
			
		except: 
			# This occurs if there is only m < N_pages of results for a certain suburb
			if DEBUG: print(suburb)
			break
			
url_links = list(url_links)
# output to urls json in data/raw/
with open('../data/raw/urls.json', 'w') as f:
	dump(property_metadata, f)
	
# for each url, scrape some basic metadata
count = 1
print("Begin Property Scraping")
for i in tqdm(range(len(url_links))):
	property_url = url_links[i]
	if DEBUG: print(f"scraping property #{count}")
	count += 1

	bs_object = BeautifulSoup(requests.get(property_url, headers=headers).text, "html.parser")

	### looks for the header class to get property name
	property_metadata[property_url]['name'] = bs_object \
		.find("h1", {"class": "css-164r41r"}) \
		.text


	### looks for the div containing a summary title for cost
	property_metadata[property_url]['cost_text'] = bs_object \
		.find("div", {"data-testid": "listing-details__summary-title"}) \
		.text
	# note that this method grabs texts like "contact agent" as well. Need to preprocess it. TODO

	
	### extract coordinates from the hyperlink provided
	# the link in bs_object takes you to the location of the property in gmaps.
	property_metadata[property_url]['coordinates'] = [
		float(coord) for coord in re.findall(
			r'destination=([-\s,\d\.]+)', # the location coordinate written in the gmaps link
			bs_object \
				.find(
					"a",
					{"target": "_blank", 'rel': "noopener noreferer"}
				) \
				.attrs['href']
		)[0].split(',')
	]

	
	### extract the number of beds, baths and parking spaces from the features displayed on website
	feature_data = bs_object \
		.find_all("span", class_= "css-lvv8is")
	
	# for each of the divs we have found
	for fd in feature_data:
		# check which feature it matches (this avoids typos)
		for feature in PROPERTY_FEATURES: 
			if feature in fd.text[1:]:
				# assign the values; '-' replaced with 0.
				property_metadata[property_url][feature] =	fd.text[0] if fd.text[0].isnumeric() else 0

				
	### extract property type
	p_type = bs_object \
		.find("div", {"data-testid":"listing-summary-property-type"}).text
	property_metadata[property_url]["property_type"] = p_type if p_type is not [] else EMPTY_FIELD
	
	### extract property description head
	try:
		p_desc_head = bs_object.find("h4", {"data-testid": "listing-details__description-headline"}).text
	except AttributeError:
		p_desc_head = EMPTY_FIELD
	property_metadata[property_url]["desc_head"] = p_desc_head
	
	### TODO: from the desc_head, extract the number of stories
	
	### extract property description
	property_metadata[property_url]['desc'] = re \
		.sub(r'<br\/>', '\n', str(bs_object.find("p"))) \
		.strip('</p>')


	### extract additional property features other than bed, bath park, for example, 
	# whether a property has aircon, heating, balcony, etc.
	p_features = []
	soup = bs_object \
		.findAll("li", {"data-testid": "listing-details__additional-features-listing"})
	
	# some will result in an empty list, some will have additional property features listed.
	for i in soup:
		p_features.append(i.text)

	property_metadata[property_url]["additional features"] = p_features if p_features is not [] else EMPTY_FIELD
	
	
	### extract area
	# Part 1: extract from given area summary info
	found_area = []
	
	if (found_area == []):
		if DEBUG: print(property_url)
		try: 
			p_area = bs_object \
			.find(
				"ul",
				{"data-testid": "listing-summary-strip"}
			) \
			.find_all(
				"li"
			)
			
			for elem in p_area:
				temp = str(elem).lower()
				# generate internal area where possible, using https://www.domain.com.au/110-webb-road-bonshaw-vic-3352-16070196
				# as example
				if "internal area" in (temp):
					property_metadata[property_url]['internal_area_sqkm'] = re.findall('\d+', temp)
				
				# can we get the land area as well?
				if "land area" in (temp):
					found_area = re.findall('\d+', temp)
					
			# Lets check the description for area information
			if (found_area == []):
				# is the area in sq metres? 
				found_area = re.findall('(\d+(?=\w?sqm))|(\d+(?=\w?m<sup>))', property_metadata[property_url]['desc'] + 
																			property_metadata[property_url]["desc_head"])
																			
				if (found_area == []):
					# is the found area in hectares?
					found_area = re.findall('(\d+(?=\w?Hectares))|(\d+(?=\w?ha))', property_metadata[property_url]['desc'] + 
																					property_metadata[property_url]["desc_head"])
					if found_area: found_area = float(found_area[0])*HA_TO_SQM
					
				if (found_area == []):
					# is the found area in acres?
					found_area = re.findall('\d+(?=\w?acres)', property_metadata[property_url]['desc'] + 
																property_metadata[property_url]["desc_head"])
					if found_area: found_area = float(found_area[0])*ACRES_TO_SQM_TO_SQM
				
			# if the property type is flat or apartment, internal area may be incorrectly listed as land area.
			# eg: https://www.domain.com.au/2614-350-william-street-melbourne-vic-3000-16070171
			
			if "apartment" in property_metadata[property_url]["property_type"].lower():
				# todo p_type if p_type is not [] else EMPTY_FIELD
				property_metadata[property_url]['internal_area_sqkm'] = found_area if found_area is not [] else EMPTY_FIELD
			else:
				property_metadata[property_url]['land_area_sqkm'] = found_area if found_area is not [] else EMPTY_FIELD
			if DEBUG: print("\nfound area", found_area, "\n")
			
		except AttributeError:
			# occurs if there is no area summary attribute. This is fine, it just means we skip this.
			pass
		
	property_metadata[property_url]['land_area_sqkm'] = found_area if found_area is not [] else EMPTY_FIELD
	
	


# output to example json in data/raw/
with open('../data/raw/example.json', 'w') as f:
	dump(property_metadata, f)
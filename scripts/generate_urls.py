"""
A very simple and basic	web	scraping script. Feel free to
use	this as	a source of	inspiration, but, make sure	to attribute
it if you do so.

This is	by no means	production code.
"""
# built-in imports
import re
from json import dump
from collections import	defaultdict
import pandas as pd

# user packages
from bs4 import	BeautifulSoup
from urllib.request	import urlopen
import requests

# for testing purposes
from tqdm import tqdm


# constants
BASE_URL = "https://www.domain.com.au"
N_PAGES	= 50 # update this to your liking
EMPTY_FIELD	= "Not Listed"

DEBUG =	0

# NOTE:	IT'S LITERALLY GOING TO	TAKE A REEEEEEAAAAALLLLYYY LONG	TIME TO	RUN	THIS CODE. 
# Especially if	there are many number of pages.	BE PATIENT.

# begin	code
headers	= {"User-Agent": "Mozilla/5.0 (X11;	CrOS x86_64	12871.102.0) AppleWebKit/537.36	(KHTML,	like Gecko)	Chrome/81.0.4044.141 Safari/537.36"}
url_links =	set()
property_metadata =	defaultdict(dict)

# NOTE:	run	search_suburbs.py before running this script
suburbs	= pd.read_csv("../data/raw/suburb_urls.csv")

suburbs	= suburbs["suburb_url"].tolist()


print("Start Collection of URLs")
for	i in tqdm(range(len(suburbs))):
	suburb	= suburbs[i]
	# generate	list of	urls to	visit
	for page in range(1, N_PAGES+1):
		url =	suburb + f"&page={page}"
		bs_object	= BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")

		if DEBUG:	print(page)

		#	find the unordered list	(ul) elements which	are	the	results, then
		#	find all href (a) tags that	are	from the base_url website.
		try: 
			index_links = bs_object \
				.find(
					"ul",
					{"data-testid": "results"}
				) \
				.findAll(
					"a",
					href=re.compile(f"{BASE_URL}/*") #	the	`*`	denotes	wildcard any
				)

			for link	in index_links:
				# if its a property	address, add it	to the list
				if 'address' in	link['class']:
					url_links.add(link['href'])
					
			
			
		except: 
			# This occurs if	there is only m	< N_pages of results for a certain suburb
			if DEBUG: print(suburb)
			break
			
url_links =	list(url_links)

# output to	urls in data/raw/
df = pd.DataFrame({"url": url_links})
df.to_csv("../data/raw/url_links.csv", index=False)
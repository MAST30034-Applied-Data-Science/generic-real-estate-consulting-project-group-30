# Generic Real Estate Consulting Project

## Research Goal
The research goal of this project is to inspect rent growth prices for various Victorian suburbs and predict areas that will have the greatest growth within the coming years. External factors such as crime, population, income and public transport have been taken into account. 

## Timeline
The timeline for the property data is from the year 2022, taken from the month of September. The rest of the data is taken from the year 2021. 

## Pipeline
To run the pipeline, please download the dependencies in requirements.txt. Please note that the chrome browser is required for the program to run. 
Then, please visit the `scripts` and `notebooks directory` and run the files in order:
1. `suburb.py`: This scrapes all the 307 SA2 level suburbs and saves it in the `data\raw` directory
2. `search_suburbs.py`: This script uses domain.com.au's autocomplete feature to get the URLs for Victoria's suburbs and saves it to `data\raw`
3. `generate_urls.py`: This script generates all the property URLs by suburb
3. `scrape.py`: This script scrapes properties, saving them to the `data\raw` directory
4. `download_census.py`: This script downloads census data from Australian Bureau of Statistics(ABS) abs.gov.au for 2011,2016,2021, saving them to the `data\raw` directory
5. `download_crime.ipynb`: This script downloads crime data, saving them to the `data\raw` directory


## Group Members 
Andrew Dharmaputra, 1213935

Arshia Azarhoush, 1175924

Ayesha Tabassum, 1166531

Shah Sarwesvaran, 1063490

Sureen Tiwana, 912147



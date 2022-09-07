# Generic Real Estate Consulting Project
Groups should generate their own suitable `README.md`.

## Research Goal
The research goal of this project is to inspect rent growth prices for various Victorian suburbs (SA2) and predict areas that will have the greatest growth within the coming years. Factors such as crime, population, income, distance to schools and public transport will be considered. 

## Timeline
The timeline for the property data is from the 2022 year, taken from the month of sept. The rest of the data is taken from the 2021 year. 

## Pipeline
To run the pipeline, please download the dependencies in requirements.txt. Please note that the chrome browser is required for the program to run. 
Then, please visit the `scripts` and `notebooks directory` and run the files in order:
1. `suburb.py`: This scrapes all the 307 SA2 level suburbs and saves it in the `data\raw` directory
2. `search_suburbs.py`: This script uses domain.com.au's autocomplete feature to get the URLs for Victoria's suburbs and saves it to `data\raw`
3. `scrape.py`: This script generates every page with houses for each suburb, and then scrapes properties, saving them to the `data\raw` directory


## Group Members 
Andrew Dharmaputra, 1213935

Sureen Tiwana, 912147

Ayesha Tabassum, 1166531

Shah Sarwesvaran, 1063490

Arshia Azarhoush, 1175924


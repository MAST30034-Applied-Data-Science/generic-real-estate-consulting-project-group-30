# Generic Real Estate Consulting Project

## Research Goal
The research goal of this project is to inspect rent growth prices for various Victorian suburbs and predict areas that will have the greatest growth within the coming years. External factors such as crime, population, income and public transport have been taken into account. 

## Timeline
The timeline for the property data is from the year 2022, taken from the month of September. The rest of the external data is taken from the years of 2021, 2016 and 2011. 

## Pipeline
To run the pipeline, please download the dependencies in requirements.txt. Please note that the chrome browser is required for the program to run. 
Then, please visit the `scripts` directory and run the files in order:
(Please note that only step 1. `shapefiles.py` needs to be run since the shapefiles were too large to upload. The raw data for steps 2-7 have already been uploaded but may be run again if required.)
1. `shapefiles.py`: This script downloads the Australian SA2 shapefiles from the Australian Bureau of Statistics(ABS), and saves them to the `data\raw\shapefiles` directory.
2. `suburb.py`: This scrapes all the 307 SA2 level suburbs and saves it in the `data\raw` directory
3. `search_suburbs.py`: This script uses domain.com.au's autocomplete feature to get the URLs for Victoria's suburbs and saves it to `data\raw`
4. `generate_urls.py`: This script generates all the property URLs by suburb
5. `scrape.py`: This script scrapes properties, saving them to the `data\raw` directory
6. `download_census.py`: This script downloads census data from the Australian Bureau of Statistics(ABS) abs.gov.au for 2011,2016,2021, saving them to the `data\raw` directory. <br/>
Please visit the notebook directory at this time.
7. `download_crime.ipynb`: This notebook downloads crime data, saving them to the `data\raw` directory

Then, please visit the `notebooks` directory and run these files in order:
1. external data preprocessing: <br/>
`preprocessing_crime.ipynb`<br/>
`income_&_population_2021.ipynb`<br/>
`income_&_population_2011_2016.ipynb`<br/>
`routing_assignments.ipynb`<br/>
`shapefiles_visualisation.ipynb`<br/>


2. property data preprocessing:<br/>
`preprocess_property.ipynb`<br/>
`assign_suburbs.ipynb`<br/>
`visualisation_housing.ipynb`<br/>

3. joining datasets:<br/>
`join_datasets.ipynb`<br/>
`join_isochrones_and_crime_data.ipynb`<br/>

4. analysis and modelling:<br/>
`feature_analysis.ipynb`<br/>
`linear_model.ipynb`<br/>
`liveability_ranking.ipynb`<br/>
`neural_network_model.ipynb`<br/>
`xgboost_model.ipynb`<br/>

5. summary:<br/>
`summary.ipynb`<br/>


## Group Members 
Andrew Dharmaputra, 1213935

Arshia Azarhoush, 1175924

Ayesha Tabassum, 1166531

Sophie Sarwesvaran, 1063490

Sureen Tiwana, 912147




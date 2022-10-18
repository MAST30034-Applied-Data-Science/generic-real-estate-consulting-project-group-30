import zipfile, urllib.request, shutil
import contextlib
import os

url  = 'https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/SA2_2021_AUST_SHP_GDA2020.zip'



# download zip file
print("starting download")
file_name = 'SA2_2021_AUST_SHP_GDA2020.zip'

with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
    shutil.copyfileobj(response, out_file)
    with zipfile.ZipFile(file_name) as zf:
        zf.extractall('./data/raw/shapefiles/Statistical_area_level2')

# remove zip file from main directory
with contextlib.suppress(FileNotFoundError):
    os.remove(file_name)

print('download complete')
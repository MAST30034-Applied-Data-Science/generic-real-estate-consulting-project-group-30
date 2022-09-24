import requests
import zipfile
from io import BytesIO
import shutil

URL  = "http://abs.gov.au/census/find-census-data/datapacks/download/2021_GCP_SA2_for_VIC_short-header.zip"

output_dir = "../data/raw/"

# download zip file
print("starting download")
req = requests.get(URL)
filename = URL.split('/')[-1]

zipfile = zipfile.ZipFile(BytesIO(req.content))
zipfile.extractall(f"{output_dir}{filename}")
print("download complete")

# delete unneeccessary files
# i still don't know how to spell "uncesecsary" properly, please forgive me
file_dir = f"{output_dir}{filename}/2021 Census GCP Statistical Area 2 for VIC/"
shutil.move(f"{file_dir}2021Census_G02_VIC_SA2.csv", f"{output_dir}2021Census_G02_VIC_SA2.csv")
shutil.move(f"{file_dir}2021Census_G17A_VIC_SA2.csv", f"{output_dir}2021Census_G17A_VIC_SA2.csv")
shutil.move(f"{file_dir}2021Census_G17B_VIC_SA2.csv", f"{output_dir}2021Census_G17B_VIC_SA2.csv")
shutil.rmtree(f"{output_dir}{filename}")
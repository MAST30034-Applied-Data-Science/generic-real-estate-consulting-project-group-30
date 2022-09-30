# note: year needs to be 2021, 2016, or 2011, any other value'd be invalid since the census doesn't exist every year
def download_census(year):
    import requests
    import zipfile
    from io import BytesIO
    import shutil

    if year == 2011:
        # 2011 had BCP, not GCP
        URL  = f"http://abs.gov.au/census/find-census-data/datapacks/download/{year}_BCP_SA2_for_VIC_short-header.zip"
    else:
        URL  = f"http://abs.gov.au/census/find-census-data/datapacks/download/{year}_GCP_SA2_for_VIC_short-header.zip"

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
    if year == 2011:
        file_dir = f"{output_dir}{filename}/{year} Census BCP Statistical Areas Level 2 for VIC/VIC/"
        shutil.move(f"{file_dir}{year}Census_B02_VIC_SA2_short.csv", f"{output_dir}{year}Census_B02_VIC_SA2_short.csv")
        shutil.move(f"{file_dir}{year}Census_B17A_VIC_SA2_short.csv", f"{output_dir}{year}Census_B17A_VIC_SA2_short.csv")
        shutil.move(f"{file_dir}{year}Census_B17B_VIC_SA2_short.csv", f"{output_dir}{year}Census_B17B_VIC_SA2_short.csv")
        shutil.rmtree(f"{output_dir}{filename}")
    else:
        file_dir = f"{output_dir}{filename}/{year} Census GCP Statistical Area 2 for VIC/"
        shutil.move(f"{file_dir}{year}Census_G02_VIC_SA2.csv", f"{output_dir}{year}Census_G02_VIC_SA2.csv")
        shutil.move(f"{file_dir}{year}Census_G17A_VIC_SA2.csv", f"{output_dir}{year}Census_G17A_VIC_SA2.csv")
        shutil.move(f"{file_dir}{year}Census_G17B_VIC_SA2.csv", f"{output_dir}{year}Census_G17B_VIC_SA2.csv")
        shutil.rmtree(f"{output_dir}{filename}")

download_census(2011)
download_census(2016)
download_census(2021)
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
 

# Function to download the csv file of the road traffic in Rennes
def get_csv_file(url_page):
    """
    Function to download the csv file of the road traffic in Rennes
    """
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    # Get the html page
    try:
        response = requests.get(url_page, headers=headers)
        if response.status_code == 200:
            print(f"✅ OK: {url_page}")
        else:
            print("❌ invalid url")
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        soup = BeautifulSoup(response.text, "html.parser")
        link_tag = soup.find("a", href=lambda href: href and "TP_FCD_AT.csv" in href)
        print("✅ HTML page downloaded successfully")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Find the CSV link
    if link_tag:
        csv_url = link_tag["href"]
        print(f"CSV link found : {csv_url}")

        # Download the csv file
        csv_response = requests.get(csv_url)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"C:/Users/henin/OneDrive/Documents/Coding/My Portfolio/Projects/project4/data/raw_data/Rennes_road_traffic{timestamp}.csv"
        with open(filename, "wb") as f:
            f.write(csv_response.content)
        print("✅ File succesfully download")
    else:
        print("❌ CSV link not found")

    return csv_url


get_csv_file(url_page="https://dkan.autoroutes-trafic.fr/?q=dataset/donn%C3%A9es-trafic-rennes-m%C3%A9tropole")

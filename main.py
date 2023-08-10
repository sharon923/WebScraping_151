import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://www.flipkart.com/search?q=fridge&sid=j9e%2Cabm%2Chzg&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&as-pos=1&as-type=RECENT&suggestionId=fridge%7CRefrigerators&requestId=ef4b9ec0-f7fd-4725-883a-d265c7d5f5c1&as-searchtext=fri"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}

max_retries = 5
retry_delay = 5  # seconds

phone_data = []
for retry in range(max_retries):
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        break  # Exit the loop if the request is successful
    except requests.RequestException as e:
        print(f"Request error (Retry {retry + 1}/{max_retries}):", e)
        if retry < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print("Max retries reached. Exiting.")
            exit()

soup = BeautifulSoup(response.content, "html.parser")
fridge_cards = soup.find_all("div", class_="_1AtVbE")

for fridge_card in fridge_cards:
    try:
        fridge_name = fridge_card.find("div", class_="_4rR01T").text
        fridge_price = fridge_card.find("div", class_="_30jeq3").text if fridge_card.find("div",
                                                                                       class_="_30jeq3") else "N/A"
        fridge_rating = fridge_card.find("div", class_="_3LWZlK").text if fridge_card.find("div",
                                                                                        class_="_3LWZlK") else "N/A"

        phone_data.append({
            "Name": fridge_name,
            "Price": fridge_price,
            "Rating": fridge_rating
        })
    except Exception as e:
        print("Error in extracting phone data:", e)

df = pd.DataFrame(phone_data)
df.to_csv("frige.csv", index=False)

print("Data successfully extracted and CSV saved.")
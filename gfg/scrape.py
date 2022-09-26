from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import localtime, strftime
import re
import os
from selenium import webdriver
import re
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def send_request(name, low, high, sort):

    sort_number = 1

    if sort.lower() == "high to low":
        sort_number = 3
    if sort.lower() == "recent":
        sort_number = 2
    if sort.lower() == "low to high":
        sort_number = 4
    else:
        sort_number = 1

    name_list = []
    name_search = ""
    name_list = name.split()
    for i in name_list:
        name_search = name_search + i + "%20"

    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(
        "https://www.carousell.sg/search/{}?price_start={}&price_end={}&sort_by={}".format(
            name_search,
            low,
            high,
            sort_number,
        )
    )

    more_buttons = driver.find_elements(
        by=By.XPATH,
        value="/html/body/div[1]/div/div/main/div[1]/div/section/div[5]/div/div/div[2]/div/button",
    )
    driver.execute_script("arguments[0].click", more_buttons)

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, "lxml")
    body = soup.find("body")
    main = body.find("main", class_=re.compile("D_"))

    div = main.find_all("div", {"class": "D_SG"})  # Regex ^D_[A-z][A-z]$
    details = main.find_all("a", {"class": "D_jP"})  # Regex ^D_j[A-Z]$

    dataset = []

    for i in range(0, len(div)):
        dataset.append(div[i]["data-testid"])

    df_file = pd

    details_odd = details[1::2]
    details_even = details[0::2]

    # product details
    seller_name = ""
    posted_on = ""

    seller_name = details_odd

    price_list = []
    info_list = []

    # splitting of string to extract price and infor respectively
    for i in range(0, len(details_odd)):
        price_list.append(re.findall("S\$[0-9][0-9][0-9]", details_odd[i].text))

        if re.search("S\$[0-9][0-9][0-9]", details_odd[i].text):
            info_list.append(re.split("S\$[0-9][0-9][0-9]", details_odd[i].text))

    # Empty value removal
    price_list = list(filter(lambda x: x, price_list))

    df_scraped = pd.DataFrame(
        {"listing-id": dataset, "Price": price_list, "Product-info": info_list}
    )

    # Getting the list ID's
    try:
        df_file = pd.read_csv(os.path.dirname(__file__) + "/watch_id.csv")
        for index, i in df_scraped.iterrows():
            for index, j in df_file.iterrows():
                if j["listing-id"] == i["listing-id"]:
                    delete_row = df_scraped[
                        df_scraped["listing-id"] == i["listing-id"]
                    ].index
                    df_scraped.drop(delete_row, inplace=True)

        df_scraped.to_csv(
            os.path.dirname(__file__) + "/watch_id.csv", mode="a", index=False
        )

    except FileNotFoundError as err:
        if len(str(err)) != 0:
            df_scraped.to_csv(os.path.dirname(__file__) + "/watch_id.csv", index=False)

    # Alert on telegram about the new listing
    for index, i in df_scraped.iterrows():
        bot(
            str(strftime("%Y-%m-%d %H:%M:%S", localtime()))
            + "\n🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥"
            + "\nThe product info is "
            + str(i["Product-info"])
            + " and the price is: "
            + str(i["Price"])
            + "\n🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥"
        )


def bot(message):
    token = "5790580647:AAG6kRahTPN9cUlQUhTakfy5PaptF8EhsGk"
    chat_id = "1104013374"
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)

import requests
import json
import csv
import pandas as pd
from bs4 import BeautifulSoup

def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    trs = soup.find_all("tr")
    weekday, service, hour = [], [], []
    for data in trs:
        sub_tr = data.text.split()
        weekday.append(sub_tr[0])
        service.append("".join(sub_tr[1:3]))
        hour.append("".join(sub_tr[3:4]))
    _data = pd.DataFrame()
    _data["dates"] = weekday
    _data["service"] = service
    _data["hours"] = hour
    return _data

data_hssl = get_data("https://www.mcgill.ca/library/branches/hssl")

data_hssl.to_csv("open.csv", index=False)
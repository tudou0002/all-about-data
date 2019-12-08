import requests
import json
import csv
import pandas as pd
from bs4 import BeautifulSoup

'''
r = requests.get("https://www.mcgill.ca/library/branches/law")
html = r.text
table_bf = BeautifulSoup(html, features="lxml")
table = table_bf.find_all('table', class_ = 'no-zebra')
'''
# check the url
def check_link(url):
    try:
        r = requests.get(url)
        return r.text
    except:
        print("Can't connect to the server")

# start scarpping
def get_contents(ulist, rurl):
    soup = BeautifulSoup(rurl, features='lxml')
    tables = soup.find_all("table", attrs={'no-zebra'})
    weekday, service, hour = [], [], []
    for tb in tables:
        sub_tr = tb.text.split()
        weekday.append(sub_tr[0])
        ulist.append(tb)

# write the content to a csv file
def save_contents(urlist, branch):
    with open("C:/Users/lifre/all-about-data/crawlers/opening_hours.csv",'a') as f:
        writer = csv.writer(f)
        writer.writerow(branch) 
        writer.writerow(urlist)
        
        for i in range(len(urlist)):
            writer.writerow([urlist][i][0][1])
        
def main():
    urli = []
    libraries = ['/hssl','/law','/music']
    url = "https://www.mcgill.ca/library/branches"
    for l in libraries:
        rs = check_link(url+l)
        get_contents(urli,rs)
        save_contents(urli, l)
        print(len(urli))

main()

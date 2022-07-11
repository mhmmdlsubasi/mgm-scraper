import requests
import pandas as pd
from datetime import datetime
import time

def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

mgm_url = "https://www.mgm.gov.tr/"
iller = "https://servis.mgm.gov.tr/web/merkezler/iller"
forecast_url = "https://servis.mgm.gov.tr/web/tahminler/gunluk?"
instant_url = "https://servis.mgm.gov.tr/web/sondurumlar?"

def data():
    data_requests = requests.get(f"{iller}", headers={"Origin":f"{mgm_url}"}).json()
    if data_requests:
        dict1 = {}
        for i in range(0,81):
            keys = data_requests[i]["il"]
            values = data_requests[i]["sondurumIstNo"]
            dict1.setdefault(keys,values)
    else:
        print("data_requests failed")
    return dict1
def instant_data():
    last_check = instant_data_requests[0]["veriZamani"]
    sicaklik = instant_data_requests[0]["sicaklik"]
    yagis = instant_data_requests[0]["yagis00Now"]
    nem = instant_data_requests[0]["nem"]
    ruzgarhiz = instant_data_requests[0]["ruzgarHiz"]
    return [last_check,sicaklik,yagis,nem,ruzgarhiz]

dict1=data()

location = {
    "Sinop":"",
    "Samsun":"",
    "Amasya":"",
    "Ordu":""
}
last_check = location

while True:
    for city in location.keys():

        params = {"istno":dict1[city]}
        instant_data_requests = requests.get(f"{instant_url}", params=params, headers={"Origin":f"{mgm_url}"}).json()
        if instant_data_requests:
            a=instant_data()

            if a[0] != last_check[city]:

                last_check[city] = a[0]

                timer = str(datetime_from_utc_to_local(datetime.strptime(last_check[city],"%Y-%m-%dT%H:%M:%S.%fZ")))
                date = timer.split()[0]
                clock = timer.split()[1]
                
                f = open(f"{city}_log.csv","a")
                f.write(f"{date},{clock},{a[1]},{a[2]},{a[3]},{a[4]} \n")
                f.close()

                print(f"instant data requests successful for {city} \n {timer}")
        else:
            print("instant_data_requests failed")

import requests
import pandas as pd

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

location = {
    "Sinop":"",
    "Samsun":"",
    "Amasya":"",
    "Ordu":""
}
dict1=data()
last_check={"Sinop":"",
    "Samsun":"",
    "Amasya":"",
    "Ordu":""}

def instant_data():
    last_check = instant_data_requests[0]["veriZamani"]
    sicaklik = instant_data_requests[0]["sicaklik"]
    yagis = instant_data_requests[0]["yagis00Now"]
    nem = instant_data_requests[0]["nem"]
    ruzgarhiz = instant_data_requests[0]["ruzgarHiz"]
    return [last_check,sicaklik,yagis,nem,ruzgarhiz]
 
while True:
    for city, veri in location.items():

        params = {"istno":dict1[city]}
        instant_data_requests = requests.get(f"{instant_url}", params=params, headers={"Origin":f"{mgm_url}"}).json()
        if instant_data_requests:
            a=instant_data()

            if a[0] != last_check[city]:

                last_check[city] = a[0]

                f = open(f"{city}_log.csv","a")
                f.write(f"{a[1]},{a[2]},{a[3]},{a[4]} \n")
                f.close()
            else:
                print("no update received")
                print(f"last check date: {last_check}")
                print("-"*200)
        else:
            print("instant_data_requests failed")
            


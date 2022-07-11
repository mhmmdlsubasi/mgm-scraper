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

def instant_data(last_check=None,dict1=data()):
    while True:
        for city, veri in location.items():
            params = {"istno":dict1[city]}
            instant_data_requests = requests.get(f"{instant_url}", params=params, headers={"Origin":f"{mgm_url}"}).json()
            if instant_data_requests:
                if last_check != instant_data_requests[0]["veriZamani"]:
                    last_check = instant_data_requests[0]["veriZamani"]

                    sicaklik = instant_data_requests[0]["sicaklik"]
                    yagis = instant_data_requests[0]["yagis00Now"]
                    nem = instant_data_requests[0]["nem"]
                    ruzgarhiz = instant_data_requests[0]["ruzgarHiz"]

                    f = open(f"{city}_log.csv","a")
                    f.write(f"{sicaklik},{yagis},{nem},{ruzgarhiz} \n")
                    f.close()
                else:
                    print("no update received")
            else:
                print("instant_data_requests failed")


instant_data()

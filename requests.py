import requests
import pandas as pd
from datetime import datetime
import time

mgm_url = "https://www.mgm.gov.tr/"
iller = "https://servis.mgm.gov.tr/web/merkezler/iller"
forecast_url = "https://servis.mgm.gov.tr/web/tahminler/gunluk?"
instant_url = "https://servis.mgm.gov.tr/web/sondurumlar?"

def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

def data():
    data_requests = requests.get(f"{iller}", headers={"Origin":f"{mgm_url}"}).json()
    if data_requests:
        dict1 = {}
        dict2 = {}
        dict3 = {}
        for i in range(0,81):
            keys = data_requests[i]["il"]
            instant_values = data_requests[i]["sondurumIstNo"]
            dict1.setdefault(keys,instant_values)
            daily_values = data_requests[i]["gunlukTahminIstNo"]
            dict2.setdefault(keys,daily_values)
            dict3.setdefault(keys,"")
    else:
        print("data_requests failed")
    return dict1,dict2,dict3

def instant_data_requests(city,instant_data_requests):
    last_check = instant_data_requests[0]["veriZamani"]
    sicaklik = instant_data_requests[0]["sicaklik"]
    yagis = instant_data_requests[0]["yagis00Now"]
    nem = instant_data_requests[0]["nem"]
    ruzgarhiz = instant_data_requests[0]["ruzgarHiz"]

    timer = str(datetime_from_utc_to_local(datetime.strptime(last_check,"%Y-%m-%dT%H:%M:%S.%fZ")))
    date = timer.split()[0]
    clock = timer.split()[1]
    return [city,last_check,timer,date,clock,sicaklik,yagis,nem,ruzgarhiz]
def forecast_data_requests(city,forecast_data_requests,i):
    
    forecast_last_check = forecast_data_requests[0][f"tarihGun{i}"]
    forecast_min_sicaklik = forecast_data_requests[0][f"enDusukGun{i}"]
    forecast_max_sicaklik = forecast_data_requests[0][f"enYuksekGun{i}"]
    forecast_min_nem = forecast_data_requests[0][f"enDusukNemGun{i}"]
    forecast_max_nem = forecast_data_requests[0][f"enYuksekNemGun{i}"]
    forecast_ruzgarhiz = forecast_data_requests[0][f"ruzgarHizGun{i}"]

    forecast_timer = str(datetime_from_utc_to_local(datetime.strptime(forecast_last_check,"%Y-%m-%dT%H:%M:%S.%fZ")))
    forecast_date = forecast_timer.split()[0]
    forecast_clock = forecast_timer.split()[1]
    return [city,forecast_last_check,forecast_timer,forecast_date,forecast_clock,forecast_min_sicaklik,forecast_max_sicaklik,forecast_min_nem,forecast_max_nem,forecast_ruzgarhiz]

city_instant_istno_dict=data()[0]
city_daily_istno_dict = data()[1]

location = data()[2]    #   Çalışma Alanı
instant_last_check = location.copy()
forecast_last_check = location.copy()

forecast_df = pd.DataFrame(columns=["İl","İstasyon Numarası","Tarih","Saat","Min. Sıcaklık (C)","Max. Sıcaklık (C)","Min. Nem (%)","Max. Nem (%)","Rüzgar Hızı (km/s)"]) 
instant_df = pd.DataFrame(columns=["İl","İstasyon Numarası","Tarih","Saat","Sıcaklık (C)","Yağış Miktarı (mm)","Nem (%)","Rüzgar Hızı (km/s)"]) 

def instant(city):
    params = {"istno":city_instant_istno_dict[city]}
    instant_data_r = requests.get(f"{instant_url}", params=params, headers={"Origin":f"{mgm_url}"}).json()
    if instant_data_r:
        instant_data=instant_data_requests(city,instant_data_r)

        if instant_data[1] != instant_last_check[city]:

            instant_last_check[city] = instant_data[1]

            instant_datas = [instant_data[0],city_instant_istno_dict[city],instant_data[3],instant_data[4],instant_data[5],instant_data[6],instant_data[7],instant_data[8]]
            instant_df.loc[len(instant_df.index)] = instant_datas
            instant_df[instant_df["İl"]==city].to_csv(f"{city}_instant_df.csv",index=False)

            print(f"instant data requests successful for {city} \n {instant_data[3]},{instant_data[4]}")
    else:
        print("instant_data_requests failed")
def forecast(city):
    params = {"istno":city_daily_istno_dict[city]}
    forecast_data_r = requests.get(f"{forecast_url}", params=params, headers={"Origin":f"{mgm_url}"}).json()
    if forecast_data_r:
        forecast_data = forecast_data_requests(city,forecast_data_r,1)

        if forecast_data[1] != forecast_last_check[city]:
                
            forecast_last_check[city] = forecast_data[1]
            for i in [1,2,3,4,5]:
                forecast_data = forecast_data_requests(city,forecast_data_r,i)
                forecasts = [forecast_data[0],city_instant_istno_dict[city],forecast_data[3],forecast_data[4],forecast_data[5],forecast_data[6],forecast_data[7],forecast_data[8],forecast_data[9]]
                forecast_df.loc[len(forecast_df.index)] = forecasts
                forecast_df[forecast_df["İl"]==city].to_csv(f"{city}_forecast_df.csv",index=False)

            print(f"forecast data requests successful for {city} \n {forecast_data[3]},{forecast_data[4]}")
    else:
        print("forecast_data_requests failed")

while True:
    for city in location.keys():
        instant(city)
        forecast(city)

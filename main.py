import requests
import pandas as pd
from datetime import datetime
import time

def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

def data():
    data_requests = requests.get(f"{iller}", headers={"Origin":f"{mgm_url}"}).json()
    if data_requests:
        dict0 = {}
        dict1 = {}
        dict2 = {}
        dict3 = {}
        for i in range(0,81):
            keys = data_requests[i]["il"]
            dict0.setdefault(keys,"")

            instant_values = data_requests[i]["sondurumIstNo"]
            dict1.setdefault(keys,instant_values)

            daily_values = data_requests[i]["gunlukTahminIstNo"]
            dict2.setdefault(keys,daily_values)

            hourly_values = data_requests[i]["saatlikTahminIstNo"]
            dict3.setdefault(keys,hourly_values)
    else:
        print("data_requests failed")
    return dict0,dict1,dict2,dict3

def instant(city):
    params = {"istno":city_instant_istno_dict[city]}
    instant_data_r = requests.get(f"{instant_url}", params=params, headers={"Origin":f"{mgm_url}"}).json()
    if instant_data_r:
        instant_data=instant_data_requests(city,instant_data_r)

        if instant_data[1] != instant_last_check[city]:

            instant_last_check[city] = instant_data[1]

            instant_datas = [instant_data[0],city_instant_istno_dict[city],instant_data[3],instant_data[4],instant_data[5],instant_data[6],instant_data[7],instant_data[8]]
            instant_df.loc[len(instant_df.index)] = instant_datas

            print(f"instant data requests successful for {city} \n {instant_data[3]},{instant_data[4]}")
    else:
        print("instant_data_requests failed")
def instant_data_requests(city,instant_data_requests):
    last_check = instant_data_requests[0]["veriZamani"]
    sicaklik = instant_data_requests[0]["sicaklik"]
    yagis = instant_data_requests[0]["yagis00Now"]
    nem = instant_data_requests[0]["nem"]
    ruzgarhiz = instant_data_requests[0]["ruzgarHiz"]

    timer = str(datetime_from_utc_to_local(datetime.strptime(last_check,"%Y-%m-%dT%H:%M:%S.%fZ")))
    date = timer.split()[0]
    clock = timer.split()[1]
    return [
        city,
        last_check,
        timer,date,
        clock,
        sicaklik,
        yagis,
        nem,
        ruzgarhiz
        ]

def daily_forecast(city):
    params = {"istno":city_daily_forecast_istno_dict[city]}
    daily_forecast_data_r = requests.get(f"{daily_forecast_url}", params=params, headers={"Origin":f"{mgm_url}"}).json()
    if daily_forecast_data_r:
        daily_forecast_data = daily_forecast_data_requests(city,daily_forecast_data_r,1)

        if daily_forecast_data[1] != daily_forecast_last_check[city]:
                
            daily_forecast_last_check[city] = daily_forecast_data[1]
            for i in [1,2,3,4,5]:
                daily_forecast_data = daily_forecast_data_requests(city,daily_forecast_data_r,i)
                daily_forecasts = [
                    daily_forecast_data[0],
                    city_instant_istno_dict[city],
                    daily_forecast_data[3],
                    daily_forecast_data[4],
                    daily_forecast_data[5],
                    daily_forecast_data[6],
                    daily_forecast_data[7],
                    daily_forecast_data[8],
                    daily_forecast_data[9]
                    ]
                daily_forecast_df.loc[len(daily_forecast_df.index)] = daily_forecasts

            print(f"daily forecast data requests successful for {city} \n {daily_forecast_data[3]},{daily_forecast_data[4]}")
    else:
        print("daily forecast data requests failed")
def daily_forecast_data_requests(city,daily_forecast_data_requests,i):
    
    daily_forecast_last_check = daily_forecast_data_requests[0][f"tarihGun{i}"]
    daily_forecast_min_sicaklik = daily_forecast_data_requests[0][f"enDusukGun{i}"]
    daily_forecast_max_sicaklik = daily_forecast_data_requests[0][f"enYuksekGun{i}"]
    daily_forecast_min_nem = daily_forecast_data_requests[0][f"enDusukNemGun{i}"]
    daily_forecast_max_nem = daily_forecast_data_requests[0][f"enYuksekNemGun{i}"]
    daily_forecast_ruzgarhiz = daily_forecast_data_requests[0][f"ruzgarHizGun{i}"]

    daily_forecast_timer = str(datetime_from_utc_to_local(datetime.strptime(daily_forecast_last_check,"%Y-%m-%dT%H:%M:%S.%fZ")))
    daily_forecast_date = daily_forecast_timer.split()[0]
    daily_forecast_clock = daily_forecast_timer.split()[1]
    return [
        city,
        daily_forecast_last_check,
        daily_forecast_timer,
        daily_forecast_date,
        daily_forecast_clock,
        daily_forecast_min_sicaklik,
        daily_forecast_max_sicaklik,
        daily_forecast_min_nem,
        daily_forecast_max_nem,
        daily_forecast_ruzgarhiz
        ]

def hourly_forecast(city):
    params = {"istno":city_hourly_forecast_istno_dict[city]}
    hourly_forecast_data_r = requests.get(f"{hourly_forecast_url}", params=params, headers={"Origin":f"{mgm_url}"}).json()
    if hourly_forecast_data_r:
        hourly_forecast_data = hourly_forecast_data_requests(city,hourly_forecast_data_r,1)

        if hourly_forecast_data[1] != hourly_forecast_last_check[city]:
                
            hourly_forecast_last_check[city] = hourly_forecast_data[1]
            for i in range(0,len(hourly_forecast_data_r[0]["tahmin"])+1):
                hourly_forecast_data = hourly_forecast_data_requests(city,hourly_forecast_data_r,i)
                hourly_forecasts = [
                    hourly_forecast_data[0],
                    city_hourly_forecast_istno_dict[city],
                    hourly_forecast_data[3],
                    hourly_forecast_data[8],
                    hourly_forecast_data[9],
                    hourly_forecast_data[10],
                    hourly_forecast_data[11],
                    hourly_forecast_data[12],
                    hourly_forecast_data[13],
                    hourly_forecast_data[14],
                    hourly_forecast_data[15]
                    ]
                hourly_forecast_df.loc[len(hourly_forecast_df.index)] = hourly_forecasts
                
            print(f"hourly forecast data requests successful for {city} \n {hourly_forecast_data[3]},{hourly_forecast_data[4]}")
    else:
        print("hourly forecast data requests failed")
def hourly_forecast_data_requests(city,hourly_forecast_data_requests,i):
    
    hourly_forecast_last_check = hourly_forecast_data_requests[0]["baslangicZamani"]

    hourly_forecast_tarih = hourly_forecast_data_requests[0]["tahmin"][i]["tarih"]
    hourly_forecast_hadise = hourly_forecast_data_requests[0]["tahmin"][i]["hadise"]
    hourly_forecast_sicaklik = hourly_forecast_data_requests[0]["tahmin"][i]["sicaklik"]
    hourly_forecast_hissedilen_sicaklik = hourly_forecast_data_requests[0]["tahmin"][i]["hissedilenSicaklik"]
    hourly_forecast_nem = hourly_forecast_data_requests[0]["tahmin"][i]["nem"]
    hourly_forecast_ruzgar_yonu = hourly_forecast_data_requests[0]["tahmin"][i]["ruzgarYonu"]
    hourly_forecast_ruzgarhiz = hourly_forecast_data_requests[0]["tahmin"][i]["ruzgarHizi"]
    hourly_forecast_max_ruzgarhiz = hourly_forecast_data_requests[0]["tahmin"][i]["maksimumRuzgarHizi"]

    hourly_forecast_last_check_convert = str(datetime_from_utc_to_local(datetime.strptime(hourly_forecast_last_check,"%Y-%m-%dT%H:%M:%S.%fZ")))
    hourly_forecast_last_check_date = hourly_forecast_last_check_convert.split()[0]
    hourly_forecast_last_check_clock = hourly_forecast_last_check_convert.split()[1]

    hourly_forecast_tarih_convert = str(datetime_from_utc_to_local(datetime.strptime(hourly_forecast_tarih,"%Y-%m-%dT%H:%M:%S.%fZ")))
    hourly_forecast_tarih_date = hourly_forecast_tarih_convert.split()[0]
    hourly_forecast_tarih_clock = hourly_forecast_tarih_convert.split()[1]
    return [
        city,
        hourly_forecast_last_check,
        hourly_forecast_last_check_convert,
        hourly_forecast_last_check_date,
        hourly_forecast_last_check_clock,
        hourly_forecast_tarih,
        hourly_forecast_tarih_convert,
        hourly_forecast_tarih_date,
        hourly_forecast_tarih_clock,
        hourly_forecast_hadise,
        hourly_forecast_sicaklik,
        hourly_forecast_hissedilen_sicaklik,
        hourly_forecast_nem,
        hourly_forecast_ruzgar_yonu,
        hourly_forecast_ruzgarhiz,
        hourly_forecast_max_ruzgarhiz
        ]

    

mgm_url = "https://www.mgm.gov.tr/"
iller = "https://servis.mgm.gov.tr/web/merkezler/iller"
instant_url = "https://servis.mgm.gov.tr/web/sondurumlar?"
daily_forecast_url = "https://servis.mgm.gov.tr/web/tahminler/gunluk?"
hourly_forecast_url = "https://servis.mgm.gov.tr/web/tahminler/saatlik?"

city_instant_istno_dict=data()[1]
city_daily_forecast_istno_dict = data()[2]
city_hourly_forecast_istno_dict = data()[3]

location = data()[2]    #   Çalışma Alanı

instant_last_check = location.copy()
daily_forecast_last_check = location.copy()
hourly_forecast_last_check = location.copy()

instant_df = pd.DataFrame(
    columns=[
    "İl",
"İstasyon Numarası",
"Tarih",
"Saat",
"Sıcaklık (C)",
"Yağış Miktarı (mm)",
"Nem (%)",
"Rüzgar Hızı (km/s)"
]
) 
daily_forecast_df = pd.DataFrame(
    columns=[
        "İl",
        "İstasyon Numarası",
        "Tarih",
        "Saat",
        "Min. Sıcaklık (C)",
        "Max. Sıcaklık (C)",
        "Min. Nem (%)",
        "Max. Nem (%)",
        "Rüzgar Hızı (km/s)"
        ]
        ) 
hourly_forecast_df = pd.DataFrame(
    columns=[
        "İl",
        "İstasyon Numarası",
        "Tarih",
        "Saat",
        "Beklenen Hadise",
        "Sıcaklık (°C)",
        "Hissedilen Sıcaklık (°C)",
        "Nem (%)",
        "Rüzgar Yönü",
        "Ort. Rüzgar Hızı (km/sa)",
        "Maks. Rüzgar Hızı (km/sa)"
        ]
        )

flag = True
while True:
    if flag:
        for city in location.keys():
            instant(city)
            daily_forecast(city)
            hourly_forecast(city)
            with pd.ExcelWriter(f'{city}.xlsx') as writer:  
                instant_df[instant_df["İl"]==city].to_excel(
                    writer, 
                sheet_name='Instant',index=False
                )
                daily_forecast_df[daily_forecast_df["İl"]==city].to_excel(
                    writer, 
                sheet_name='Daily Forecast',index=False
                )
                hourly_forecast_df[hourly_forecast_df["İl"]==city].to_excel(
                    writer, 
                sheet_name='Hourly Forecast',index=False
                )

from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from datetime import datetime, timedelta
from keep_alive import keep_alive
from pytz import timezone
import pandas as pd
import requests
import os

session = requests.Session()
retry = Retry(connect=3, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

#   time converter
def datetime_from_utc_to_local(utc_datetime):
    return utc_datetime.astimezone(timezone('Turkey'))

#   istno
def data():
    data_requests = session.get(f"{iller}", headers={"Origin":f"{mgm_url}"}).json()
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

# instant
def instant(city):
    params = {"istno":city_instant_istno_dict[city]}
    instant_data_r = session.get(f"{instant_url}", params=params, headers={"Origin":f"{mgm_url}"}).json()
    if instant_data_r:
        instant_data=instant_data_requests(city,instant_data_r)
        if instant_data[0] != instant_last_check[city]:
            instant_last_check[city] = instant_data[0]
            new_row = pd.Series(instant_data[1]).to_frame().T
            new_row.to_csv(f"{path}/instant/{city}.csv", mode='a', header=False, index=False)
        return "I'm busy now. I'm saving instant data."
    else:
        print("instant_data_requests failed")
def instant_data_requests(city,instant_data_requests):
    last_check = instant_data_requests[0]["veriZamani"]
    sicaklik = instant_data_requests[0]["sicaklik"]
    hadise = instant_data_requests[0]["hadiseKodu"]
    yagis = instant_data_requests[0]["yagis00Now"]
    nem = instant_data_requests[0]["nem"]
    ruzgarYon = instant_data_requests[0]["ruzgarYon"]
    ruzgarhiz = instant_data_requests[0]["ruzgarHiz"]
    aktuelBasinc = instant_data_requests[0]["aktuelBasinc"]
    denizeIndirgenmisBasinc = instant_data_requests[0]["denizeIndirgenmisBasinc"]

    timer = datetime_from_utc_to_local(datetime.strptime(last_check,"%Y-%m-%dT%H:%M:%S.%fZ"))
    date = format(timer,"%d/%m/%Y")
    clock = format(timer,"%H:%M:%S")
    return [last_check,[
        city,
        city_instant_istno_dict[city],
        date,
        clock,
        sicaklik,
        hadise,
        yagis,
        nem,
        ruzgarYon,
        ruzgarhiz,
        aktuelBasinc,
        denizeIndirgenmisBasinc
        ]]

#   hourly forecast
def hourly_forecast(city):
    params = {"istno":city_hourly_forecast_istno_dict[city]}
    hourly_forecast_data_r = session.get(f"{hourly_forecast_url}", params=params, headers={"Origin":f"{mgm_url}"}).json()
    if hourly_forecast_data_r:
        hourly_forecast_data = hourly_forecast_data_requests(city,hourly_forecast_data_r,1)

        if hourly_forecast_data[0] != hourly_forecast_last_check[city]:
                
            hourly_forecast_last_check[city] = hourly_forecast_data[0]
            for i in range(0,len(hourly_forecast_data_r[0]["tahmin"])):
                hourly_forecast_data = hourly_forecast_data_requests(city,hourly_forecast_data_r,i)   
                new_row = pd.Series(hourly_forecast_data[1]).to_frame().T
                new_row.to_csv(f"{path}/hourly_forecast/{city}.csv", mode='a', header=False, index=False)
            return "I'm busy now. I'm saving hourly forecast data."
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

    hourly_forecast_last_check_convert = datetime_from_utc_to_local(datetime.strptime(hourly_forecast_last_check,"%Y-%m-%dT%H:%M:%S.%fZ"))
    hourly_forecast_last_check_date = format(hourly_forecast_last_check_convert,"%d/%m/%Y")
    hourly_forecast_last_check_clock = format(hourly_forecast_last_check_convert,"%H:%M:%S")

    hourly_forecast_tarih_convert = datetime_from_utc_to_local(datetime.strptime(hourly_forecast_tarih,"%Y-%m-%dT%H:%M:%S.%fZ"))
    hourly_forecast_tarih_date = format(hourly_forecast_tarih_convert,"%d/%m/%Y")
    hourly_forecast_tarih_baslangic_clock = format(hourly_forecast_tarih_convert - timedelta(hours=3),"%H:%M:%S")
    hourly_forecast_tarih_bitis_clock = format(hourly_forecast_tarih_convert,"%H:%M:%S")
    return [hourly_forecast_last_check,[
        city,
        city_hourly_forecast_istno_dict[city],
        hourly_forecast_last_check_date,
        hourly_forecast_last_check_clock,
        hourly_forecast_tarih_date,
        hourly_forecast_tarih_baslangic_clock,
        hourly_forecast_tarih_bitis_clock,
        hourly_forecast_hadise,
        hourly_forecast_sicaklik,
        hourly_forecast_hissedilen_sicaklik,
        hourly_forecast_nem,
        hourly_forecast_ruzgar_yonu,
        hourly_forecast_ruzgarhiz,
        hourly_forecast_max_ruzgarhiz
        ]]

#   daily forecast
def daily_forecast(city):
    params = {"istno":city_daily_forecast_istno_dict[city]}
    daily_forecast_data_r = session.get(f"{daily_forecast_url}", params=params, headers={"Origin":f"{mgm_url}"}).json()
    if daily_forecast_data_r:
        daily_forecast_data = daily_forecast_data_requests(city,daily_forecast_data_r,1)

        if daily_forecast_data[0] != daily_forecast_last_check[city]: 
            daily_forecast_last_check[city] = daily_forecast_data[0]
            for i in [1,2,3,4,5]:
                daily_forecast_data = daily_forecast_data_requests(city,daily_forecast_data_r,i)
                new_row = pd.Series(daily_forecast_data[1]).to_frame().T
                new_row.to_csv(f"{path}/daily_forecast/{city}.csv", mode='a', header=False, index=False)
            return "I'm busy now. I'm saving daily forecast data."
    else:
        print("daily forecast data requests failed")
def daily_forecast_data_requests(city,daily_forecast_data_requests,i):
    
    daily_forecast_check = daily_forecast_data_requests[0]["tarihGun1"]

    daily_forecast_last_check = daily_forecast_data_requests[0][f"tarihGun{i}"]
    daily_forecast_hadise = daily_forecast_data_requests[0][f"hadiseGun{i}"]
    daily_forecast_min_sicaklik = daily_forecast_data_requests[0][f"enDusukGun{i}"]
    daily_forecast_max_sicaklik = daily_forecast_data_requests[0][f"enYuksekGun{i}"]
    daily_forecast_min_nem = daily_forecast_data_requests[0][f"enDusukNemGun{i}"]
    daily_forecast_max_nem = daily_forecast_data_requests[0][f"enYuksekNemGun{i}"]
    daily_forecast_ruzgaryon = daily_forecast_data_requests[0][f"ruzgarYonGun{i}"]
    daily_forecast_ruzgarhiz = daily_forecast_data_requests[0][f"ruzgarHizGun{i}"]

    daily_forecast_timer = datetime_from_utc_to_local(datetime.strptime(daily_forecast_last_check,"%Y-%m-%dT%H:%M:%S.%fZ"))
    daily_forecast_date = format(daily_forecast_timer,"%d/%m/%Y")
    daily_forecast_clock = format(daily_forecast_timer,"%H:%M:%S")

    daily_forecast_check_timer = datetime_from_utc_to_local(datetime.strptime(daily_forecast_check,"%Y-%m-%dT%H:%M:%S.%fZ"))
    daily_forecast_check_date = format(daily_forecast_check_timer,"%d/%m/%Y")
    daily_forecast_check_clock = format(daily_forecast_check_timer,"%H:%M:%S")
    return [daily_forecast_check,[
        city,
        city_instant_istno_dict[city],
        format(daily_forecast_check_timer - timedelta(days=1),"%d-%m-%Y"),
        daily_forecast_date,
        daily_forecast_clock,
        daily_forecast_hadise,
        daily_forecast_min_sicaklik,
        daily_forecast_max_sicaklik,
        daily_forecast_min_nem,
        daily_forecast_max_nem,
        daily_forecast_ruzgaryon,
        daily_forecast_ruzgarhiz
        ]]

#  request links
mgm_url = "https://www.mgm.gov.tr/"
iller = "https://servis.mgm.gov.tr/web/merkezler/iller"
instant_url = "https://servis.mgm.gov.tr/web/sondurumlar?"
daily_forecast_url = "https://servis.mgm.gov.tr/web/tahminler/gunluk?"
hourly_forecast_url = "https://servis.mgm.gov.tr/web/tahminler/saatlik?"

#   create istno dicts
city_instant_istno_dict=data()[1]
city_daily_forecast_istno_dict = data()[2]
city_hourly_forecast_istno_dict = data()[3]

#   create working areas
location = data()[2]

#   create last check dicts
instant_last_check = location.copy()
daily_forecast_last_check = location.copy()
hourly_forecast_last_check = location.copy()

#   create empty DataFrames
instant_df = pd.DataFrame(
    columns=[
        "İl",
        "İstasyon Numarası",
        "Tarih",
        "Saat",
        "Sıcaklık (°C)",
        "Hadise",
        "Yağış Miktarı (mm)",
        "Nem (%)",
        "Rüzgar Yönü",
        "Rüzgar Hızı (km/sa)",
        "A. Basınç",
        "D.İ.Basınç"
        ]
        ) 
daily_forecast_df = pd.DataFrame(
    columns=[
        "İl",
        "İstasyon Numarası",
        "Tarih",
        "Tahmin Tarihi",
        "Tahmin Saati",
        "Hadise",
        "Min. Sıcaklık (°C)",
        "Max. Sıcaklık (°C)",
        "Min. Nem (%)",
        "Max. Nem (%)",
        "Rüzgar Yönü",
        "Rüzgar Hızı (km/sa)"
        ]
        ) 
hourly_forecast_df = pd.DataFrame(
    columns=[
        "İl",
        "İstasyon Numarası",
        "Tarih",
        "Saat",
        "Tahmin Tarihi",
        "Başlangıç Saati",
        "Bitiş Saati",
        "Beklenen Hadise",
        "Sıcaklık (°C)",
        "Hissedilen Sıcaklık (°C)",
        "Nem (%)",
        "Rüzgar Yönü",
        "Ort. Rüzgar Hızı (km/sa)",
        "Maks. Rüzgar Hızı (km/sa)"
        ]
        )

path = "output"

for city in location.keys():
    if not os.path.exists(f"{path}/instant/{city}.csv"):
        instant_df.to_csv(f"{path}/instant/{city}.csv", index=False)

    if not os.path.exists(f"{path}/hourly_forecast/{city}.csv"):
        hourly_forecast_df.to_csv(f"{path}/hourly_forecast/{city}.csv", index=False)

    if not os.path.exists(f"{path}/daily_forecast/{city}.csv"):
        daily_forecast_df.to_csv(f"{path}/daily_forecast/{city}.csv", index=False)
    
    new_row = pd.Series(["-","-","-","-","-","-","-","-","-","-","-","-"]).to_frame().T
    new_row.to_csv(f"{path}/instant/{city}.csv", mode='a', header=False, index=False)

    new_row = pd.Series(["-","-","-","-","-","-","-","-","-","-","-","-","-","-"]).to_frame().T
    new_row.to_csv(f"{path}/hourly_forecast/{city}.csv", mode='a', header=False, index=False)

    new_row = pd.Series(["-","-","-","-","-","-","-","-","-","-","-","-"]).to_frame().T
    new_row.to_csv(f"{path}/daily_forecast/{city}.csv", mode='a', header=False, index=False)
print("empty files are ready.")
keep_alive()

flag = True

print("We are ready. Let's go!")
while flag==True:
    if flag:
        for city in location.keys():
            instant(city)
            hourly_forecast(city)
            daily_forecast(city)
            

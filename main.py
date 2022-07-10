'''
!pip3 install selenium
!pip3 install pandas
!pip3 install datetime
!pip3 install time
'''
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
import datetime
import time
def selenium():
    options = Options()
    options.binary_location = "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(chrome_options = options, executable_path=r"C:\Program Files (x86)\chromedriver.exe")
    return browser
def date(next_date_2):
    current_date = datetime.datetime.now()
    next_date = current_date + datetime.timedelta(days = 1)
    current_date_text = current_date.strftime("%d %B %A")
    next_date_text = next_date.strftime("%d %B %A")
    next_date_2_text = next_date_2.strftime("%d %B %A")
    current_time_text = current_date.strftime("%H:%M")
    month = {"January":"Ocak","February":"Şubat","March":"Mart","April":"Nisan","May":"Mayıs","June":"Haziran","July":"Temmuz","August":"Ağustos","September":"Eylül","October":"Ekim","November":"Kasım","December":"Aralık"}
    for i,j in month.items():
        current_date_text = current_date_text.replace(i,j)
        next_date_text = next_date_text.replace(i,j)
        next_date_2_text = next_date_2_text.replace(i,j)
    weekday = {"Monday":"Pazartesi","Tuesday":"Salı","Wednesday":"Çarşamba","Thursday":"Perşembe","Friday":"Cuma","Saturday":"Cumartesi","Sunday":"Pazar"}
    for i,j in weekday.items():
        current_date_text = current_date_text.replace(i,j)
        next_date_text = next_date_text.replace(i,j)
        next_date_2_text = next_date_2_text.replace(i,j)
    return [current_date_text,next_date_text,next_date_2_text,current_time_text,current_date,next_date]
def log_data(browser,current_time_text,current_date_text):
    # Web Scraper...
    anlik_Temp_C = browser.find_element_by_xpath("//*[@id='pages']/div/section/div[5]/div[1]/div[1]").text
    anlik_rainfall = browser.find_element_by_xpath("//*[@id='pages']/div/section/div[5]/div[1]/div[3]/div[2]/div[2]").text
    anlik_moisture = browser.find_element_by_xpath("//*[@id='pages']/div/section/div[5]/div[2]/div[1]/div[2]/div[2]").text
    anlik_Wind_Speed = browser.find_element_by_xpath("//*[@id='pages']/div/section/div[5]/div[2]/div[2]/div[2]/div[2]").text
    # Elde edilen verileri listeye ekle.
    current_data_time_text.append(current_time_text)
    current_data_date_text.append(current_date_text)
    log_data_Temp_C.append(anlik_Temp_C)
    log_data_rainfall.append(anlik_rainfall)
    log_data_moisture.append(anlik_moisture)
    log_data_Wind_Speed.append(anlik_Wind_Speed)
def Forecast_data(browser,current_date_text):
    for i in [1,2,3,4,5]:
        # Web Scraper...
        Forecast_date_text = browser.find_element_by_xpath("//*[@id='_4_5gunluk']/table/tbody/tr[{}]/td[1]".format(i)).text
        Forecast_Temp_C_min = browser.find_element_by_xpath("//*[@id='_4_5gunluk']/table/tbody/tr[{}]/td[3]".format(i)).text
        Forecast_Temp_C_max = browser.find_element_by_xpath("//*[@id='_4_5gunluk']/table/tbody/tr[{}]/td[4]".format(i)).text
        Forecast_Moisture_min = browser.find_element_by_xpath("//*[@id='_4_5gunluk']/table/tbody/tr[{}]/td[5]".format(i)).text
        Forecast_Moisture_max = browser.find_element_by_xpath("//*[@id='_4_5gunluk']/table/tbody/tr[{}]/td[6]".format(i)).text
        Forecast_Wind_Speed = browser.find_element_by_xpath("//*[@id='_4_5gunluk']/table/tbody/tr[{}]/td[8]".format(i)).text
        # Elde edilen verileri listeye ekle.
        current_data_date_2_text.append(current_date_text)
        Forecast_data_date_text.append(Forecast_date_text)
        Forecast_data_Temp_C_min.append(Forecast_Temp_C_min)
        Forecast_data_Temp_C_max.append(Forecast_Temp_C_max)
        Forecast_data_Moisture_min.append(Forecast_Moisture_min)
        Forecast_data_Moisture_max.append(Forecast_Moisture_max)
        Forecast_data_Wind_Speed.append(Forecast_Wind_Speed) 
def web_scraber(il,ilce,browser=selenium(),anlik_veri_zamani_2=0):
    '''
    il = input("Verilerini çekmek istediğiniz ili giriniz: ")
    ilce = input("Verilerini çekmek istediğiniz ilçeyi giriniz: ")
    '''
    mgm_tahmin_link="https://mgm.gov.tr/tahmin/il-ve-ilceler.aspx?"
    
    if ilce=="":
        link = mgm_tahmin_link + "il=" + il
    else:
        link = mgm_tahmin_link + "il=" + il + "&" + "ilce=" + ilce
    browser.get(link)
    
    while True:
        browser.refresh()
        time.sleep(10)
        next_date_2 = datetime.datetime.now() + datetime.timedelta(days = 1)
        next_date_2_text = date(next_date_2)[2]
        
        Forecast_date_text = browser.find_element_by_xpath("//*[@id='_4_5gunluk']/table/tbody/tr[1]/td[1]").text
        anlik_veri_zamani = browser.find_element_by_xpath("//*[@id='pages']/div/section/h2[1]/span").text
        
        if anlik_veri_zamani != anlik_veri_zamani_2:
                time.sleep(10)
                current_date_text = date(next_date_2)[0]   
                current_time_text = date(next_date_2)[3]
                
                anlik_veri_zamani_2 = browser.find_element_by_xpath("//*[@id='pages']/div/section/h2[1]/span").text
                
                log_data(browser,current_time_text,current_date_text)

                Forecast_date_text = browser.find_element_by_xpath("//*[@id='_4_5gunluk']/table/tbody/tr[1]/td[1]").text
                
                if next_date_2_text == Forecast_date_text:
                    Forecast_data(browser,current_date_text)

                    next_date_2 += datetime.timedelta(days = 1)
                    next_date_2_text = date(next_date_2)[2]
                    print("Gelecek 5 güne ait tahmin verileri alındı.")
                    print("Gerçekleşme tarihi ve saati: \n {} \n {}".format(current_date_text,current_time_text))
                    
                logs_dict = {
                    "Date":current_data_date_text,
                    "Time":current_data_time_text,
                    "Temp_C":log_data_Temp_C,
                    "Rainfall":log_data_rainfall,
                    "Moisture":log_data_moisture,
                    "Wind_Speed":log_data_Wind_Speed
                    }
                Forecast_dict = {
                    "Date":current_data_date_2_text,
                    "Forecast_date":Forecast_data_date_text,
                    "Temp_C_min":Forecast_data_Temp_C_min,
                    "Temp_C_max":Forecast_data_Temp_C_max,
                    "Moisture_min":Forecast_data_Moisture_min,
                    "Moisture_max":Forecast_data_Moisture_max,
                    "Wind_Speed":Forecast_data_Wind_Speed
                    }
                
                logs = pd.DataFrame(logs_dict)
                Forecasts = pd.DataFrame(Forecast_dict)
                
                logs.replace(to_replace=",",value=".",inplace=True)
                Forecasts.replace(to_replace=",",value=".",inplace=True)

                logs.to_excel("logs.xlsx",index=False)
                Forecasts.to_excel("Forecasts.xlsx",index=False)
                
                time.sleep(60) # Veri çekme periyodu
                browser.refresh()
        else:
            print("Güncelleme saati henüz gelmedi. Lütfen güncelleme saatini bekleyiniz.")
            print("Şu Anki Saat:    {}".format(date(next_date_2)[3]))
            time.sleep(60) # Güncellenme saati kontrol etme periyodu

log_data_Temp_C = []
log_data_rainfall = []
log_data_moisture = []
log_data_Wind_Speed = []
current_data_time_text = []
current_data_date_text = []
current_data_date_2_text = []
Forecast_data_date_text = []
Forecast_data_Temp_C_min = []
Forecast_data_Temp_C_max = []
Forecast_data_Moisture_min = []
Forecast_data_Moisture_max = []
Forecast_data_Wind_Speed = []

web_scraber("Samsun","")

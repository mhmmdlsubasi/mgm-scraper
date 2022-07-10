'''requirement
%pip install selenium
%pip install pandas
%pip install datetime
%pip install time
'''

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
import datetime
import time

def selenium(): #   Webdriver Options...
    options = Options()
    options.binary_location = "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(chrome_options = options, executable_path=r"C:\Program Files (x86)\chromedriver.exe")
    return browser

def date(next_forecast_date):   #   Time Definition...

    current_date = datetime.datetime.now()
    next_date = current_date + datetime.timedelta(days = 1)

    current_date_text = current_date.strftime("%d %B %A")
    current_time_text = current_date.strftime("%H:%M")

    next_date_text = next_date.strftime("%d %B %A")
    next_forecast_date_text = next_forecast_date.strftime("%d %B %A")

    #   ENG to TR
    month = {
        "January":"Ocak",
        "February":"Şubat",
        "March":"Mart",
        "April":"Nisan",
        "May":"Mayıs",
        "June":"Haziran",
        "July":"Temmuz",
        "August":"Ağustos",
        "September":"Eylül",
        "October":"Ekim",
        "November":"Kasım",
        "December":"Aralık"
        }
    for i,j in month.items():
        current_date_text = current_date_text.replace(i,j)
        next_date_text = next_date_text.replace(i,j)
        next_forecast_date_text = next_forecast_date_text.replace(i,j)
    #   ENG to TR
    weekday = {
        "Monday":"Pazartesi",
        "Tuesday":"Salı",
        "Wednesday":"Çarşamba",
        "Thursday":"Perşembe",
        "Friday":"Cuma",
        "Saturday":"Cumartesi",
        "Sunday":"Pazar"
        }
    for i,j in weekday.items():
        current_date_text = current_date_text.replace(i,j)
        next_date_text = next_date_text.replace(i,j)
        next_forecast_date_text = next_forecast_date_text.replace(i,j)
    return (current_date_text,next_forecast_date_text,current_time_text)

def log_data(browser,current_time_text,current_date_text):  #   daily forecast
    #   Web Scraper...
    instant_Temp_C = browser.find_element_by_xpath("//*[@id='pages']/div/section/div[5]/div[1]/div[1]").text
    instant_rainfall = browser.find_element_by_xpath("//*[@id='pages']/div/section/div[5]/div[1]/div[3]/div[2]/div[2]").text
    instant_Humidity = browser.find_element_by_xpath("//*[@id='pages']/div/section/div[5]/div[2]/div[1]/div[2]/div[2]").text
    instant_Wind_Speed = browser.find_element_by_xpath("//*[@id='pages']/div/section/div[5]/div[2]/div[2]/div[2]/div[2]").text
    #   Add data to list...
    current_time_text_list.append(current_time_text)
    current_date_text_list.append(current_date_text)
    log_data_Temp_C_list.append(instant_Temp_C)
    log_data_rainfall_list.append(instant_rainfall)
    log_data_Humidity_list.append(instant_Humidity)
    log_data_Wind_Speed_list.append(instant_Wind_Speed)

def daily_forecast_data(browser,current_date_text): #   5 day forecast
    for i in [1,2,3,4,5]:
        #   Web Scraper...
        forecast_date_text = browser.find_element_by_xpath("//*[@id='_4_5gunluk']/table/tbody/tr[{}]/td[1]".format(i)).text
        forecast_Temp_C_min = browser.find_element_by_xpath("//*[@id='_4_5gunluk']/table/tbody/tr[{}]/td[3]".format(i)).text
        forecast_Temp_C_max = browser.find_element_by_xpath("//*[@id='_4_5gunluk']/table/tbody/tr[{}]/td[4]".format(i)).text
        forecast_Humidity_min = browser.find_element_by_xpath("//*[@id='_4_5gunluk']/table/tbody/tr[{}]/td[5]".format(i)).text
        forecast_Humidity_max = browser.find_element_by_xpath("//*[@id='_4_5gunluk']/table/tbody/tr[{}]/td[6]".format(i)).text
        forecast_Wind_Speed = browser.find_element_by_xpath("//*[@id='_4_5gunluk']/table/tbody/tr[{}]/td[8]".format(i)).text
        #   Add data to list...
        next_forecast_date_text_list.append(current_date_text)
        forecast_date_text_list.append(forecast_date_text)
        forecast_min_Temp_C_list.append(forecast_Temp_C_min)
        forecast_min_Temp_C_list.append(forecast_Temp_C_max)
        forecast_min_Humidity_list.append(forecast_Humidity_min)
        forecast_max_Humidity_list.append(forecast_Humidity_max)
        forecast_Wind_Speed_list.append(forecast_Wind_Speed) 

def main(il,ilce,browser=selenium(),last_date_check=None): 
    browser.get(url)    #   open browser with link
    while True:
        browser.refresh()
        time.sleep(10)
        
        forecast_date_text = browser.find_element_by_xpath("//*[@id='_4_5gunluk']/table/tbody/tr[1]/td[1]").text
        date_check = browser.find_element_by_xpath("//*[@id='pages']/div/section/h2[1]/span").text
        
        if date_check != last_date_check:   #   instant weather check

                time.sleep(10)

                current_date_text = date(next_forecast_date)[0]   
                current_time_text = date(next_forecast_date)[2]
                
                last_date_check = browser.find_element_by_xpath("//*[@id='pages']/div/section/h2[1]/span").text
                
                log_data(browser,current_time_text,current_date_text)   #   daily forecast
                print("Anlık tahmin verileri alındı.")
                print("Gerçekleşme saati:   {}".format(current_time_text))

                forecast_date_text = browser.find_element_by_xpath("//*[@id='_4_5gunluk']/table/tbody/tr[1]/td[1]").text
                
                if forecast_date_text == next_forecast_date_text:   #   next weather check
                    daily_forecast_data(browser,current_date_text)  #   5 day forecast

                    next_forecast_date += datetime.timedelta(days = 1)
                    next_forecast_date_text = date(next_forecast_date)[1]

                    print("Gelecek 5 güne ait tahmin verileri alındı.")
                    print("Gerçekleşme tarihi ve saati: \n {} \n {}".format(current_date_text,current_time_text))
                    
                log = {
                    "Date":current_date_text_list,
                    "Time":current_time_text_list,
                    "Temp_C":log_data_Temp_C_list,
                    "Rainfall":log_data_rainfall_list,
                    "Humidity":log_data_Humidity_list,
                    "Wind_Speed":log_data_Wind_Speed_list
                    }
                forecast = {
                    "Date":next_forecast_date_text_list,
                    "Forecast_Date":forecast_date_text_list,
                    "min_Temp_C":forecast_min_Temp_C_list,
                    "max_Temp_C":forecast_min_Temp_C_list,
                    "min_Humidity":forecast_min_Humidity_list,
                    "max_Humidity":forecast_max_Humidity_list,
                    "Wind_Speed":forecast_Wind_Speed_list
                    }
                
                log_df = pd.DataFrame(log)
                forecast_df = pd.DataFrame(forecast)
                
                log_df.replace(to_replace=",",value=".",inplace=True)
                forecast_df.replace(to_replace=",",value=".",inplace=True)

                log_df.to_excel("{}_log.xlsx".format(il+ilce),index=False)
                forecast_df.to_excel("{}_forecast.xlsx".format(il+ilce),index=False)
                
                time.sleep(60) # data extraction time control period
                browser.refresh()
        else:
            print("Güncelleme saati henüz gelmedi. Lütfen güncelleme saatini bekleyiniz.")
            time.sleep(60) # Update time control period

#   list:
log_data_Temp_C_list = []
log_data_rainfall_list = []
log_data_Humidity_list = []
log_data_Wind_Speed_list = []
current_time_text_list = []
current_date_text_list = []
next_forecast_date_text_list = []
forecast_date_text_list = []
forecast_min_Temp_C_list = []
forecast_min_Temp_C_list = []
forecast_min_Humidity_list = []
forecast_max_Humidity_list = []
forecast_Wind_Speed_list = []
#   var:
next_forecast_date = datetime.datetime.now() + datetime.timedelta(days = 1)
next_forecast_date_text = date(next_forecast_date)[1]

#------------------------------
'''
location = {
    "Sinop":"",
    "Samsun":"",
    "Amasya":"",
    "Ordu":""
    }
for il,ilce in location.items():
'''

il="Samsun"
ilce=""

url="https://mgm.gov.tr/tahmin/il-ve-ilceler.aspx?"
    
if ilce=="":
        url += "il=" + il
else:
        url += "il=" + il + "&" + "ilce=" + ilce

main(il,ilce)
#Simple python script to get covid slots for a district_id
#rahul.kolath@gmail.com
#https://github.com/RahulKolath/covidslots
import requests
import json
import smtplib
from datetime import date
from email.message import EmailMessage
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys

#WhatsappInitializationStuff
driver = webdriver.Chrome('/Users/rkola1/Downloads/chromedriver')
driver.get("https://web.whatsapp.com/")
target = '"Home"'


#Http Headers
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
}

#Email variables
gmail_user = 'someuser@gmail.com'
gmail_password = 'password'
to = []
subject = 'Pappu Says Cowin Slot Opened , check Immediately'


def send_whatsapp_message():
    wait = WebDriverWait(driver, 30)
    x_arg = '//span[contains(@title,' + target + ')]'
    group_title = wait.until(EC.presence_of_element_located((
        By.XPATH, x_arg)))
    group_title.click()
    inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]'
    input_box = wait.until(EC.presence_of_element_located((
        By.XPATH, inp_xpath)))
    input_box.send_keys(subject + Keys.ENTER)
    time.sleep(1)


def get_covid_results():
    #curr_date = date.today().strftime("%d-%m-%Y")
    #cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=308&date=" + curr_date
    response = requests.get(cowin_url , headers = headers)
    print("url : " + cowin_url + ", target : " + target + ", email : " + str(to))
    slotAvailableList = []
    if response.status_code >=200   and response.status_code <400:
        print("Status " + str(response.status_code))
        cowin_results =  response.json()
        for center in cowin_results["centers"]:
            slotTuple = ()
            for session in center["sessions"]:
                if  session["available_capacity_dose1"] > 0 and session["min_age_limit"] == 18:
                    slotTuple = (center["name"],center["pincode"],session["date"], session["available_capacity_dose1"])
                    slotAvailableList.append(slotTuple)

    if len(slotAvailableList) > 0:

        #Email Stuff
        msg = EmailMessage()
        msg.set_content(str(slotAvailableList))

        msg['Subject'] = subject
        msg['From'] = gmail_user
        msg['To'] = to

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
            server.quit()
            print('Email sent!')
            try :
                send_whatsapp_message()
                print("whatsapp sent!")
            except Exception as e:
                print('Something went wrong in whatsapp...'+str(e))
            #print("Sleeping for half an hour..")
            #   time.sleep(1800)
        except Exception as e:
            print('Something went wrong...'+str(e))

while True :
    #palakkad
    target = '"Home"'
    curr_date = date.today().strftime("%d-%m-%Y")
    cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=308&date=" + curr_date
    to = ['rahul.kolath@gmail.com','kuttypr@gmail.com','kolath.raghu@gmail.com']
    get_covid_results()
    print("Sleeping for 5 mins..")
    time.sleep(300)
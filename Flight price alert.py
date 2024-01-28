from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

driver=webdriver.Chrome()
url="https://www.kayak.com/flights/YTO-YVR/2024-02-24/2024-03-02?sort=bestflight_a&attempt=1&lastms=1706240976437"
driver.get(url)
sleep(1)


elements = driver.find_elements(By.CLASS_NAME, "nrc6-inner")

flight_names=[]
flight_times=[]
flight_prices=[]


for webelement in elements:
    elementHTML=webelement.get_attribute('outerHTML')
    elementSoup=BeautifulSoup(elementHTML,'html.parser')
    
    flight_name=elementSoup.find("div", {"class":"c_cgF c_cgF-mod-variant-default"}, {"dir":"auto"}).text
    flight_names.append(flight_name)
    #print("FLIGHT NAME:", flight_name)

    flight_time=elementSoup.find("div", {"class":"vmXl vmXl-mod-variant-large"}).text
    flight_times.append(flight_time)
    #print("ARRIVAL DATE/DEPARTURE DATE:", flight_time)

    flight_price=elementSoup.find("div", {"class":"f8F1-price-text"}).text
    flight_prices.append(flight_price)
    #print("JOURNEY COST:", flight_price)


    
length_list=len(flight_names)
    
with open('prices.txt', 'a') as file1:
    for item in flight_names:
        file1.write(str(item) + '\n')

with open('names.txt', 'a') as file2:
    for item in flight_prices:
        file2.write(str(item) + '\n')

with open('timings.txt', 'a') as file3:
    for item in flight_times:
        file3.write(str(item) + '\n')


all_flight_names = []
all_flight_prices = []
all_flight_times = []


with open('prices.txt', 'r') as file1:
    for line in file1:
        all_flight_names.append(line.strip())

with open('names.txt', 'r') as file2:
    for line in file2:
        all_flight_prices.append(line.strip())

with open('timings.txt', 'r') as file3:
    for line in file3:
        all_flight_times.append(line.strip())


current_chunk_prices = all_flight_prices[:length_list]
current_chunk_names = all_flight_names[:length_list]
current_chunk_times = all_flight_times[:length_list]

dropped_flights_set = set()


for i in range(length_list, len(all_flight_prices), length_list):
    next_chunk_prices = all_flight_prices[i:i+length_list]
    next_chunk_names = all_flight_names[i:i+length_list]
    next_chunk_times = all_flight_times[i:i+length_list]

    for i in range(min(len(next_chunk_prices), len(current_chunk_prices), len(next_chunk_names), len(current_chunk_names),len(next_chunk_times), len(current_chunk_times))):
        if (
            i < len(next_chunk_prices) and
            i < len(current_chunk_prices) and
            i < len(next_chunk_names) and
            i < len(current_chunk_names) and
            i < len(next_chunk_times) and
            i < len(current_chunk_times) and
            next_chunk_prices[i] < current_chunk_prices[i] and
            next_chunk_names[i] == current_chunk_names[i]
    ):
            dropped_flights_set.add(f"The flight {next_chunk_names[i]} with timings {next_chunk_times[i]} has dropped to {next_chunk_prices[i]} from {current_chunk_prices[i]}")
            
for dropped_flight in dropped_flights_set:
    print(dropped_flight)


sender_email = "mullangibhuvana9@gmail.com"
receiver_email = "mullangibhuvana9@gmail.com"
subject = "Dropped Flights Notification"


smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "mullangibhuvana9@gmail.com"
smtp_password = "my-password"


body = "\n".join(dropped_flights_set)
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()  # Use TLS for encryption
    server.login(smtp_username, smtp_password)
    server.sendmail(sender_email, receiver_email, message.as_string())

print("Email sent successfully!")




  












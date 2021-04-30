#!/usr/bin/env python
# coding: utf-8
#! C:\Users\Pesapal\AppData\Local\Programs\Python\Python37\python.exe

# In[1]:


import selenium
from selenium import webdriver as wb
import time
from tqdm import tqdm 
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

webD = wb.Chrome("chromedriver.exe")
webD.get('https://www.tripadvisor.com/Restaurants-g294206-Kenya.html')


# In[2]:


time.sleep(15)
webD.find_element_by_class_name('WmEK0bU8').find_element_by_tag_name('input').click()
webD.find_element_by_class_name('WmEK0bU8').find_element_by_tag_name('input').send_keys('nairobi restaurants')
time.sleep(10)


# In[3]:


delay = 20
WebDriverWait(webD, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "_1dvyiAq4"))).click()


# In[ ]:


listOfLinks = []

delay = 5
condition=True
while condition:
    restInfoLinks = webD.find_elements_by_class_name('_2kbTRHSI')
      
    for el in restInfoLinks:
        ppp = el.find_element_by_tag_name('a').get_property('href')
        listOfLinks.append(ppp)
    try:
        time.sleep(5)
        webD.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        nextP = WebDriverWait(webD, delay).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Next')]")))
        nextP.click()
        #webD.find_element_by_xpath("//a[contains(text(),'Next')]").click()
        time.sleep(10)  
    except TimeoutException:
        condition=False
listOfLinks = set(listOfLinks)


# In[ ]:


Rest_data = []

for i in tqdm(listOfLinks):
    webD.get(i)
    try:
        name = webD.find_element_by_class_name('_1hkogt_o').find_element_by_tag_name('h1').text
        #cuisine = webD.find_elements_by_class_name('_1ud-0ITN')[0].find_elements_by_tag_name('span')[6].text
        cuisine = webD.find_elements_by_class_name('_1ud-0ITN')[0].find_elements_by_tag_name('span')
        cuisine = cuisine[6].text if 6<len(cuisine) else "None"
        
        #location = webD.find_elements_by_class_name('_1ud-0ITN')[1].find_elements_by_tag_name('span')[1].find_element_by_class_name('_15QfMZ2L').text
        location = webD.find_elements_by_class_name('_1ud-0ITN')[1].find_elements_by_tag_name('span')
        location = location[1].text if 1<len(location) else "None"
        
        #phone = webD.find_elements_by_class_name('_1ud-0ITN')[1].find_elements_by_tag_name('span')[4].find_element_by_class_name('_15QfMZ2L').text
        phone = webD.find_elements_by_class_name('_1ud-0ITN')[1].find_elements_by_tag_name('span')
        phone = phone[4].find_element_by_class_name('_15QfMZ2L').text if 4<len(phone) else "None"
        
        
        #website = webD.find_elements_by_class_name('_1ud-0ITN')[1].find_elements_by_tag_name('span')[9].find_element_by_tag_name('a').get_property('href')
        website = webD.find_elements_by_class_name('_1ud-0ITN')[1].find_elements_by_tag_name('span')
        website = website[9].find_element_by_tag_name('a').get_property('href') if 9<len(website) else "None"
        
        
        rating = webD.find_element_by_class_name('r2Cf69qf').text
        #specialDiets = webD.find_elements_by_class_name('ui_columns ')[6].find_elements_by_class_name('ui_column ')[1].find_elements_by_tag_name('div')[12].text
        #meals = webD.find_element_by_xpath('//*[@id="component_40"]/div/div/div/div[2]/div/div[2]/div[3]/div[2]').text
        #features = webD.find_element_by_xpath('//*[@id="component_40"]/div/div/div/div[2]/div/div[3]/div[2]/div[2]').text
        
        #priceRange = webD.find_elements_by_class_name('ui_columns ')[6].find_elements_by_class_name('ui_column ')[1].find_elements_by_tag_name('div')[6].text
        priceRange = webD.find_elements_by_class_name('ui_columns ')[6].find_elements_by_class_name('ui_column ')[1].find_elements_by_tag_name('div')
        priceRange = priceRange[6].text if 6<len(priceRange) else "None"
        
    except NoSuchElementException:
        pass
    
    tempJ = {
        'name': name,
        'cuisine': cuisine,
        'location':  location,
        'phone': phone,
        'website': website,
        'rating': rating,
        'priceRange': priceRange,
        'link': i
    }
    Rest_data.append(tempJ)


# In[ ]:


import pandas as pd
# pd.set_option('display.max_columns', None)

data = pd.DataFrame(Rest_data)
 
data.to_csv(r'F:\1. Scrape With Selenium\ta.csv')

#insert into a database

# import pymysql

# connection = pymysql.connect(host = 'localhost',user='root',password = '',db ='tripadvisor')
# cursor=connection.cursor()

# cols = "`,`".join([str(i) for i in data.columns.tolist()])

# for i,row in data.iterrows():
#     sql = "INSERT INTO `rest_info` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
#     cursor.execute(sql, tuple(row))

#     # the connection is not autocommitted by default, so we must commit to save our changes
#     connection.commit()
# connection.close()


# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 14:26:54 2022

"""
import time
import webbrowser
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

link = 'https://ndber.seai.ie/pass/Download/PassDownloadBER.ashx?type=nas&ber=100002807&file=bercert'
counter = 0
success = 0
#options = Options()
#options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_experimental_option("useAutomationExtension", False)
#options.add_experimental_option("excludeSwitches",["enable-automation", 'enable-logging'])
#options.add_argument('--headless')
#options.add_argument('--disable-gpu')  # Last I checked this was necessary.

browser = webdriver.Chrome(ChromeDriverManager().install())#, chrome_options=options)

for ber in range(113000000, 115000000):
    link_1 = link[:70]
    link_2 = str(ber)
    link_3 = link[79:]
    link_final = link_1+link_2+link_3      
    counter +=1
    print("Counter: ", counter)
    print("Ber Code: ", link_2)
    '''
    try:
        webbrowser.open(link_final)  # Go to example.com
        success +=1
        #print("Successful Runs: ", success)
        quit()
    except:
        None
    if counter % 150 == 0:
        time.sleep(35)
        browserExe = "chrome.exe" 
        os.system("taskkill /f /im "+browserExe) 
        #os.system("killall -9 'Google Chrome'")
    if counter % 900 == 0:
        print('Recovering Time 15 Seconds')
        time.sleep(60)
    '''
    try:
        browser.get(link_final) 
    except:
        None

# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 09:16:02 2021

"""
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import bs4
import pandas as pd
from selenium.webdriver.chrome.options import Options
import time


#options = Options()
#options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_experimental_option("useAutomationExtension", False)
#options.add_experimental_option("excludeSwitches",["enable-automation", 'enable-logging'])
#options.add_argument('--headless')
#options.add_argument('--disable-gpu')  # Last I checked this was necessary.

def extract_seai_details(ber_code, browser):
    #Create empty DataFrame
    df = pd.DataFrame(columns=['Address','Eircode', 'Bercode', 'Date of Issue', 'Type of Rating', 'Date Valid Until', 'DEAP Version', 'Building Energy Rating', 'CO2 Emissions Indicator', 'Dwelling Type', 'Year of Construction', 'Floor Area', 'Building Type', 'Building Environment', 'Useful Floor Area', 'Main Heating Fuel'])
    try:
        #Guess BER Number
        ber_try =  ber_code
        #Open page & insert BER Number and Eir Code
        browser = browser
        #type(browser)

        browser.get('https://ndber.seai.ie/pass/ber/search.aspx')
        browser.implicitly_wait(2)
        ber_send = browser.find_element(By.XPATH, '/html/body/form/div[3]/div[3]/div[1]/fieldset/div/table/tbody/tr[3]/td/div/div[1]/span/table/tbody/tr/td[2]/input')
        ber_send.send_keys(ber_try)
        browser.implicitly_wait(2)
        form = browser.find_element(By.XPATH,'/html/body/form/div[3]/div[3]/div[1]/fieldset/div/table/tbody/tr[5]/td/table/tbody/tr/td/input[1]')
        form.click()
        browser.implicitly_wait(2)
        try:
            checker = len(str(browser.find_element(By.XPATH,'/html/body/form/div[3]/div[3]/div[1]/fieldset/div/table/tbody/tr[3]/td/div/div[1]/span/table/tbody/tr/td[1]')))
        except:
            checker = 0    
        print('checker: ', checker)
        runner = 0
        while checker > 50 and runner <= 4:
            browser.implicitly_wait(5)
            if len(str(browser.find_element(By.XPATH, '/html/body/form/div[3]/div[3]/div[1]/fieldset/div/table/tbody/tr[2]/td/div'))) > 10:
                ber_send = browser.find_element(By.XPATH, '/html/body/form/div[3]/div[3]/div[1]/fieldset/div/table/tbody/tr[3]/td/div/div[1]/span/table/tbody/tr/td[2]/input')
                ber_send.send_keys(ber_try)
                browser.implicitly_wait(5)
            form = browser.find_element(By.XPATH,'/html/body/form/div[3]/div[3]/div[1]/fieldset/div/table/tbody/tr[5]/td/table/tbody/tr/td/input[1]')
            form.click()
            try:
                checker = len(str(browser.find_element(By.XPATH,'/html/body/form/div[3]/div[3]/div[1]/fieldset/div/table/tbody/tr[3]/td/div/div[1]/span/table/tbody/tr/td[1]')))
            except:
                checker = 0
            print('checker: ', checker)
            runner+=1
            print('While loop runner: ', str(runner))
            time.sleep(2)
            if runner == 3:
                print('Sleeping for 20 minutes')
                time.sleep(1200)
        browser.implicitly_wait(2)
        #click intermediate page and check if non domestic or domestic building
        form_2 = browser.find_element(By.XPATH,'/html/body/form/div[3]/div[3]/div[3]/span/div/div[3]/div/table/tbody/tr[2]/td[1]/a')
        form_2.click()
            
        #scrape the page
        browser.implicitly_wait(10)
        soup = bs4.BeautifulSoup(browser.page_source, features="html.parser")
        
        #Headline
        ber_type = soup.find('div', {'id':'ctl00_DefaultContent_BERSearch_dfSearchAgain_dataFormHeader'})
        ber_specification = ber_type.get_text().strip()
        #print(ber_specification)
        if ber_specification == 'BER Details - Non Domestic Building':
            #Scrape Non Domestic Buildings
            # First Section
            nber = soup.find('table', {'id':'ctl00_DefaultContent_BERSearch_dfBER_dataFormContainerTable'})
            
            address = nber.find('div', {'id':'ctl00_DefaultContent_BERSearch_dfBER_div_PublishingAddress'})
            address = (address.get_text(', ').strip())
            
            eircode = nber.find('span', {'id':'ctl00_DefaultContent_BERSearch_dfBER_container_Eircode'})
            eircode = eircode.get_text().strip()
            
            energy_rating = nber.find('div', {'id':'ctl00_DefaultContent_BERSearch_dfBER_div_EnergyRating'}) 
            energy_rating = energy_rating.get_text().strip()
            
            co2_emissions = nber.find('div', {'id':'ctl00_DefaultContent_BERSearch_dfBER_div_CDERValue'}) 
            co2_emissions = co2_emissions.get_text().strip()
            
            date_issue = nber.find('span', {'id':'ctl00_DefaultContent_BERSearch_dfBER_container_DateOfIssue'}) 
            date_issue = date_issue.get_text().strip()
            
            type_of_rating = nber.find('span', {'id':'ctl00_DefaultContent_BERSearch_dfBER_container_TypeOfRating'}) 
            type_of_rating = type_of_rating.get_text().strip()
            
            date_valid = nber.find('span', {'id':'ctl00_DefaultContent_BERSearch_dfBER_container_DateValidUntil'}) 
            date_valid = date_valid.get_text().strip()
            
            # Second Section
            nber_2 = soup.find('table', {'id':'ctl00_DefaultContent_BERSearch_dfNdNasStructuralDetails_dataFormContainerTable'})
            
            building_type = nber_2.find('span', {'id':'ctl00_DefaultContent_BERSearch_dfNdNasStructuralDetails_container_BuildingType'}) 
            building_type = building_type.get_text().strip()
            
            year_of_construction = nber_2.find('span', {'id':'ctl00_DefaultContent_BERSearch_dfNdNasStructuralDetails_container_DateOfConstruction'}) 
            year_of_construction = year_of_construction.get_text().strip()
            
            building_environment = nber_2.find('span', {'id':'ctl00_DefaultContent_BERSearch_dfNdNasStructuralDetails_container_BuildingEnvironment'}) 
            building_environment = building_environment.get_text().strip()
            
            useful_floor_area = nber_2.find('div', {'id':'ctl00_DefaultContent_BERSearch_dfNdNasStructuralDetails_div_FloorArea'}) 
            useful_floor_area = useful_floor_area.get_text().strip()
            
            main_heating_fuel = nber_2.find('span', {'id':'ctl00_DefaultContent_BERSearch_dfNdNasStructuralDetails_container_MainHeatingFuel'}) 
            main_heating_fuel = main_heating_fuel.get_text().strip()
            
            df = df.append({'Address': address, 'Eircode': eircode[13:], 'Bercode':ber_code, 'Date of Issue': date_issue[-10:], 'Type of Rating': type_of_rating[20:], 'Date Valid Until':date_valid[-10:] , 'Building Energy Rating': energy_rating, 'CO2 Emissions Indicator': co2_emissions, 'Year of Construction': year_of_construction[-4:], 'Building Type': building_type[20:], 'Building Environment': building_environment[27:], 'Useful Floor Area': useful_floor_area, 'Main Heating Fuel': main_heating_fuel[24:]}, ignore_index = True)
            #print(df)
            
        else:
            #Scrape Domestic Ber Register
            ber_dec = soup.find('table', {'id':'ctl00_DefaultContent_BERSearch_dfBER_dataFormContainerTable'})
            
            address = ber_dec.find('div', {'id':'ctl00_DefaultContent_BERSearch_dfBER_div_PublishingAddress'})
            address = (address.get_text(', ').strip())
            #print(address)
            
            date_issue = ber_dec.find('span', {'id':'ctl00_DefaultContent_BERSearch_dfBER_container_DateOfIssue'}) 
            date_issue = date_issue.get_text().strip()
            #print(date_issue)
            
            type_of_rating = ber_dec.find('span', {'id':'ctl00_DefaultContent_BERSearch_dfBER_container_TypeOfRating'}) 
            type_of_rating = type_of_rating.get_text().strip()
            #print(type_of_rating)
            
            date_valid = ber_dec.find('span', {'id':'ctl00_DefaultContent_BERSearch_dfBER_container_DateValidUntil'}) 
            date_valid = date_valid.get_text().strip()
            #print(date_valid)
            
            deap_version = ber_dec.find('div', {'id':'ctl00_DefaultContent_BERSearch_dfBER_div_BERTool'}) 
            deap_version = deap_version.get_text().strip()
            #print(deap_version)
            
            energy_rating = ber_dec.find('div', {'id':'ctl00_DefaultContent_BERSearch_dfBER_div_EnergyRating'}) 
            energy_rating = energy_rating.get_text().strip()
            #print(energy_rating)
            
            co2_emissions = ber_dec.find('div', {'id':'ctl00_DefaultContent_BERSearch_dfBER_div_CDERValue'}) 
            co2_emissions = co2_emissions.get_text().strip()
            #print(co2_emissions)
            
            dwelling_type = ber_dec.find('span', {'id':'ctl00_DefaultContent_BERSearch_dfBER_container_DwellingType'}) 
            dwelling_type = dwelling_type.get_text().strip()
            #print(dwelling_type)
            
            year_of_construction = ber_dec.find('span', {'id':'ctl00_DefaultContent_BERSearch_dfBER_container_DateOfConstruction'}) 
            year_of_construction = year_of_construction.get_text().strip()
            #print(year_of_construction)
            
            floor_area = ber_dec.find('div', {'id':'ctl00_DefaultContent_BERSearch_dfBER_div_FloorArea'}) 
            floor_area = floor_area.get_text().strip()
            #print(floor_area)
            
            df = df.append({'Address': address, 'Bercode':ber_code, 'Date of Issue': date_issue[-10:], 'Type of Rating': type_of_rating[20:], 'Date Valid Until':date_valid[-10:] , 'DEAP Version': deap_version[-5:], 'Building Energy Rating': energy_rating, 'CO2 Emissions Indicator': co2_emissions, 'Dwelling Type': dwelling_type[20:], 'Year of Construction': year_of_construction[-4:], 'Floor Area': floor_area}, ignore_index = True)
            #print(df)
        
        #browser.quit()
        return df
    
    except:
        #browser.quit()
        print('Error occured')
        time.sleep(5)
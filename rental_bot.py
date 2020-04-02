# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 18:08:37 2020

Author: Rounak Meyur
Description: This program automates the reservation of rental car from a National pickup
location and for specified pickup and return dates. Further improvements need to be made
for time selection, reward days etc. Also requires exception handling which are coming up
in future versions.
"""


# Modules
from selenium import webdriver
from time import sleep
from datetime import datetime
from dotenv import load_dotenv

import sys,os
workPath = os.getcwd()
sys.path.append(workPath)

load_dotenv(dotenv_path=workPath+'/keys.env')
rental_username = os.getenv("RENTAL_USER")
rental_password = os.getenv("RENTAL_PASS")

#%% Class definition 
class Bot():
    """
    Class with attributes and methods to reserve a car from National rental agency.
    It uses Chromedriver dependency. Make sure you have the version compatible with
    your web browser.
	 """
    def __init__(self):
        """
        Initialize the Selenium Chromedriver
        """
        # download chromedriver and provide the path if you haven't
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        return
    
    def login(self):
        """
        Log in to your account with your credentials. For this program, the credentials
        are stored in the paraphrase.py file in the working folder.
        """
        print('Attempting login')
        self.driver.get("https://www.nationalcar.com/en/home")
        
        sleep(3)
        
        sign_btn = self.driver.find_element_by_class_name('page__header__login-title')
        sign_btn.click()
        
        user_in = self.driver.find_element_by_name('username')
        user_in.send_keys(rental_username)
        
        pw_in = self.driver.find_element_by_name('password')
        pw_in.send_keys(rental_password)
        
        login_btn = self.driver.find_element_by_xpath('/html/body/div[6]/div/div/section[1]/div/form/button/span[1]')
        login_btn.click()
        
        sleep(3)
        return
    
    def itinerary(self,pickup,date_pickup,date_return,drop=None):
        """
        Select the pickup location, pickup and drop off times.
        """
        # Pickup Location selection
        pickup_in = self.driver.find_element_by_class_name('search-autocomplete__input')
        pickup_in.send_keys(pickup)
        sleep(3)
        pickup_choice = self.driver.find_element_by_class_name('search-autocomplete__result-title')
        pickup_choice.click()
        sleep(2)
        
        
        
        # Select pickup date and time
        place_id_pickup = 'date-time__pickup-toggle'
        target_date_pickup = datetime.strptime(date_pickup,'%Y-%m-%d').strftime('%B %d')
        xpath_date_pickup = '//button[@aria-label="Pick up. Current value '+target_date_pickup+'"]'
        self.selectdate(datetime.today().strftime('%Y-%m-%d'),
                        date_pickup,place_id_pickup,xpath_date_pickup)
        
        
        
        # Select return date and time
        place_id_return = 'date-time__return-toggle'
        target_date_return = datetime.strptime(date_return, '%Y-%m-%d').strftime('%B %d')
        xpath_date_return = '//button[@aria-label="Return. Current value '+target_date_return+'"]'
        self.selectdate(date_pickup,date_return,place_id_return,xpath_date_return)
        
        
        
        # Finalize the itinerary
        next_btn = self.driver.find_element_by_xpath('//*[@id="booking-widget-inputs"]/div[2]/div/button')
        next_btn.click()
        sleep(10)
        return
    
    def selectdate(self,initial,target,placeholder_id,xpath_date):
        """
        Computes the number of times the right arrow has to be clicked to swipe the
        months and then selects the required date.
        """
        [tyear,tmonth,tday] = [int(x) for x in target.split('-')]
        [iyear,imonth,_] = [int(x) for x in initial.split('-')]
        right_swipes = (tyear-iyear)*12 + (tmonth-imonth)
        
        # Select the placeholder
        date_element = self.driver.find_element_by_id(placeholder_id)
        date_element.click()
        sleep(2)
        
        # Select the right swipe button
        right_btn = self.driver.find_element_by_xpath('//*[@id="dateContainerId"]/div[2]/div[2]/button')
        for i in range(right_swipes-1): 
            right_btn.click()
            sleep(1)
        
        # Select the day button
        day_btn = self.driver.find_element_by_xpath(xpath_date)
        day_btn.click()
        sleep(3)
        return
    
    def bookcar(self,choice='F'):
        """
        Reserve the type of car.
        C: Compact
        E: Economy
        F: Full Size
        P: Premium
        Check the others from website
        """
        xpath_car = '//button[@data-dtm-track="button.select_'+choice+'CAR.reserve_vehicle"]'
        car_btn = self.driver.find_element_by_xpath(xpath_car)
        car_btn.click()
        sleep(5)
        
        review_btn = self.driver.find_element_by_xpath('//*[@id="zl-app"]/div[5]/div/div/div/div/section/div/div/div/div[2]/button')
        review_btn.click()
        sleep(5)
        return
    
    def finalize(self):
        """
        Finalize the reservation. Currently, this just clicks the submit button. This
        assumes that the credit card details are saved in the account.
        """
        final_btn = self.driver.find_element_by_xpath('//*[@id="zl-app"]/div[5]/div/div/div/section/div/div/div/div[2]/div[1]/div/button/span[1]/span')
        final_btn.click()
        sleep(5)
        return
    

#%% Main program starts here

# Create an instance of the class
bot = Bot()

# Login with necessary credentials. The credentials are stored in passphrase.py file
# under the names rental_username and rental_password
bot.login()

# Reservation details: Dates and Pickup Location
bot.itinerary('ROA', '2020-05-22', '2020-05-24')

# Car type (Default is Full Size (F). Others are premium (P), compact (C), economy (E), etc.)
bot.bookcar(choice='P')

# Finalize reservation: Currently commented for trial purposes
# bot.finalize()

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 18:08:37 2020

Author: Rounak Meyur
Description: This program automates likes in an Instagram account. The 
"""


# Modules
from selenium import webdriver
from time import sleep
from datetime import datetime


import sys,os
workPath = os.getcwd()
sys.path.append(workPath)

# Note that passphrase.py has to be updated to user's credentials
from passphrase import facebook_username,facebook_password


#%% Class definition 
class Bot():
    """
    Class with attributes and methods to reserve a car from National rental agency.
    It uses Chromedriver dependency. Make sure you have the version compatible with
    your web browser.
	 """
    def __init__(self):
        """
        Initialize the Selenium Chromedriver and open the website
        """
        # download chromedriver and provide the path if you haven't
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://www.instagram.com/")
        sleep(3)
        return
    
    def login(self):
        """
        Log in to your account with your credentials. For this program, the credentials
        are stored in the paraphrase.py file in the working folder.
        """
        fb_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[1]/button')
        fb_btn.click()
        
        user_in = self.driver.find_element_by_xpath('//*[@id="email"]')
        user_in.send_keys(facebook_username)
        
        pw_in = self.driver.find_element_by_xpath('//*[@id="pass"]')
        pw_in.send_keys(facebook_password)
        
        login_btn = self.driver.find_element_by_xpath('//*[@id="loginbutton"]')
        login_btn.click()
        
        sleep(4)
        
        popup_btn = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]')
        popup_btn.click()
        sleep(2)
        return
    
    def auto_like(self,num):
        """
        Like unliked pictures in the feed
        """
        # Like instagram pictures
        while i <num:
            all_like_btn = self.driver.find_elements_by_class_name('fr66n')
            for like_btn in all_like_btn:
                val = like_btn.find_element_by_class_name("wpO6b ").find_element_by_class_name("_8-yf5 ").get_attribute("fill")
                if val == '#262626':
                    like_btn.click()
                    i+=1
                    sleep(1)
        return
    
    def like(self):
        """
        A method to like individual photos in an instagram account.
        
        Returns 1 if photo was unliked before and liked now
                0 if photo was liked before
        """
        like_btn = self.driver.find_elements_by_class_name('fr66n')[0]
        val = like_btn.find_element_by_class_name("wpO6b ").find_element_by_class_name("_8-yf5 ").get_attribute("fill")
        if val == '#262626':
            like_btn.click()
            sleep(2)
            return 1
        else:
            return 0
    
    def like_account(self,account_name,num=None):
        """
        Returns
        -------
        None.
        Likes all unliked images in a given account
        """
        search_box = self.driver.find_element_by_xpath('//input[@placeholder="Search"]')
        search_box.send_keys(account_name)
        sleep(1)
        account_choice = self.driver.find_element_by_class_name('Ap253')
        account_choice.click()
        sleep(2)
        
        post = self.driver.find_element_by_class_name('g47SY ')
        npost = int(post.text)
        
        photo_btn = self.driver.find_element_by_class_name('eLAPa')
        photo_btn.click()
        sleep(1)
        
        if num==None: num=npost
        
        for i in range(num):
            _ = self.like()
            if i==0:
                xpt = '/html/body/div[4]/div[1]/div/div/a'
            else:
                xpt = '/html/body/div[4]/div[1]/div/div/a[2]'
            if i!=num-1:
                right_btn = self.driver.find_element_by_xpath(xpt)
                right_btn.click()
                sleep(5)
        return
    

#%% Main program starts here

# if __name__ == '__main__':

#     bot = Bot()
#     bot.login()
    
#     choice = sys.argv[1]
#     print("Choice:",choice,)
#     if choice == str(1):
#         account_name = sys.argv[2]
#         bot.like_account(account_name)
#     elif choice == str(2):
#         bot.auto_like(30)
#         print(" Automating likes on feed...")
#     else:
#         print("Invalid Choice")
#         sys.exit(0)
        
bot = Bot()
bot.login()
bot.auto_like(30)


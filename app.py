import time
from selenium import webdriver
import sys

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

import os

class Autobot:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password 
        self.bot = webdriver.Edge(executable_path="./driver/msedgedriver.exe")

    def login(self):
        bot = self.bot
        bot.get('https://instagram.com')
        time.sleep(3)
        id_input = bot.find_element_by_name('username')
        pass_input = bot.find_element_by_name('password')
        id_input.send_keys(self.username)
        pass_input.send_keys(self.password)
        pass_input.send_keys(Keys.RETURN)

    def get_unfollowers(self):
        time.sleep(5)
        bot = self.bot
        bot.get('https://www.instagram.com/' + self.username )
        self.wait('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
        bot.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
        followers = self.get_names()
        self.wait('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a')
        bot.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()
        following = self.get_names()

        #People not following back
        not_followin_back = [people for people in following if people not in followers]
        time.sleep(3)
        print(not_followin_back)
        print(len(not_followin_back))

    def get_fans(self):
        time.sleep(5)
        bot = self.bot
        bot.get('https://www.instagram.com/' + self.username )
        self.wait('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
        bot.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
        followers = self.get_names()
        self.wait('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a')
        bot.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()
        following = self.get_names()

        #People not following back
        fans = [people for people in followers if people not in following]
        time.sleep(3)
        print(fans)
        print(len(fans))
        
    def cancel_sent_req(self):
        pending_list = self.get_pending_req()   
        bot = self.bot
        for x in pending_list:
            bot.get('https://www.instagram.com/' + x )
            self.wait('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/div/button')
            bot.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/div/button').click()
            self.wait('/html/body/div[5]/div/div/div/div[3]/button[1]')
            bot.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[1]').click()
            
            print(x + "  Unfollowed")
        print('Task Completed')        



    def get_names(self):
        bot = self.bot
        time.sleep(4)
        self.wait('/html/body/div[5]/div/div/div[2]')
        scroll_box = bot.find_element_by_xpath('/html/body/div[5]/div/div/div[2]')
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            time.sleep(1)
            try:
                ht = bot.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight;", scroll_box)
            except StaleElementReferenceException:
                continue
        self.wait('a','tag_name')
        time.sleep(1)
        links = scroll_box.find_elements_by_tag_name('a')
        time.sleep(1)
        names = [name.text for name in links if name.text != '']
        bot.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/button').click()
        time.sleep(2)
        return names

    def get_pending_req(self):
        time.sleep(5)
        bot = self.bot
        bot.get('https://www.instagram.com/' + self.username )
        self.wait('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/button')
        bot.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/button').click()
        self.wait('/html/body/div[5]/div/div/div/div/button[5]')
        bot.find_element_by_xpath('/html/body/div[5]/div/div/div/div/button[5]').click()
        self.wait('//*[@id="react-root"]/section/main/div/article/main/section[6]/a')
        bot.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/main/section[6]/a').click()
        self.wait('//*[@id="react-root"]/section/main/div/article/main/div/div[2]/section[1]/section[1]/a')
        bot.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/main/div/div[2]/section[1]/section[1]/a').click()
        self.wait("-utLf", "class_name")
        names = bot.find_elements_by_class_name('-utLf')
        pending_list=[]
        for n in names:
            pending_list.append(n.text)
        return pending_list    
            

        


    def logout(self):
        time.sleep(3)
        bot = self.bot
        self.wait('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/button')
        bot.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/button').click()
        time.sleep(1)
        bot.find_element_by_xpath('/html/body/div[5]/div/div/div/div/button[9]').click()
        exit()



    def wait(self, element_to_locate, by='xpath'):
        bot = self.bot 
        wait = WebDriverWait(bot, 20)
        if by == 'xpath':
            wait.until(EC.element_to_be_clickable((By.XPATH, element_to_locate)))
        elif by == 'class_name':
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, element_to_locate)))
        elif by == 'tag_name':
            wait.until(EC.element_to_be_clickable((By.TAG_NAME, element_to_locate)))    




def main():
    username = input('Enter your usernname:')
    password = input('Enter your password:')
    os.system('cls')
    mybot = Autobot(username,password)
    a = True
    while a:
        print()
        print("*******Autbot*******")
        x = input("1. list Un-followers\n2. list Fans\n3. Cancel all the sent follow requests\n4. Unfollow those who don't follow you back\n5. Exit\nEnter the choice : ")
        if x == "1":
            mybot.login()
            mybot.get_unfollowers()
        elif x == "2":
            mybot.login()
            mybot.get_fans()
        elif x == "3":
            mybot.login()
            mybot.cancel_sent_req()
        elif x == "4":
            print("Sorry not available right now")
        elif x == "5":
            mybot.logout()
            a = False

        else:
            print('Invalid Option')

main()                   



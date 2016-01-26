# -*- coding: utf-8 -*-
"""
Created on Tue Apr 01 11:21:29 2014

@author: tanhe
"""

from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from random import choice
import re
from selenium.webdriver.common.keys import Keys
#import pickle
class wordpress:
    def __init__(self):
        self.browser= webdriver.Firefox();
        self.wait = ui.WebDriverWait(self.browser,20)
        self.browser.set_window_size(1280,800);
    def set_blog(self,homepage,user,passwd):
        self.homepage=homepage;
        self.user=user;
        self.passwd=passwd;
    def login(self):
        self.browser.get(self.homepage);
        #sleep(10);
        self.wait.until(lambda browser=self.browser: browser.find_element_by_link_text("Log in"));
        self.browser.find_element_by_link_text("Log in").click();
        #sleep(5);#?ȴ?5s?õ?½ҳ??????
        self.wait.until(lambda browser=self.browser:browser.find_element_by_xpath("//input[@name='log']"));
        user=self.browser.find_element_by_xpath("//input[@name='log']");
        user.clear();
        user.send_keys(self.user);
        self.wait.until(lambda browser=self.browser:browser.find_element_by_xpath("//input[@name='pwd']"));
        passwd=self.browser.find_element_by_xpath("//input[@name='pwd']");
        passwd.clear();
        passwd.send_keys(self.passwd);
        self.browser.find_element_by_xpath("//input[@type='submit']").click();
        #???˵?½????
        #sleep(5);
        #?˴?Ӧ?е?½?ɹ??Ĳ???
    def post(self,worker_id,log_info):
        self.wait.until(lambda browser=self.browser:browser.find_element_by_xpath("//li[@id='wp-admin-bar-new-content']"));
        self.browser.find_element_by_xpath("//li[@id='wp-admin-bar-new-content']").click();

        #hover=ActionChains(self.browser);
        #hover.move_to_element(new_list).perform();
        #self.wait.until(lambda browser=self.browser:browser.find_element_by_xpath("//li[@id='wp-admin-bar-new-post']"));
        #self.browser.find_element_by_xpath("//li[@id='wp-admin-bar-new-post']").click();
        #sleep(5);
        self.wait.until(lambda browser=self.browser:browser.find_element_by_xpath("//input[@name='post_title']"));
        title=self.browser.find_element_by_xpath("//input[@name='post_title']");
        title.clear();
        title.send_keys(worker_id);
        self.browser.switch_to_frame("content_ifr");
        text_body=self.browser.find_element_by_xpath("//body[@id='tinymce']");
        text_body.send_keys(Keys.TAB);
        text_body.send_keys(log_info);
        self.browser.switch_to_default_content();
        sleep(5);
        self.browser.find_element_by_xpath("//input[@name='publish']").click();
        #sleep(5);
        self.wait.until(lambda browser=self.browser:browser.find_element_by_xpath("//input[@value='Update']"));
        self.browser.quit();
       
        


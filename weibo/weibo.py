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
from string import split,digits
import re
#import pickle

browser = webdriver.Firefox() # �򿪹ȸ�������
wait = ui.WebDriverWait(browser,10)
total_pages=0;
browser.get("http://weibo.cn/")

def login(username,password):
    browser.find_element_by_link_text("登录").click()
    wait.until(lambda browser: browser.find_element_by_xpath("//input[@name='mobile']"))
    user = browser.find_element_by_xpath("//input[@name='mobile']")
    user.clear()
    user.send_keys(username)
    psw = browser.find_element_by_xpath("//input[@type='password']")
    psw.clear()
    psw.send_keys(password)
    verify_code= browser.find_element_by_xpath("//input[@name='code']")
    if(verify_code):
        sleep(10)
    wait.until(lambda browser: browser.find_element_by_xpath("//input[@name='submit']"))
    browser.find_element_by_xpath("//input[@name='submit']").click()
    sleep(3);
    browser.save_screenshot("code.png")
    
    #browser.find_element_by_xpath("//input[@name='submit']").click()


def search(searchWord):
    browser.get("http://weibo.cn/")
    wait.until(lambda browser: browser.find_element_by_xpath("//input[@name='keyword']"))
    
    inputBtn = browser.find_element_by_xpath("//input[@name='keyword']")
    inputBtn.clear()
    inputBtn.send_keys(searchWord.strip().decode("utf-8"))
    #inputBtn.send_keys("С���ֻ�".strip().decode("gbk"))
    browser.find_element_by_xpath("//input[@name='smblog']").click()
    
    #wait.until(lambda browser: browser.find_element_by_class_name("search_num"))

#texts = browser.find_elements_by_xpath("//dl[@class='feed_list W_linecolor ']/dd[@class='content']/p[@node-type='feed_list_content']/em")
def gettext():
    content =[]
    wait.until(lambda browser: browser.find_element_by_class_name("search_page_M"))
    texts = browser.find_elements_by_xpath("//dl[@action-type='feed_list_item']/dd[@class='content']/p[@node-type='feed_list_content']/em")
    #print len(texts)
    for n in texts:
        try:
            highpoints = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        mytext =  highpoints.sub(u'', n.text)
        print mytext.encode("utf-8")
        content.append(mytext.encode("utf-8"))
    return content
def iterate_page():
    global total_pages
    wait.until(lambda browser: browser.find_element_by_xpath("//div[@id='pagelist']/form/div"))
    pages=browser.find_element_by_xpath("//div[@id='pagelist']/form/div")
    print pages.text;
    nums=0;
    for i in split(split(pages.text)[1],'/')[1]:
        if(i in digits):
            nums=nums*10+int(i)
        else:
            break;
    print nums;
    for i in range(1,nums):
        wait.until(lambda browser: browser.find_element_by_xpath("//div[@id='pagelist']/form/div/input[2]"))
        the_page=browser.find_element_by_xpath("//div[@id='pagelist']/form/div/input[2]")
        the_page.clear();
        the_page.send_keys(str(i));
        browser.find_element_by_xpath("//div[@id='pagelist']/form/div/input[3]").click();
        total_pages+=1;
        #if total_pages%10==0:
        print total_pages;
        sleep(15);
def nextPage():
    #wait.until(lambda browser: browser.find_element_by_class_name("search_page_M"))
    if browser.find_elements_by_xpath("//ul[@class='search_page_M']") != None:
        nums = len(browser.find_elements_by_xpath("//ul[@class='search_page_M']/li"))
        #browser.execute_script("window.scrollTo(0, 7100)")
        pg = browser.find_element_by_xpath("//ul[@class='search_page_M']/li[%d]/a" %nums) #.text.encode("gbk")
        y = pg.location['y']+100
        print y
        browser.execute_script('window.scrollTo(0, {0})'.format(y))        
        ActionChains(browser).move_to_element(pg).click(pg).perform()

def main():

    login("huangfeidian@live.cn","10311010")
    while True:
        search("佟丽娅")
        iterate_page();


main()

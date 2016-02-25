# -*- coding: utf-8 -*-


from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from datetime import datetime,time
from weibo import weibo
from random import choice
from string import split,digits
import codecs
import json
import re
#import pickle
browser = webdriver.Firefox() # �򿪹ȸ�������
wait = ui.WebDriverWait(browser,10)
out_file=codecs.open("weibo_test.json","w","utf-8");
total_pages = 0
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
    verify_code = browser.find_element_by_xpath("//input[@name='code']")
    if(verify_code):
        sleep(10)
    wait.until(lambda browser: browser.find_element_by_xpath("//input[@name='submit']"))
    browser.find_element_by_xpath("//input[@name='submit']").click()
    sleep(3)
    browser.save_screenshot("code.png")
    
    #browser.find_element_by_xpath("//input[@name='submit']").click()
def parse_time(today,weibo_ct):
	time_stamp=weibo_ct.split(u"来自")[0];
	if(time_stamp.find(u"年")!=-1):
		#不是今年的不要
		return None;
	if(time_stamp.startswith(u"今天")):
		#处理的是今天的微博
		index=0;
		while(time_stamp[index] not in digits):
			index+=1;
		time_str=str();
		while(time_stamp[index]!=' '):
			time_str+=time_stamp[index];
			index+=1;
		time_today=datetime.strptime(time_str,u"%H:%M").time();
		result_time=datetime.combine(today,time_today);
		return result_time;

	if(time_stamp.find(u"月")!=-1):
		#处理的是既往的微博
		temp_datetime=datetime.strptime(time_stamp,u"%m月%d日 %H:%M ");
		the_date=temp_time.date().replace(year=2016);
		result_datetime=datetime.combine(the_date,temp_time.time());
		return result_datetime
	#剩下的就是那种22分钟前 5秒前之类的 我们不处理
	return None;
	

def search(searchWord):
    browser.get("http://weibo.cn/")
    wait.until(lambda browser: browser.find_element_by_xpath("//input[@name='keyword']"))
    
    inputBtn = browser.find_element_by_xpath("//input[@name='keyword']")
    inputBtn.clear()
    inputBtn.send_keys(searchWord.strip().decode("utf-8"))
    #inputBtn.send_keys("С���ֻ�".strip().decode("gbk"))
    browser.find_element_by_xpath("//input[@name='smblog']").click()
    
    #wait.until(lambda browser:
    #browser.find_element_by_class_name("search_num"))

#texts = browser.find_elements_by_xpath("//dl[@class='feed_list W_linecolor
#']/dd[@class='content']/p[@node-type='feed_list_content']/em")
def search_gettext():
    content = []
    wait.until(lambda browser: browser.find_element_by_class_name("search_page_M"))
    texts = browser.find_elements_by_xpath("//dl[@action-type='feed_list_item']/dd[@class='content']/p[@node-type='feed_list_content']/em")
    #print len(texts)
    for n in texts:
        try:
            highpoints = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        mytext = highpoints.sub(u'', n.text)
        print mytext.encode("utf-8")
        content.append(mytext.encode("utf-8"))
    return content

def search_iterate_page():
    global total_pages
    wait.until(lambda browser: browser.find_element_by_xpath("//div[@id='pagelist']/form/div"))
    pages = browser.find_element_by_xpath("//div[@id='pagelist']/form/div")
    print pages.text
    nums = 0
    for i in split(split(pages.text)[1],'/')[1]:
        if(i in digits):
            nums = nums * 10 + int(i)
        else:
            break
    print nums
    for i in range(1,nums):
        wait.until(lambda browser: browser.find_element_by_xpath("//div[@id='pagelist']/form/div/input[2]"))
        the_page = browser.find_element_by_xpath("//div[@id='pagelist']/form/div/input[2]")
        the_page.clear()
        the_page.send_keys(str(i))
        browser.find_element_by_xpath("//div[@id='pagelist']/form/div/input[3]").click()
        total_pages+=1
        #if total_pages%10==0:
        print total_pages
        sleep(15)
def search_nextPage():
    #wait.until(lambda browser:
    #browser.find_element_by_class_name("search_page_M"))
    if browser.find_elements_by_xpath("//ul[@class='search_page_M']") != None:
        nums = len(browser.find_elements_by_xpath("//ul[@class='search_page_M']/li"))
        #browser.execute_script("window.scrollTo(0, 7100)")
        pg = browser.find_element_by_xpath("//ul[@class='search_page_M']/li[%d]/a" % nums) #.text.encode("gbk")
        y = pg.location['y'] + 100
        print y
        browser.execute_script('window.scrollTo(0, {0})'.format(y))        
        ActionChains(browser).move_to_element(pg).click(pg).perform()

def get_weibo_self_page():
	#获得当前登陆用户某个页面的所有微博
	result=[];
	useless_weibo_num=0;
	today=datetime.today();
	all_weibo_in_page = browser.find_elements_by_xpath("//div[@class='c'][@id]");
	weibo_num_in_page=len(all_weibo_in_page);
	print "the num of weibo in this page is ",weibo_num_in_page;
	for single_weibo in all_weibo_in_page:
		weibo_id = single_weibo.get_attribute("id")
		weibo_body=single_weibo.find_element_by_xpath(".//div[1]");
		try:
			weibo_cmt=weibo_body.find_element_by_xpath(".//span[@class='cmt']");
			#如果遇到转发的微博，直接忽略
			continue;
		except:
			#其实我这里想什么都不干的
			useless_weibo.num+=1;
		weibo_dict={};
		weibo_author=weibo_body.find_element_by_xpath(".//a[@class='nk']");
		weibo_dict["author"]=weibo_author.get_attribute("href");
		weibo_span=weibo_body.find_element_by_xpath(".//span[@class='ctt']");
		weibo_dict["text"]=weibo_span.text;
		print weibo_id+"\t"+weibo_text;
		weibo_ct=single_weibo.find_element_by_xpath(".//div/span[@class='ct']").text;
		print weibo_ct;
		time_stamp=parse_time(today,weibo_ct);
		if(time_stamp):
			weibo_dict["datetime"]=time_stamp;
			result.append(weibo_dict);

	return result;
def get_weibo_user_page(user_home):
	result=[];
	useless_weibo_num=0;
	today=datetime.today();
	wait.until(lambda browser: browser.find_element_by_xpath("//div[@class='c'][@id]"));
	all_weibo_in_page = browser.find_elements_by_xpath("//div[@class='c'][@id]")
	weibo_num_in_page=len(all_weibo_in_page);
	print "the num of weibo in this page is ",weibo_num_in_page;
	for single_weibo in all_weibo_in_page:
		weibo_id = single_weibo.get_attribute("id")
		weibo_body=single_weibo.find_element_by_xpath(".//div[1]");
		try:
			weibo_kt=weibo_body.find_element_by_xpath(".//span[@class='kt']");
			#越过置顶
			weibo_num_in_page-=1;
			continue;
		except:
			weibo_num_in_page-=0;
		try:
			weibo_cmt=weibo_body.find_element_by_xpath(".//span[@class='cmt']");
			weibo_num_in_page-=1;
			#如果遇到转发的微博，直接忽略
			continue;
		except:
			#其实我这里想什么都不干的
			weibo_num_in_page-=0;
		weibo_dict={};
		weibo_dict["id"]=weibo_id;
		weibo_dict["author"]=user_home;
		weibo_text=weibo_body.find_element_by_xpath(".//span[@class='ctt']").text;
		weibo_dict["text"]=unicode(weibo_text);
		print weibo_id+"\t"+weibo_text;
		weibo_ct=single_weibo.find_element_by_xpath(".//div/span[@class='ct']").text;
		print weibo_ct;
		result.append(weibo_dict);
		#time_stamp=parse_time(today,weibo_ct);
		#if(time_stamp):
		#	weibo_dict["datetime"]=time_stamp;
		#	result.append(weibo_dict);
		#else:
		#	weibo_num_in_page-=1;
	return result;
def get_weibo_user_lately(user_home,last_time):

	current_page=user_home;
	continue_condition=True;
	while continue_condition:
		page_result=get_weibo_user_page(user_home);
		if len(page_result)==0:
			continue;
		else:
			if page_result[0]["datetime"]<last_time:
				#第一条微博的时间就超过了上一条微博的时间的话，则不再需要处理
				break;
			else:
				json_result=json.dumps(page_result);
				out_file.write(json_result);
		try:
			next_page=browser.find_element_by_link_text(u"下页");
			next_page.click();
		except:
			print "next page doesn't exists"
			break;
		
def main():
	#login("huangfeidian@live.cn","10311010")
	#browser.get("http://weibo.cn/")
	browser.get("http://weibo.cn/xiaomishouji")
	the_weibo_list=get_weibo_user_page("http://weibo.cn/xiaomishouji");
	#weibo_objects=[];
	#for i in the_weibo_list:
	#	weibo_objects.append(weibo(i));
	#weibo_strings=[];
	#for i in weibo_objects:
	#	weibo_strings.append(i.get_json_dict());
	#json_result=json.dumps(weibo_strings);
	json_result=json.dumps(the_weibo_list);
	out_file.write(json_result);
main()
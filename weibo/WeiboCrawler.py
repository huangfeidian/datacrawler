# -*- coding: utf-8 -*-


from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from datetime import datetime,time
from weibo import weibo_weibo
from random import choice
from string import split,digits,join
import json
from lxml import html,etree
import requests
browser = webdriver.Firefox() 
wait = ui.WebDriverWait(browser,10)
cookie_file=open("weibo_cookie.json","r");
total_pages = 0
#browser.get("http://weibo.cn/")

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
		temp_str=time_stamp.replace(u"月","-");
		temp_str=temp_str.replace(u"日","");
		temp_time=datetime.strptime(temp_str,"%m-%d %H:%M ");
		the_date=temp_time.date().replace(year=2016);
		result_datetime=datetime.combine(the_date,temp_time.time());
		return result_datetime
	#剩下的就是那种22分钟前 5秒前之类的 我们不处理
	return None;
	

#def search(searchWord):
#    browser.get("http://weibo.cn/")
#    wait.until(lambda browser: browser.find_element_by_xpath("//input[@name='keyword']"))
    
#    inputBtn = browser.find_element_by_xpath("//input[@name='keyword']")
#    inputBtn.clear()
#    inputBtn.send_keys(searchWord.strip().decode("utf-8"))
#    #inputBtn.send_keys("С���ֻ�".strip().decode("gbk"))
#    browser.find_element_by_xpath("//input[@name='smblog']").click()
    
#    #wait.until(lambda browser:
#    #browser.find_element_by_class_name("search_num"))

##texts = browser.find_elements_by_xpath("//dl[@class='feed_list W_linecolor
##']/dd[@class='content']/p[@node-type='feed_list_content']/em")
#def search_gettext():
#    content = []
#    wait.until(lambda browser: browser.find_element_by_class_name("search_page_M"))
#    texts = browser.find_elements_by_xpath("//dl[@action-type='feed_list_item']/dd[@class='content']/p[@node-type='feed_list_content']/em")
#    #print len(texts)
#    for n in texts:
#        try:
#            highpoints = re.compile(u'[\U00010000-\U0010ffff]')
#        except re.error:
#            highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
#        mytext = highpoints.sub(u'', n.text)
#        print mytext.encode("utf-8")
#        content.append(mytext.encode("utf-8"))
#    return content

#def search_iterate_page():
#    global total_pages
#    wait.until(lambda browser: browser.find_element_by_xpath("//div[@id='pagelist']/form/div"))
#    pages = browser.find_element_by_xpath("//div[@id='pagelist']/form/div")
#    print pages.text
#    nums = 0
#    for i in split(split(pages.text)[1],'/')[1]:
#        if(i in digits):
#            nums = nums * 10 + int(i)
#        else:
#            break
#    print nums
#    for i in range(1,nums):
#        wait.until(lambda browser: browser.find_element_by_xpath("//div[@id='pagelist']/form/div/input[2]"))
#        the_page = browser.find_element_by_xpath("//div[@id='pagelist']/form/div/input[2]")
#        the_page.clear()
#        the_page.send_keys(str(i))
#        browser.find_element_by_xpath("//div[@id='pagelist']/form/div/input[3]").click()
#        total_pages+=1
#        #if total_pages%10==0:
#        print total_pages
#        sleep(15)
#def search_nextPage():
#    #wait.until(lambda browser:
#    #browser.find_element_by_class_name("search_page_M"))
#    if browser.find_elements_by_xpath("//ul[@class='search_page_M']") != None:
#        nums = len(browser.find_elements_by_xpath("//ul[@class='search_page_M']/li"))
#        #browser.execute_script("window.scrollTo(0, 7100)")
#        pg = browser.find_element_by_xpath("//ul[@class='search_page_M']/li[%d]/a" % nums) #.text.encode("gbk")
#        y = pg.location['y'] + 100
#        print y
#        browser.execute_script('window.scrollTo(0, {0})'.format(y))        
#        ActionChains(browser).move_to_element(pg).click(pg).perform()
def next_page():
	try:
		next_page_short_url=browser.find_element_by_link_text(u"下页").get_attribute("href");
		return next_page_short_url;
	except:
		return None;

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
		#print weibo_id+"\t"+weibo_text;
		weibo_ct=single_weibo.find_element_by_xpath(".//div/span[@class='ct']").text;
		#print weibo_ct;
		time_stamp=parse_time(today,weibo_ct);
		if(time_stamp):
			#weibo_dict["datetime"]=time_stamp;
			weibo_dict["datetime"]=time_stamp.strftime("%Y-%m-%d %H:%M:%S");
			result.append(weibo_dict);

	return result;
def get_cookie_str():
	cookies= "; ".join([item["name"] + "=" + item["value"] for item in browser.get_cookies()]);
def get_weibo_user_page(user_page):
	#获得特定用户的某个页面的微博
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
		weibo_dict["author"]=user_page;
		weibo_text=weibo_body.find_element_by_xpath(".//span[@class='ctt']").text;
		weibo_dict["text"]=unicode(weibo_text);
		#print weibo_id+"\t"+weibo_text;
		weibo_ct=single_weibo.find_element_by_xpath(".//div/span[@class='ct']").text;
		#print weibo_ct;
		
		time_stamp=parse_time(today,weibo_ct);
		if(time_stamp):
			#weibo_dict["datetime"]=time_stamp;
			weibo_dict["datetime"]=time_stamp.strftime("%Y-%m-%d %H:%M:%S");
			result.append(weibo_dict);
		else:
			weibo_num_in_page-=1;
	return result;
def get_weibo_user_lately(user_home,last_time):
	current_page=user_home;
	total_weibo=[];
	while current_page!=None:
		browser.get(current_page);
		page_result=get_weibo_user_page(current_page);
		#if len(page_result)==0:
		#	continue;
		#else:
		#	if page_result[0]["datetime"]<last_time:
		#		#第一条微博的时间就超过了上一条微博的时间的话，则不再需要处理
		#		break;
		#	else:
		#		total_weibo.extend(page_result);
		total_weibo.extend(page_result);
		if(len(total_weibo)>=200):
			break;
		current_page=next_page();
	return total_weibo;
def get_real_homepage(user_home):
	#从用户的主页获得用户的个人uid的url
	follow_url=browser.find_element_by_link_text(u"关注").get_attribute("href");
	#/xxxxxx/follow the xxxx is unique user id
	user_id=join(info_url.split("/")[0:-1],"/");
	return user_id;


def get_follower_user(user_home):
	browser.get(user_home);
	follow_url=browser.find_element_by_xpath("//div[@class='tip2']/a[1]").get_attribute("href");
	
	follow_url_list=list();
	while follow_url!=None:
		fo_url_this_page=get_follower_page(follow_url);
		for url in fo_url_this_page:
			follow_url_list.append(url);
		follow_url=next_page();
	return follow_url_list;

def get_follower_page(follow_page):
	browser.get(follow_page);
	followers_in_page=browser.find_elements_by_xpath("//table/tbody/tr/td[2]");
	follower_in_page=[];
	for i in followers_in_page:
		temp_user=dict();
		temp_user["home"]=i.find_element_by_xpath(".//a[1]").get_attribute("href");
		temp_user["nick"]=i.find_element_by_xpath(".//a[1]").text;
		fan_string=i.text;
		fan_num_list=join(filter((lambda x : x in digits),list(fan_string)),"");
		fan_num_int=int(fan_num_list);
		temp_user["fan_num"]=fan_num_int;
		follower_in_page.append(temp_user);
	# it may not be the unique id 
	return follower_in_page;
	
def main():
	#browser.get("http://weibo.cn/");
	#login("huangfeidian@live.cn","10311010")
	browser.get("http://weibo.cn/404page");
	cookie_str=join(cookie_file.readlines(),"\n");
	cookie=json.loads(cookie_str);
	for i in cookie:
		browser.add_cookie(i);
	browser.get("http://weibo.cn/");
	#browser.get("http://weibo.cn/")
	#browser.get("http://weibo.cn/xiaomishouji")
	#the_weibo_list=get_weibo_user_page("http://weibo.cn/xiaomishouji");
	#last_time=datetime.today();
	#the_fo_list=get_weibo_user_lately("http://weibo.cn/xiaomishouji",last_time);
	#weibo_objects=[];
	#for i in the_weibo_list:
	#	weibo_objects.append(weibo(i));
	#weibo_strings=[];
	#for i in weibo_objects:
	#	weibo_strings.append(i.get_json_dict());
	#json_result=json.dumps(weibo_strings);
	#cookie=list(browser.get_cookies());
	#json_result=json.dumps(cookie);
	#cookie_file.write(json_result);
main()

# -*- coding: utf-8 -*-
import json
import requests
from string import join,digits
from lxml import html
from datetime import datetime,timedelta
from time import sleep
import codecs
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import traceback
import os
class request_session:
	def __init__(self):
		self.ss_proxy=None;
		self.ss_header=None;
		self.ss_cookie=None;
		self.user_name=None;
		self.user=None;
		self.domain=u"http://weibo.cn";
		self.ss_referer="http://www.baidu.com";
		self.content=None;
		self.cur_link=None;
		self.response=None;
		self.weibo_result=None;
		self.weibo_total_num=0;
		self.weibo_lately_num=0;
		self.user_homepage=None;
		self.last_log_time=None;
		self.user_data=dict();
		self.ss=requests.Session();
		self.smtp163=smtplib.SMTP();

	def set_ss_config(self,session_config):
		self.ss_proxy=session_config["proxy"];
		self.ss_cookie=session_config["cookie"];
		self.ss_header=session_config["header"];

		for cookie in self.ss_cookie:
			self.ss.cookies.set(cookie["name"],cookie["value"],domain=cookie["domain"],path=cookie["path"]);
		self.ss.proxies=self.ss_proxy;
		self.ss.headers=self.ss_header;
	def set_email_config(self,email_config):
		self.email_from_addr=email_config["from_addr"];
		self.email_to_addr=email_config["to_addr"];
		self.email_from_passwd=email_config["from_passwd"];
		self.email_smtp_addr=email_config["smtp_addr"];
		self.email_smtp_port=email_config["smtp_port"];
	def set_log_config(self,log_config):
		self.user_name=log_config["user_name"];
		if(not os.path.exists(self.user_name)):
			os.mkdir(self.user_name);
		self.weibo_total_num=log_config["total_num"];
		self.last_log_time=datetime.now();
	def set_user_log(self,user_log):
		for i in user_log:
			self.user_data[i]=dict();
			self.user_data[i]["timestamp"]=datetime.strptime(user_log[i]["timestamp"],"%Y-%m-%d %H:%M:%S");
			self.user_data[i]["weibo_num"]=user_log[i]["weibo_num"];
	def save_routine(self):
		# 保存每个user 的log 和所有user的统计log
		
		#要把时间转换为字符串
		translated_data=dict();

		for i in self.user_data:
			translated_data[i]=dict();
			translated_data[i]["weibo_num"]=self.user_data[i]["weibo_num"];
			translated_data[i]["timestamp"]=self.user_data[i]["timestamp"].strftime(("%Y-%m-%d %H:%M:%S"))
		user_data_str=json.dumps(translated_data,ensure_ascii=False);

		user_file_name="user_log "+datetime.now().strftime(("%Y-%m-%d %H-%M-%S"))+".json";
		log_data=dict();
		log_data["user_name"]=self.user_name;
		log_data["weibo_total_num"]=self.weibo_total_num;
		log_data["log_time"]=self.last_log_time;
		log_data["user_file"]=user_file_name;
		log_data_str=json.dumps(log_data,ensure_ascii=False);
		os.chdir(self.user_name);
		
		user_file=open(user_file_name,"w");
		user_file.write(user_data_str);
		user_file.close();
		log_file_name=self.user_name+".json";
		log_file=open(config_file_name,"w");
		log_file.write(log_data_str);
		log_file.close();

	def send_email_except(self):
		msg=MIMEMultipart();
		msg["To"]=self.email_to_addr;
		msg["Subject"]="exception from "+self.user_name+" "+datetime.now().strftime("%Y-%m-%d %H-%M-%S");
		msg["From"]=self.email_from_addr;
		attachment==MIMEText(self.content,"base64","utf-8");
		attachment["Content-Type"]="application/octet-stream";
		attachment["Content-Disposition"]="attachment; filename=\"content.xml\"" 
		exception_msg=MIMEText(traceback.format_exc());
		msg.attach(attachment);
		msg.attach(exception_msg);
		try:
			self.smtp163.connect(self.email_smtp_addr,self.email_smtp_port);
			self.smtp163.login(self.email_from_addr,self.email_from_passwd);
			self.smtp163.sendmail(self.email_from_addr,self.email_to_addr,msg.as_string());
			self.smtp163.close();
		except:
			dumpfile=open(msg["Subject"],"w");
			dumpfile.write(msg.as_string());
			dumpfile.close();

	def send_email_log(self):
		msg=MIMEMultipart();
		msg["To"]=self.email_to_addr;
		msg["Subject"]="log from "+self.user_name+" "+datetime.now().strftime("%Y-%m-%d %H-%M-%S");
		msg["From"]=self.email_from_addr;
		log_msg_str="total weibo num is "+str(self.weibo_total_num)+"weibo lately num is "+str(self.weibo_lately_num);
		self.weibo_lately_num=0;
		log_msg=MIMEText(log_msg_str);
		msg.attach(log_msg);
		try:
			self.smtp163.connect(self.email_smtp_addr,self.email_smtp_port);
			self.smtp163.login(self.email_from_addr,self.email_from_passwd);
			self.smtp163.sendmail(self.email_from_addr,self.email_to_addr,msg.as_string());
			self.smtp163.close();
		except:
			dumpfile=open(msg["Subject"],"w");
			dumpfile.write(msg.as_string());
			dumpfile.close();

	def set_user(self,in_user):
		self.user=in_user;

	def parse_time(self,today,weibo_ct):
		time_stamp=weibo_ct.split(u"来自")[0];
		if(time_stamp.find(u"年")!=-1):
			#如果有年的话，基本可以确认是去年及以前的了，直接忽略
			return None;
		if(time_stamp.startswith(u"今天")):
			#处理的是今天的发表时间
			index=0;
			while(time_stamp[index] not in digits):
				index+=1;
			time_str=str();
			while(time_stamp[index]!=' '):
				time_str+=time_stamp[index];
				index+=1;
			time_today=datetime.strptime(time_str,"%H:%M").time();
			result_time=datetime.combine(today,time_today);
			return result_time;
		if(time_stamp.find(u"月")!=-1):
			#处理的是既往的微博
			temp_str=time_stamp.replace(u"月","-");
			temp_str=temp_str.replace(u"日","");
			temp_str=u"2016-"+temp_str;
			result_datetime=datetime.strptime(temp_str,"%Y-%m-%d %H:%M ");
			return result_datetime
		#剩下的就是那种22分钟前 5秒前之类的 我们不处理
		return None;
	def get_page(self,page_link):
		self.cur_link=page_link;
		response=self.ss.get(self.cur_link);
		self.content=response.content;
		self.tree=html.fromstring(self.content);
	def get_weibo_self_page(self):
		#从当前登录用户的页面中获得微博
		result=[];
		useless_weibo_num=0;
		today=datetime.today();
		all_weibo_in_page = self.tree.xpath("//div[@class='c'][@id]");
		weibo_num_in_page=len(all_weibo_in_page);
		print "the num of weibo in this page is ",weibo_num_in_page;
		for single_weibo in all_weibo_in_page:
			#print single_weibo;
			weibo_dict={};
			weibo_id = single_weibo.get("id");
			weibo_dict["id"]=weibo_id;
			weibo_body=single_weibo.xpath(".//div[1]")[0];
		
			weibo_cmt=weibo_body.xpath(".//span[@class='cmt']");
			#如果是转发，则直接忽略
			if(len(weibo_cmt)!=0):
				#print "a comment here"
				continue;
			weibo_author=weibo_body.xpath(".//a[@class='nk']")[0];
			weibo_dict["author"]=weibo_author.get("href");
			weibo_span=weibo_body.xpath(".//span[@class='ctt']")[0];
			weibo_dict["text"]=weibo_span.text;
			#print weibo_id+"\t"+weibo_text;
			weibo_ct=single_weibo.xpath(".//div/span[@class='ct']")[0].text.replace(u"\xa0"," ");
			#result.append(weibo_dict);
			#print weibo_ct;
			time_stamp=parse_time(today,weibo_ct);
			if(time_stamp):
			#weibo_dict["datetime"]=time_stamp;
				weibo_dict["datetime"]=time_stamp.strftime("%Y-%m-%d %H:%M:%S");
				result.append(weibo_dict);
		#print "useful num is ",len(result);
		return result;

	def next_page(self):
		#注意的是lxml不会对/abc/efg这类的地址直接加上当前域名，所以我们需要手动操作
		#手动加上"weibo.cn
		next_page=self.tree.xpath(u".//a[text()='下页']");
		if(len(next_page)==0):
			return None;
		else:
			return self.domain+next_page[0].get("href");

	def get_weibo_user_page(self,user_home):
		#获得某个用户的某个页面的所有微博
		result=[];
		useful_weibo_num=0;
		today=datetime.today();
		all_weibo_in_page = self.tree.xpath("//div[@class='c'][@id]")
		weibo_num_in_page=len(all_weibo_in_page);
		print "the num of weibo in this page is ",weibo_num_in_page;
		for single_weibo in all_weibo_in_page:
			weibo_id = single_weibo.get("id");
			weibo_body=single_weibo.xpath(".//div[1]")[0];

			weibo_kt=weibo_body.xpath(".//span[@class='kt']");
			#跳过置顶
			if(len(weibo_kt)!=0):
				continue;
			weibo_cmt=weibo_body.xpath(".//span[@class='cmt']");
			#跳过转发
			if(len(weibo_cmt)!=0):
				continue;

			weibo_dict={};
			weibo_dict["id"]=weibo_id;
			weibo_dict["author"]=user_home;
			#weibo_text=weibo_body.xpath(".//span[@class='ctt']")[0].text;
			weibo_ctt=weibo_body.xpath(".//span[@class='ctt']")[0];
			weibo_text=unicode(weibo_ctt.xpath("string()"));
			weibo_dict["text"]=weibo_text;
			#print weibo_id+"\t"+weibo_text;
			weibo_ct=single_weibo.xpath(".//div/span[@class='ct']")[0].text.replace(u"\xa0"," ");
			#print weibo_ct;
			
			time_stamp=self.parse_time(today,weibo_ct);
			if(time_stamp):
				#weibo_dict["datetime"]=time_stamp;
				weibo_dict["datetime"]=time_stamp.strftime("%Y-%m-%d %H:%M:%S");
				weibo_dict["timestamp"]=time_stamp;
				result.append(weibo_dict);
				useful_weibo_num+=1;
		return result;

	def get_weibo_user_lately(self,user_home,last_time):
		current_page=user_home;
		total_weibo=[];
		while current_page!=None:
			sleep(0.5);
			print "get page ",current_page;
			self.get_page(current_page);
			page_result=self.get_weibo_user_page(user_home);
			if len(page_result)==0:
				continue;
			else:
				if page_result[0]["datetime"]<last_time:
					#忽略时间比上一次记录晚的微博
					break;
				else:
					total_weibo.extend(page_result);
			total_weibo.extend(page_result);
			if(len(total_weibo)>=10):
				break;
			current_page=self.next_page();
		return total_weibo;
	def get_real_homepage(self,user_home):
		#由用户的主页获得用户的uid主页
		self.get_page(user_home);
		info_url=self.domain+self.tree.xpath(u".//a[text()=u'资料']")[0].get("href");
		#/xxxxxx/info the xxxx is unique user id
		user_id=join(info_url.split("/")[0:-1],"/");
		return user_id;

	def get_follower_page(self):
		#获得某个用户的某个关注界面的所有关注对象的url
		followers_in_page=self.tree.xpath("//table/tbody/tr/td[2]");
		follower_in_page=[];
		for i in followers_in_page:
			temp_user=dict();
			temp_element=i.xpath(".//a[1]")[0]
			temp_user["home"]=self.domain+ temp_element.get("href");
			temp_user["nick"]=temp_element.text;
			fan_string=i.text;
			fan_num_list=join(filter((lambda x : x in digits),list(fan_string)),"");
			fan_num_int=int(fan_num_list);
			temp_user["fan_num"]=fan_num_int;
			follower_in_page.append(temp_user);
		# it may not be the unique id 
		return follower_in_page;
	def get_follower_user(self,user_home):
		#获得某个用户的关注列表，weibo最多返回200个
		self.get_page(user_home);
		follow_url=self.domain+self.tree.xpath("//div[@class='tip2']/a[1]")[0].get("href");
		follow_url_list=list();
		while follow_url!=None:
			self.get_page(follow_url);
			fo_url_this_page=self.get_follower_page(follow_url);
			for url in fo_url_this_page:
				follow_url_list.append(url);
			follow_url=self.next_page();
		return follow_url_list;
	def filter_user_weibo(self,user_home,weibo_batch):
		result=[];
		last_time=self.user_data[user_home];
		filter_result=[i for  i in weibo_batch and i["timestamp"]>last_time];
		this_time=last_time;
		for i in filter_result:
			if(i["timestamp"]>this_time):
				this_time=i["timestamp"];
		self.user_data[user_home]=this_time;
		self.user_weibo_num[user_home]+=len(filter_result);
		return filter_result;

	def update_weibo_result(self,weibo_batch):
		new_batch_len=len(weibo_batch);
		self.weibo_lately_num+=new_batch_len;
		self.weibo_total_num+=new_batch_len;
		self.weibo_result.extend(weibo_batch);
		os.chdir(self.user_name);
		while(len(self.weibo_result)>100):
			file_name=datetime.now().strftime("%Y-%m-%d %H-%M-%S")+".json";
			output_file=open(file_name,"w");
			the_data=self.weibo_result[0:100];
			self.weibo_result=self.weibo_result[100:];
			output_file.write(json.dumps(the_data,ensure_ascii=False));
			output_file.close();
		this_log_time=datetime.now();
		time_1_hour=timedelta(hours=1.0);
		if(this_log_time-last_log_time>time_1_hour):
			#TO-DO

def main():

	proxies = {
		#"http": "http://huangfeidian:10311010@127.0.0.1:1898",
		#"https": "http://huangfeidian:10311010@127.0.0.1:1898",
		};
	headers={
		"User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
		"Accept":"*/*",
		"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
		"Accept-Encoding": "gzip, deflate, br",
		};
	cookie_file=open("weibo_cookie.json","r");
	cookie_str=join(cookie_file.readlines(),"\n");
	weibo_cookies=json.loads(cookie_str);
	session=request_session();
	session_cfg=dict();
	session_cfg["header"]=headers;
	session_cfg["cookie"]=weibo_cookies;
	session_cfg["proxy"]=proxies
	session.set_ss_config(session_cfg);
	# for cookie in weibo_cookies:
	# 	s.cookies.set(cookie["name"],cookie["value"],domain=cookie["domain"],path=cookie["path"]);
	result=session.get_weibo_user_lately("http://weibo.cn/xiaomishouji","hehe");
	response_file=codecs.open("respons.json","w","utf-8");
	weibo_result=json.dumps(result,ensure_ascii=False);

	#page_raw=codecs.open("raw_res.html","w","utf-8");
	#page_raw.write(r.text);
	# page_raw.close();
	# weibo_result=json.dumps(get_weibo_self_page(r.content,"http://weibo.cn"))
	response_file.write(weibo_result);
main();
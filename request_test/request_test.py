# -*- coding: utf-8 -*-
import json
import requests
from string import join
from lxml import html
from datetime import datetime
import codecs
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
def get_weibo_self_page(content,page_url):
	tree=html.fromstring(content);
	#获得当前登陆用户某个页面的所有微博
	result=[];
	useless_weibo_num=0;
	today=datetime.today();
	all_weibo_in_page = tree.xpath("//div[@class='c'][@id]");
	weibo_num_in_page=len(all_weibo_in_page);
	print "the num of weibo in this page is ",weibo_num_in_page;
	for single_weibo in all_weibo_in_page:
		#print single_weibo;
		weibo_dict={};
		weibo_id = single_weibo.get("id");
		weibo_dict["id"]=weibo_id;
		weibo_body=single_weibo.xpath(".//div[1]")[0];
		
		weibo_cmt=weibo_body.xpath(".//span[@class='cmt']");
		#如果遇到转发的微博，直接忽略
		if(len(weibo_cmt)!=0):
			print "a comment here"
			continue;
		
		
		weibo_author=weibo_body.xpath(".//a[@class='nk']")[0];
		weibo_dict["author"]=weibo_author.get("href");
		weibo_span=weibo_body.xpath(".//span[@class='ctt']")[0];
		weibo_dict["text"]=weibo_span.text;
		#print weibo_id+"\t"+weibo_text;
		#weibo_ct=single_weibo.xpath(".//div/span[@class='ct']")[0].text;
		result.append(weibo_dict);
		#print weibo_ct;
		# time_stamp=parse_time(today,weibo_ct);
		# if(time_stamp):
		# 	#weibo_dict["datetime"]=time_stamp;
		# 	weibo_dict["datetime"]=time_stamp.strftime("%Y-%m-%d %H:%M:%S");
		# 	result.append(weibo_dict);
	print "useful num is ",len(result);
	return result;
def main():

	s=requests.Session();
	proxies = {
		"http": "http://huangfeidian:10311010@127.0.0.1:1898",
		"https": "http://huangfeidian:10311010@127.0.0.1:1898",
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
	# for cookie in weibo_cookies:
	# 	s.cookies.set(cookie["name"],cookie["value"],domain=cookie["domain"],path=cookie["path"]);
	s.proxies=proxies;
	s.headers=headers;
	r=s.get("https://www.google.com");
	print r.status_code;
	response_file=codecs.open("respons.json","w","utf-8");
	page_raw=codecs.open("raw_res.html","w","utf-8");
	page_raw.write(r.text);
	# page_raw.close();
	# weibo_result=json.dumps(get_weibo_self_page(r.content,"http://weibo.cn"))
	# response_file.write(weibo_result);
main();
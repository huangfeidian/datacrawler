# -*- coding: utf-8 -*-
from request_session import request_session
from string import join;
import json;
import threading;
class crawler_mgr:
	def __init__(self):
		self.proxylist=None;
		self.email_config=None;
		self.worker_list=[];
		self.ss_header=None;
        self.cookie_dcit=None;
	def set_proxy(self,proxy_file_name):
		proxy_file=open(proxy_file_name,"r");
		proxy_str=join(proxy_file.readlines(),"\n");
		self.proxylist=json.loads(proxy_str);
    def set_cookie(self,cookie_file_name):
        cookie_file=open(cookie_file_name,"r");
        cookie_str=join(cookie_file.readlines(),"\n");
        self.cookie_dict=json.loads(cookie_str);
	def set_email(self,email_file_name):
		email_file=open(email_file_name,"r");
		email_str=join(email_file.readlines(),"\n");
		self.email_config=json.loads(email_str);
	def set_woker_list(self,wk_list_file_name):
		header={
		"User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
		"Accept":"*/*",
		"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
		"Accept-Encoding": "gzip, deflate, br",
		};
		wk_list_file=open(wk_list_file_name,"r");
		wk_name_list=json.loads(join(wk_list_file.readlines(),"\n"));
		i=0;
		proxy_len=len(self.proxylist);
		for name in wk_name_list:
			i+=1;
			new_worker=request_session();
            new_worker.set_log_config(name);
			new_worker.set_email_config(self.email_config);
			new_worker.set_ss_config(self.proxylist[i%proxy_len],header,self.cookie_dcit[name]);
			self.worker_list.append(new_worker);
	def run(self):
		threads=[];
		for i in self.worker_list:
			temp_thread=threading.Thread(target=self.run,args=None);
			threads.append(temp_thread);
		for i in threads:
			i.setDaemon(True);
			i.start();
		for i in threads:
			i.join();
		return;
